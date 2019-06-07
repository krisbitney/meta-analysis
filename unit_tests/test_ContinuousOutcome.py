from outcomes.ContinuousOutcome import ContinuousOutcome
import math


def test_init():
    outcome1 = ContinuousOutcome('hello', 30, 25, treat_post=8, control_post=7, treat_post_sd=2, control_post_sd=1,
                                 treat_pre=7, control_pre=6, treat_pre_sd=1.5, control_pre_sd=1.2)

    assert outcome1.label == 'hello'
    assert outcome1.treat_n == 30
    assert outcome1.control_n == 25
    assert outcome1.treat_post == 8
    assert outcome1.control_post == 7
    assert outcome1.treat_post_sd == 2
    assert outcome1.control_post_sd == 1
    assert outcome1.treat_pre == 7
    assert outcome1.control_pre == 6
    assert outcome1.treat_pre_sd == 1.5
    assert outcome1.control_pre_sd == 1.2


def test_calculate_pooled_sd():
    outcome1 = ContinuousOutcome('hello', 30, 25, treat_post=8, control_post=7, treat_post_sd=2, control_post_sd=1,
                                 treat_pre=7, control_pre=6, treat_pre_sd=1.5, control_pre_sd=1.2)

    assert math.isclose(outcome1.calculate_pooled_sd(2, 1), 1.625272110744, rel_tol=1e6)
    assert math.isclose(outcome1.calculate_pooled_sd(1.5, 1.2), 1.42093511596187, rel_tol=1e6)


def test_calculate_smd():
    outcome1 = ContinuousOutcome('hello', 30, 25, treat_post=8, control_post=7, treat_post_sd=2, control_post_sd=1,
                                 treat_pre=7, control_pre=6, treat_pre_sd=1.5, control_pre_sd=1.2)
    pooled_sd1 = outcome1.calculate_pooled_sd(2, 1)
    pooled_sd2 = outcome1.calculate_pooled_sd(1.5, 1.2)
    assert math.isclose(outcome1.calculate_smd(8, 7, pooled_sd1), 1.625272110744, rel_tol=1e6)
    assert math.isclose(outcome1.calculate_smd(7, 6, pooled_sd2), 1.42093511596187, rel_tol=1e6)


def test_calculate_variance():
    outcome1 = ContinuousOutcome('hello', 30, 25, treat_post=8, control_post=7, treat_post_sd=2, control_post_sd=1,
                                 treat_pre=7, control_pre=6, treat_pre_sd=1.5, control_pre_sd=1.2)
    pooled_sd1 = outcome1.calculate_pooled_sd(2, 1)
    es1 = outcome1.calculate_smd(8, 7, pooled_sd1)
    pooled_sd2 = outcome1.calculate_pooled_sd(1.5, 1.2)
    es2 = outcome1.calculate_smd(7, 6, pooled_sd2)

    assert math.isclose(outcome1.calculate_variance(es1), 0.076677723271016, rel_tol=1e6)
    assert math.isclose(outcome1.calculate_variance(es2), 0.077708761716434, rel_tol=1e6)


def test_estimate():
    outcome1 = ContinuousOutcome('hello', 30, 25, treat_post=10, control_post=8, treat_post_sd=2.1,
                                 control_post_sd=1.9, treat_pre=3, control_pre=4, treat_pre_sd=1.3,
                                 control_pre_sd=1.2)
    outcome1.estimate(use_pre=True)
    assert math.isclose(outcome1.effect_size, 1.73321673159002, rel_tol=1e6)
    assert math.isclose(outcome1.variance, 0.16055497274011, rel_tol=1e6)