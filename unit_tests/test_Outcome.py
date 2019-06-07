from Outcome import Outcome


def test_init():
    outcome1 = Outcome('education', 30, 30, effect_size=0.1, variance=1.0)
    outcome2 = Outcome('education', 20, 25, effect_size=0.2, variance=2.0)

    assert isinstance(outcome1.id, int)
    assert isinstance(outcome2.id, int)
    assert outcome1.id != outcome2.id
    assert outcome2.id > outcome1.id

    outcome1 = Outcome('education', 40, 30, effect_size=0.1, variance=1.0)
    assert outcome1.id != outcome2.id
    assert outcome2.id < outcome1.id


def test_str():
    outcome = Outcome('education', 30, 30, effect_size=0.1, variance=1.0)
    assert str(outcome) == f'id={outcome.id}, Outcome=education, Method=custom, ES={0.1:.4f}, Variance={1.0:.4f}'


def test_add():
    outcome1 = Outcome('education', 30, 30, effect_size=0.1, variance=1.0)
    outcome2 = Outcome('education', 20, 25, effect_size=0.2, variance=2.0)
    outcome3 = outcome1 + outcome2
    assert outcome3.label == 'education'
    assert outcome3.effect_size == (0.1*(1/1.0) + 0.2*(1/2.0)) / (1.0 + 2.0)
    assert outcome3.variance == 3.0
    assert outcome3.treat_n == 50
    assert outcome3.control_n == 55


def test_eq():
    outcome1 = Outcome('education', 30, 30, effect_size=0.1, variance=1.0)
    outcome2 = Outcome('education', 30, 30, effect_size=0.1, variance=1.0)
    outcome3 = Outcome('education', 20, 25, effect_size=0.2, variance=2.0)
    assert outcome1 == outcome2
    assert not outcome1 == outcome3


def test_neq():
    outcome1 = Outcome('education', 30, 30, effect_size=0.1, variance=1.0)
    outcome2 = Outcome('education', 20, 25, effect_size=0.2, variance=2.0)
    outcome3 = Outcome('crime', 30, 30, effect_size=0.1, variance=1.0)
    outcome4 = Outcome('education', 30, 30, effect_size=0.1, variance=1.0)
    assert outcome1 != outcome2
    assert outcome1 != outcome3
    assert not outcome1 != outcome4

