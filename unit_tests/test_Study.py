from Study import Study
from outcomes.Outcome import Outcome


def test_init_():
    outcome1 = Outcome('education', 10, 10)
    outcome2 = Outcome('education', 20, 20)
    study = Study("hello", "Kris et al 2019", outcomes=[outcome1, outcome2])
    assert study.note == 'hello'
    assert study.citation == 'Kris et al 2019'
    assert len(study.outcomes) == 2


def test_append_outcome():
    study = Study("hello", "Kris et al 2019")
    study.append_outcome(Outcome('education', 10, 10))
    assert len(study.outcomes) == 1
    assert isinstance(study.outcomes[0], Outcome)
    assert study.outcomes[0].treat_n == 10


def test_remove_outcome():
    outcome1 = Outcome('education', 30, 30)
    outcome2 = Outcome('education', 25, 25)
    outcome1_id = outcome1.id
    study = Study("hello", "Kris et al 2019", outcomes=[outcome1, outcome2])

    exists = False
    for outcome in study.outcomes:
        if outcome.id == outcome1_id:
            exists = True
    assert exists

    study = study.remove_outcome(outcome1_id)
    for outcome in study.outcomes:
        assert outcome.id != outcome1_id


def test_get_outcome_by_id():
    outcome1 = Outcome('education', 30, 30)
    outcome2 = Outcome('education', 25, 25)
    outcome1_id = outcome1.id
    outcome2_id = outcome2.id
    study = Study("hello", "Kris et al 2019", outcomes=[outcome1, outcome2])

    outcome_pull1 = study.get_outcome_by_id(outcome1_id)
    assert outcome_pull1 == outcome1
    outcome_pull2 = study.get_outcome_by_id(outcome2_id)
    assert outcome_pull2 == outcome2
    assert outcome_pull1 != outcome_pull2


def test_get_outcomes_by_label():
    outcome1 = Outcome('education', 30, 30)
    outcome2 = Outcome('education', 25, 25)
    outcome3 = Outcome('crime', 25, 25)
    study = Study("hello", "Kris et al 2019", outcomes=[outcome1, outcome2, outcome3])
    edu_outcome_list = study.get_outcomes_by_label('education')
    assert len(edu_outcome_list) == 2
    for outcome in edu_outcome_list:
        assert outcome.label == 'education'