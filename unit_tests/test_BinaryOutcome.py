from outcomes.BinaryOutcome import BinaryOutcome
import math


def test_init():
    outcome1 = BinaryOutcome('hi', 10, 15, 0.5, 0.4, treat_pre=0.4, control_pre=0.4)

    assert outcome1.label == 'hi'
    assert outcome1.treat_n == 10
    assert outcome1.control_n == 15
    assert outcome1.treat_post == 0.5
    assert outcome1.control_post == 0.4
    assert outcome1.treat_pre == 0.4
    assert outcome1.control_pre == 0.4


def test_make_logit():
    outcome1 = BinaryOutcome('hi', 10, 15, 0.5, 0.4, treat_pre=0.4, control_pre=0.4)
    assert math.isclose(outcome1.make_logit(0.7, 0.3), 0.847297860387204, rel_tol=1e6)
    assert math.isclose(outcome1.make_logit(0.4, 0.5), -0.405465108108164, rel_tol=1e6)


def test_transform_logit():
    outcome1 = BinaryOutcome('hi', 10, 15, 0.5, 0.4, treat_pre=0.4, control_pre=0.4)
    logit1 = outcome1.make_logit(0.7, 0.3)
    logit2 = outcome1.make_logit(0.05, 0.5)
    assert math.isclose(outcome1.transform_logit(logit1), 0.44740149232839, rel_tol=1e6)
    assert math.isclose(outcome1.transform_logit(logit2), -1.5547618552311, rel_tol=1e6)


def test_calculate_variance():
    # This is directly tested in the test_estimate() method
    pass


def test_estimate():
    # treat improves, control remains same
    outcome1 = BinaryOutcome('hi', 10, 15, 0.5, 0.4, treat_pre=0.4, control_pre=0.4)
    outcome1.estimate(use_pre=True)
    # no improvement
    outcome2 = BinaryOutcome('hi', 10, 15, 0.4, 0.4, treat_pre=0.4, control_pre=0.4)
    outcome2.estimate(use_pre=True)
    # both treat and control improve
    outcome3 = BinaryOutcome('hi', 10, 15, 0.5, 0.4, treat_pre=0.4, control_pre=0.2)
    outcome3.estimate(use_pre=True)
    # treat improves, control worsens
    outcome4 = BinaryOutcome('hi', 10, 15, 0.5, 0.4, treat_pre=0.4, control_pre=0.5)
    outcome4.estimate(use_pre=True)
    # post only treat > post
    outcome5 = BinaryOutcome('hi', 10, 15, 0.5, 0.4)
    outcome5.estimate()
    # post only treat < post
    outcome6 = BinaryOutcome('hi', 10, 15, 0.4, 0.5)
    outcome6.estimate()
    # pathological outcome
    outcome7 = BinaryOutcome('hi', 2, 1, 0.99, 0.01, treat_pre=0.01, control_pre=0.99)
    outcome7.estimate(use_pre=True)

    assert math.isclose(outcome1.effect_size, 0.214099082431041, rel_tol=1e6)
    assert math.isclose(outcome1.variance, 5.01539859029572, rel_tol=1e6)

    assert math.isclose(outcome2.effect_size, 0, rel_tol=1e6)
    assert math.isclose(outcome2.variance, 5.06605918211689, rel_tol=1e6)

    assert math.isclose(outcome3.effect_size, -0.303811432905619, rel_tol=1e6)
    assert math.isclose(outcome3.variance, 5.64865598806033, rel_tol=1e6)

    assert math.isclose(outcome4.effect_size, 0.428198164862082, rel_tol=1e6)
    assert math.isclose(outcome4.variance, 4.96473799847455, rel_tol=1e6)

    assert math.isclose(outcome5.effect_size, 0.214099082431041, rel_tol=1e6)
    assert math.isclose(outcome5.variance, 2.48236899923728, rel_tol=1e6)

    assert math.isclose(outcome6.effect_size, -0.214099082431041, rel_tol=1e6)
    assert math.isclose(outcome6.variance, 2.48236899923728, rel_tol=1e6)

    assert math.isclose(outcome7.effect_size, 5.79067966012675, rel_tol=1e6)
    assert math.isclose(outcome7.variance, 122.813555930106, rel_tol=1e6)


def test_eq():
    outcome1 = BinaryOutcome('hi', 10, 15, 0.5, 0.4, treat_pre=0.4, control_pre=0.4)
    outcome1.estimate(use_pre='true')
    outcome2 = BinaryOutcome('hi', 10, 15, 0.5, 0.4, treat_pre=0.4, control_pre=0.4)
    outcome2.estimate(use_pre='true')
    outcome3 = BinaryOutcome('hi', 10, 15, 0.5, 0.4)
    outcome3.estimate()

    assert outcome1 == outcome2
    assert outcome1 != outcome3
