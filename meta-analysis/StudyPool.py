import copy
from Study import Study
import numpy as np
from scipy.stats import chi2


class StudyPool:
    """ Holds a pool of research studies and performs meta-analysis,
        provides methods to calculate statistics of interest,
        and producing tree plots (tree plots not yet implemented)

    Attributes:
        studies (list) collection containing studies
        outcome_label (str) type of outcome currently registered; set using set_outcome() method
        effect_sizes (numpy 1d array) effect sizes associated with currently registered outcome_label
        variances (numpy 1d array) variances associated with currently registered outcome_label

    References (informal list):
        DerSimonian, R., & Laird, N. (1986). Meta-analysis in clinical trials. Controlled clinical trials, 7(3), 177-188

        Lipsey, M. W., & Wilson, D. B. (2001). Practical meta-analysis. SAGE publications, Inc.

        Washington State Institute for Public Policy. (December 2018). Benefit-cost technical documentation.
            Olympia, WA

        Borenstein, M., Higgins, J. P., Hedges, L. V., & Rothstein, H. R. (2017).
            Basics of meta‐analysis: I2 is not an absolute measure of heterogeneity.
            Research synthesis methods, 8(1), 5-18.
    """

    def __init__(self, studies, outcome_label=''):
        """
        :param studies: (list) collection containing studies
        :param outcome_label: (str) type of outcome to use on initialization
        """
        assert len(studies) >= 2, 'studies must be a list of length >= 2'
        assert all(isinstance(x, Study) for x in studies), \
            'studies can only contain object of type Study'

        self.studies = studies
        self.outcome_label = outcome_label
        self.effect_sizes = np.array([])
        self.variances = np.array([])
        if outcome_label:
            self.set_outcome(outcome_label)
        else:
            print('Warning: outcome_label not set. Set outcome_label with StudyPool.set_outcome() method.')

    def append_study(self, study):
        """ Add study to study pool.

        :param study: (Study) study to be added
        :return: None
        """
        assert isinstance(study, Study), 'Argument outcome must be of type Study'
        self.studies.append(study)

    def remove_study(self, citation):
        study_pool = self.copy()
        for study in study_pool.studies:
            if study.citation == citation:
                study_pool.studies.remove(study)
                study_pool.set_outcome('' + self.outcome_label)
                return study
        raise ValueError('Outcome ID not found')

    def set_outcome(self, outcome_label):
        """ Register outcome type for meta-analysis. Only one outcome type can
            be registered at a time. All class operations are performed on the registered
            outcome type.

        :param outcome_label: (str) type of outcome
        :param inplace: (bool) whether to set the outcome in place, or to return a new StudyPool
        :return: (StudyPool) if inplace=True, return StudyPool with outcome_label registered
        """
        effect_sizes = []
        variances = []
        try:
            for study in self.studies:
                for outcome in study.outcomes:
                    if outcome.label == outcome_label:
                        effect_sizes.append(outcome.effect_size)
                        variances.append(outcome.variance)
            self.outcome_label = outcome_label
            self.effect_sizes = np.array(effect_sizes)
            self.variances = np.array(variances)
        except ReferenceError:
            # TODO: set up logger, make error the right error to except
            raise Exception('outcome label not found')

    def meta_analysis(self, method='auto'):
        """ Perform meta-analysis.

        :param method: (str) random effects meta-analysis if 're', fixed effects meta-analysis if 'fe',
                        base choice on statistical significance (p<0.05) of Q statistic if 'auto'
        :return: (float, float) weighted mean effect size, variance of effect size
        """
        # if method is auto, test for heterogeneity
        # use random effects if heterogeneity is present
        if method == 'auto':
            _, _, p = self.calculate_q()
            if p < 0.05:
                method = 're'
            else:
                method = 'fe'
        # if method is random effects, add between-study heterogeneity
        # otherwise return estimate that assumes homogeneous population effect size
        meta_effect_size = self.calculate_ivw_effect_size(method=method)
        meta_variance = self.calculate_variance(method=method)
        return meta_effect_size, meta_variance

    def calculate_ivw_effect_size(self, method='fe'):
        """ Calculate inverse variance weighted mean effect size.

        :param method: (str) random effects effect size if 're', fixed effects effect size if 'fe'
        :return: (float) weighted mean effect size
        """
        variances = self.variances
        # if method is random effects, add between-study heterogeneity
        if method == 're':
            variances = self.variances + self.calculate_re()
        ivw = 1 / variances
        sum_ivw_d = np.dot(ivw, self.effect_sizes)
        sum_ivw = ivw.sum()
        weighted_mean_effect_size = sum_ivw_d / sum_ivw
        return weighted_mean_effect_size

    def calculate_variance(self, method='fe'):
        """ Calculate variance of weighted mean effect size.

        :param method: random effects variance estimate if 're', fixed effects variance estimate if 'fe'
        :return: variance of effect size
        """
        variances = self.variances
        # if method is random effects, add between-study heterogeneity
        if method == 're':
            variances = variances + self.calculate_re()
        total_variance = 1 / (1 / variances).sum()
        return total_variance

    def calculate_q(self):
        """ Calculate Q statistic to test dispersion around the weighted mean effect size.
            Q is defined as the sum of squared standardized effect sizes. This method uses
            a rearranged form of the equation that facilitates computation.
            Q is asymptotically distributed chi-square with k-1 degrees of freedom.

        :return: (float, int, float) Q statistic, Q-stat degrees of freedom, p-value from one-sided chi-square test
        """
        ivw = 1 / self.variances
        square_es = np.square(self.effect_sizes)
        # q is distributed chi-square with k-1 degrees of freedom
        q = np.dot(ivw, square_es) - np.dot(ivw, square_es) / ivw.sum()
        dof = self.effect_sizes.size - 1
        # one sided chi-square test
        p = 1 - chi2.cdf(q, dof)
        return q, dof, p

    def calculate_re(self):
        """ Calculate tau-square, the random effect portion of the variance estimate used
            in random effects meta-analysis. Tau-square can be interpreted as the between-study
            variance, or between-study heterogeneity, which is ignored in fixed effects meta-analysis.

        :return:
        """
        # calculate using  DerSimonian-Laird (DL) approach (based on MM)
        q, dof, _ = self.calculate_q()
        ivw_fe = 1 / self.variances
        sum_ivw_fe = ivw_fe.sum()
        sum_ivw_fe_square = np.square(ivw_fe).sum()
        tau_square = (q - dof) / (sum_ivw_fe - sum_ivw_fe_square / sum_ivw_fe)
        if tau_square <= 0:
            return 0
        return tau_square

    def calculate_i_square(self):
        """ Calculate I-square, an estimate of the proportion of the total variance that is between-study variance.
            I-square is calculated as tau-square / (tau-square + sigma_square), where tau-square is
            between-study variance and sigma-square is within-study variance from sampling error.

        :return: I-square, the proportion of the total variance that is between-study variance
        """
        q, dof, _ = self.calculate_q()
        i_square = (q - dof) / q
        return i_square

    def copy(self, full=True):
        """ Create a copy of StudyPool

        :param full: (bool) If full=true, copy outcome_label, effect_sizes, and variances in addition to studies list.
        :return:
        """
        if full:
            return copy.deepcopy(self)
        studies = copy.deepcopy(self.studies)
        cpy = StudyPool(studies)
        return cpy

    def __repr__(self):
        result = 'Study pool containing: '
        for study in self.studies:
            result += '\n' + '\t' + str(study)
        return result

