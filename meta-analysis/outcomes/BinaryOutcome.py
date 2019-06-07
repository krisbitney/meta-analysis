from .Outcome import Outcome
import math


class BinaryOutcome(Outcome):
    """ A binary outcome of a research study.

    Attributes:
        label (str) type of outcome
        treat_n (int) sample size of treatment group
        control_n (int) sample size of control group
        effect size (float) standardized mean difference or approximation
        variance (float) variance of effect size
        note (str) space for researcher notes
        method (str) estimation method
        id (int) unique id assigned to this outcome instance

        treat_post (float) percent "successes" of treatment group in post period
        control_post (float) percent "successes" of control group in post period
        treat_pre (float) percent "successes" of treatment group in pre period
        control_pre (float) percent "successes" of control group in pre period

    References (informal list):
        Lipsey, M. W., & Wilson, D. B. (2001). Practical meta-analysis. SAGE publications, Inc.

        http://www.campbellcollaboration.org/images/pdf/plain-language/Calculating_Effect_Sizes_Wilson_2013.pdf

        https://www.meta-analysis.com/downloads/Meta-analysis%20Converting%20among%20effect%20sizes.pdf

        Sánchez-Meca, J., Marín-Martínez, F., & Chacón-Moscoso, S. (2003). Effect-size indices for
            dichotomized outcomes in meta-analysis. Psychological methods, 8(4), 448.

        Washington State Institute for Public Policy. (December 2018). Benefit-cost technical documentation.
            Olympia, WA
    """

    def __init__(self, label, treat_n, control_n, treat_post, control_post, treat_pre=None, control_pre=None):
        super().__init__(label, treat_n, control_n)
        self.treat_post = treat_post
        self.control_post = control_post
        self.treat_pre = treat_pre
        self.control_pre = control_pre

    def estimate(self, use_pre=False):
        """ Calculates and updates effect size and variance. This is always inplace.

            Args:
                use_pre (bool) use gains scores if pre-period is available
            Returns:
                effect_size (float) Approximation of standardized mean difference
                variance (float) Variance of effect size estimate
        """
        # construct effect size
        logit = self.make_logit(self.treat_post, self.control_post)
        effect_size = self.transform_logit(logit)
        # construct variance
        variance = self.calculate_variance(self.treat_post, self.control_post)
        # track estimation method
        self.method = 'logit_post'
        # calculate effect size using gains scores if use_pre=True
        if use_pre:
            try:
                pre_logit = self.make_logit(self.treat_pre, self.control_pre)
                effect_size -= self.transform_logit(pre_logit)
                variance += self.calculate_variance(self.treat_pre, self.control_pre)
                # track estimation method
                self.method = 'logit_gains'
            except ReferenceError:
                # TODO: set up logger, make error the right error to except
                raise Exception('Pre-period scores not found or incomplete.')
        # store effect size and variance calculations
        self.effect_size = effect_size
        self.variance = variance

    def transform_logit(self, logit):
        """ Transforms logit to standardized mean difference approximation
            by dividing by standard deviation.

            Args:
                logit (float) log odds; random variable with logistic distribution
            Returns:
                corrected_d (float) SMD approximation from logit
        """
        # transform logit to have unit variance
        d = logit / (math.pi/math.sqrt(3))
        # apply finite sample bias correction for small samples
        adjustment = 1 - 3 / (4 * (self.treat_n + self.control_n) - 9)
        corrected_d = d * adjustment
        return corrected_d

    def make_logit(self, treat_p, control_p):
        """ Calculates log odds, a random variable with logistic distribution

            Args:
                treat_p (float) treatment group percent "successes"
                control_p (float) control group percent "successes"
            Returns:
                logit (float) log odds
        """
        odds_numerator = treat_p*(1-control_p)
        odds_denominator = control_p*(1-treat_p)
        log_odds = math.log(odds_numerator/odds_denominator)
        return log_odds

    def calculate_variance(self, treat_p, control_p):
        """ Calculates binary outcome effect size variance

           Args:
               treat_p (float) treatment group percent "successes"
               control_p (float) control group percent "successes"
           Returns:
               variance_d (float) variance of logit-based effect size estimate
        """

        o1 = 1 / treat_p
        o2 = 1 / (1 - treat_p)
        o3 = 1 / control_p
        o4 = 1 / (1 - control_p)
        variance_logit = o1 + o2 + o3 + o4
        variance_d = variance_logit / (math.pi**2 / 3)
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