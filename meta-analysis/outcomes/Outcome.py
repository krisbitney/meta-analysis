import copy


class Outcome:
    """ An outcome of a research study.

    Attributes:
        label (str) type of outcome
        treat_n (int) sample size of treatment group
        control_n (int) sample size of control group
        effect size (float) standardized mean difference or approximation
        variance (float) variance of effect size
        note (str) space for researcher notes
        method (str) estimation method
        id (int) unique id assigned to this outcome instance

    Global variables:
        _outcome_id_tracker (int) facilitates assignment of unique id to each Outcome instance
    """

    _outcome_id_tracker = 0

    def __init__(self, label, treat_n, control_n, effect_size=0.0, variance=float('inf'), note=''):
        self.label = label
        self.treat_n = treat_n
        self.control_n = control_n
        self.effect_size = effect_size
        self.variance = variance
        self.note = note
        self.method = 'custom'

        self.id = 0 + Outcome._outcome_id_tracker
        Outcome._outcome_id_tracker += 1

    def set_label(self, label):
        self.label = label

    def get_label(self):
        return self.label

    def set_n(self, treat_n, control_n):
        self.treat_n = treat_n
        self.control_n = control_n

    def get_n(self):
        return self.treat_n, self.control_n

    def set_estimate(self, effect_size, variance):
        self.effect_size = effect_size
        self.variance = variance

    def get_estimate(self):
        return self.effect_size, self.variance

    def set_note(self, note):
        self.note = note

    def get_note(self):
        return self.note

    def copy(self):
        """ Create a copy of class instance

        :param None
        :return: deep copy of calling instance
        """
        return copy.deepcopy(self)

    def __repr__(self):
        return f'Outcome(id={self.id}, Outcome={self.label}, Method={self.method}, ' \
            f'ES={self.effect_size:.4f}, Variance={self.variance:.4f})'

    def __str__(self):
        return f'id={self.id}, Outcome={self.label}, Method={self.method}, ' \
            f'ES={self.effect_size:.4f}, Variance={self.variance:.4f}'

    def __add__(self, other):
        """ Outcome addition is being defined as an approach to
            combine two outcomes, not as a way of adding random variables.
            Outcomes are combined by producing an inverse variance weighted
            mean effect size, the variance of that effect size, and the addition
            of the two sample sizes. This approach to addition makes sense in
            the theory of meta-analysis, and can be used as a rudimentary
            approach to handling dependent outcomes (i.e. combine them into one
            effect size prior to using them in the meta-analysis).

        :param other: another Outcome of same outcome type (e.g. both "crime" or both "education" outcomes)
        :return: combined outcome
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        elif self.label != other.label:
            return NotImplemented
        else:
            label = self.label
            effect_size = (self.effect_size*(1/self.variance) + other.effect_size*(1/other.variance)) / \
                          (self.variance + other.variance)
            variance = self.variance + other.variance
            treat_n = self.treat_n + other.treat_n
            control_n = self.control_n + other.control_n
            return Outcome(label, treat_n, control_n, effect_size, variance)

    def __eq__(self, other):
        if isinstance(other, Outcome):
            return self.label == other.label and \
                   self.effect_size == other.effect_size and \
                   self.variance == other.variance and \
                   self.treat_n == other.treat_n and \
                   self.control_n == other.control_n
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __hash__(self):
        return hash((self.label, self.treat_n, self.control_n, self.effect_size, self.variance, self.id))
