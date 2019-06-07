from outcomes.Outcome import Outcome
import copy


class Study:
    """ Defines a research study by holding effect size and variance
    values used for meta-analysis. Includes methods to help calculate
    effect size and variance.

    Attributes:
        note (str) text describing study
        citation (str) study citation
        _outcomes (dictionary) Outcomes from study

    """

    def __init__(self, note='', citation='', outcomes=None):
        """ Initialize Study

        :param note: (str) text describing study
        :param citation: (str) study citation
        :param outcome_list: (list) 1d iterable of outcomes with which to initialize study
        """
        self.note = note
        self.citation = citation
        self.outcomes = outcomes or []

    def append_outcome(self, outcome):
        assert isinstance(outcome, Outcome), 'Argument outcome must be of type Outcome'
        self.outcomes.append(outcome)

    def remove_outcome(self, outcome_id):
        study = self.copy()
        for outcome in study.outcomes:
            if outcome.id == outcome_id:
                study.outcomes.remove(outcome)
                return study
        raise ValueError('Outcome ID not found')

    def list_outcomes(self):
        for outcome in self.outcomes:
            print(outcome)

    def get_outcome_by_id(self, outcome_id):
        for outcome in self.outcomes:
            if outcome.id == outcome_id:
                return outcome
        return False

    def get_outcomes_by_label(self, label):
        return [outcome for outcome in self.outcomes if outcome.label == label]

    def set_note(self, note):
        self.note = note

    def get_note(self):
        return self.note

    def set_citation(self, citation):
        self.citation = citation

    def get_citation(self):
        return self.citation

    def copy(self):
        """ Create a copy of class instance

        :param None
        :return: deep copy of calling instance
        """
        return copy.deepcopy(self)

    def __repr__(self):
        return self.citation

    def __str__(self):
        return self.citation