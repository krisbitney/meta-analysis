from .Outcome import Outcome
import math


class ContinuousOutcome(Outcome):
    """ A continous outcome of a research study.

    Attributes:
        label (str) type of outcome
        treat_n (int) sample size of treatment group
        control_n (int) sample size of control group
        effect size (float) standardized mean difference or approximation
        variance (float) variance of effect size
        note (str) space for researcher notes
        method (str) estimation method
        id (int) unique id assigned to this outcome instance

        treat_post (float) outcome mean for treatment group in post period
        control_post (float) outcome mean for control group in post period
        treat_post_sd (float) outcome standard deviation for treatment group in post period
        control_post_sd (float) outcome standard deviation for control group in post period
        treat_pre (float) outcome mean for treatment group in pre period
        control_pre (float) outcome mean for control group in pre period
        treat_pre_sd (float) outcome standard deviation for treatment group in pre period
        control_pre_sd (float) outcome standard deviation for control group in pre period

    References (informal list):
        Lipsey, M. W., & Wilson, D. B. (2001). Practical meta-analysis. SAGE publications, Inc.

        http://www.campbellcollaboration.org/images/pdf/plain-language/Calculating_Effect_Sizes_Wilson_2013.pdf

        https://www.meta-analysis.com/downloads/Meta-analysis%20Converting%20among%20effect%20sizes.pdf

        Sánchez-Meca, J., Marín-Martínez, F., & Chacón-Moscoso, S. (2003). Effect-size indices for
            dichotomized outcomes in meta-analysis. Psychological methods, 8(4), 448.

        Washington State Institute for Public Policy. (December 2018). Benefit-cost technical documentation.
            Olympia, WA
    """

    def __init__(self, label, treat_n, control_n, treat_post, control_post,
                 treat_post_sd, control_post_sd,
                 treat_pre=None, control_pre=None,
                 treat_pre_sd=None, control_pre_sd=None):
        super().__init__(label, treat_n, control_n)
        self.treat_post = treat_post
        self.control_post = control_post
        self.treat_pre = treat_pre
        self.control_pre = control_pre
        self.treat_post_sd = treat_post_sd
        self.control_post_sd = control_post_sd
        self.treat_pre_sd = treat_pre_sd
        self.control_pre_sd = control_pre_sd

    def estimate(self, use_pre=False):
        """ Calculates and updates effect size and variance. This is always inplace.

            Args:
                use_pre (bool) use gains scores if pre-period is available
            Returns:
                effect_size (float) Approximation of standardized mean difference
                variance (float) Variance of effect size estimate
        """
        # calculate effect size as standardized mean difference
        post_pooled_sd = self.calculate_pooled_sd(self.treat_post_sd, self.control_post_sd)
        effect_size = self.calculate_smd(self.treat_post, self.control_post, post_pooled_sd)
        # construct variance
        variance = self.calculate_variance(effect_size)
        # track estimation method
        self.method = 'SMD_post'
        # calculate effect size using gains scores if use_pre=True
        if use_pre:
            try:
                pre_pooled_sd = self.calculate_pooled_sd(self.treat_pre_sd, self.control_pre_sd)
                pre_effect_size = self.calculate_smd(self.treat_pre, self.control_pre, pre_pooled_sd)
                effect_size -= pre_effect_size
                variance += self.calculate_variance(pre_effect_size)
                # track estimation method
                self.method = 'SMD_gains'
            except ReferenceError:
                # TODO: set up logger, make error the right error to except
                raise Exception('Pre-period scores not found or incomplete.')
        # store effect size and variance calculations
        self.effect_size = effect_size
        self.variance = variance

    def calculate_smd(self, treat_mean, control_mean, pooled_sd):
        """ Calculates standardized mean difference

            Args:
                treat_mean (float) treatment group mean
                control_mean (float) control group mean
                pooled_sd (float) pooled standard deviation of groups
            Returns:
                corrected_d (float) standardized mean difference
        """
        # calculate standardized mean difference
        d = (treat_mean - control_mean) / pooled_sd
        # apply finite sample bias correction for small samples
        adjustment = 1 - 3 / (4 * (self.treat_n + self.control_n) - 9)
        corrected_d = d * adjustment
        return corrected_d

    def calculate_pooled_sd(self, treat_sd, control_sd):
        """ Calculates pooled standard deviation

            Args:
                treat_sd (float) standard deviation of treatment group
                control_sd (float) standard deviation of control group
            Returns:
                pooled_sd (float) pooled standard deviation
        """
        term1 = (self.treat_n-1)*treat_sd**2
        term2 = (self.control_n-1)*control_sd**2
        term3 = self.treat_n + self.control_n - 2
        pooled_variance = (term1 + term2) / term3
        pooled_sd = math.sqrt(pooled_variance)
        return pooled_sd

    def calculate_variance(self, effect_size):
        """ Calculates continuous outcome effect size variance

           Args:
               effect size (float) standardized mean difference
           Returns:
               variance_d (float) variance of logit-based effect size estimate
        """
        term1 = self.treat_n + self.control_n / self.treat_n*self.control_n
        term2 = effect_size**2
        term3 = 2 * (self.treat_n + self.control_n)
        variance_d = term1 + (term2 / term3)
        return variance_d

    def set_post_mean(self, treat_post, control_post):
        self.treat_post = treat_post
        self.control_post = control_post

    def get_post_mean(self):
        return self.treat_post, self.control_post

    def set_pre_mean(self, treat_pre, control_pre):
        self.treat_pre = treat_pre
        self.control_pre = control_pre

    def get_pre_mean(self):
        return self.treat_pre, self.control_pre

    def set_post_sd(self, treat_post_sd, control_post_sd):
        self.treat_post_sd = treat_post_sd
        self.control_post_sd = control_post_sd

    def get_post_sd(self):
        return self.treat_post_sd, self.control_post_sd

    def set_pre_sd(self, treat_pre_sd, control_pre_sd):
        self.treat_pre = treat_pre_sd
        self.control_pre = control_pre_sd

    def get_pre_sd(self):
        return self.treat_pre_sd, self.control_pre_sd