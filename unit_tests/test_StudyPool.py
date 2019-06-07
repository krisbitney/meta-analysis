from StudyPool import StudyPool
from Study import Study
from outcomes.Outcome import Outcome
import math


def test_set_outcome():
    outcome1 = Outcome('education', 30, 30, effect_size=0.1, variance=0.02)
    outcome2 = Outcome('education', 25, 25, effect_size=0.1, variance=0.02)
    outcome3 = Outcome('crime', 25, 25, effect_size=0.1, variance=0.02)
    study1 = Study("hello", "Kris et al 2019", outcomes=[outcome1, outcome2, outcome3])
    outcome4 = Outcome('education', 30, 30, effect_size=0.1, variance=0.02)
    outcome5 = Outcome('crime', 25, 25, effect_size=0.1, variance=0.02)
    outcome6 = Outcome('crime', 25, 25, effect_size=0.1, variance=0.02)
    outcome7 = Outcome('crime', 25, 25, effect_size=0.1, variance=0.02)
    study2 = Study("hello", "Kris et al 2018", outcomes=[outcome4, outcome5, outcome6, outcome7])

    studies = StudyPool([study1, study2], outcome_label='education')
    assert studies.outcome_label == 'education'
    assert len(studies.effect_sizes) == 3

    studies.set_outcome('crime')
    assert studies.outcome_label == 'crime'
    assert len(studies.effect_sizes) == 4


def test_calculate_q():
    outcome1 = Outcome('crime', 25, 25, effect_size=0.1, variance=0.02)
    outcome2 = Outcome('crime', 25, 25, effect_size=0.17, variance=0.03)
    study1 = Study("hello", "Kris et al 2019", outcomes=[outcome1, outcome2])
    outcome3 = Outcome('crime', 25, 25, effect_size=0.2, variance=0.01)
    outcome4 = Outcome('crime', 25, 25, effect_size=0.3, variance=0.025)
    outcome5 = Outcome('crime', 25, 25, effect_size=0.5, variance=0.035)
    study2 = Study("hello", "Kris et al 2018", outcomes=[outcome3, outcome4, outcome5])

    study_pool = StudyPool([study1, study2], outcome_label='crime')
    q, dof, p = study_pool.calculate_q()
    assert math.isclose(q, 16.1418558826177, rel_tol=1e6)
    assert dof == 4
    assert math.isclose(p, 0.00283460303776, rel_tol=1e6)


def test_calculate_re():
    outcome1 = Outcome('crime', 25, 25, effect_size=0.1, variance=0.02)
    outcome2 = Outcome('crime', 25, 25, effect_size=0.17, variance=0.03)
    study1 = Study("hello", "Kris et al 2019", outcomes=[outcome1, outcome2])
    outcome3 = Outcome('crime', 25, 25, effect_size=0.2, variance=0.01)
    outcome4 = Outcome('crime', 25, 25, effect_size=0.3, variance=0.025)
    outcome5 = Outcome('crime', 25, 25, effect_size=0.5, variance=0.035)
    study2 = Study("hello", "Kris et al 2018", outcomes=[outcome3, outcome4, outcome5])

    study_pool = StudyPool([study1, study2], outcome_label='crime')
    tau_square = study_pool.calculate_re()
    assert math.isclose(tau_square, 0.064488371103462, rel_tol=1e6)


def test_calculate_ivw_effect_size():
    outcome1 = Outcome('crime', 25, 25, effect_size=0.1, variance=0.02)
    outcome2 = Outcome('crime', 25, 25, effect_size=0.17, variance=0.03)
    study1 = Study("hello", "Kris et al 2019", outcomes=[outcome1, outcome2])
    outcome3 = Outcome('crime', 25, 25, effect_size=0.2, variance=0.01)
    outcome4 = Outcome('crime', 25, 25, effect_size=0.3, variance=0.025)
    outcome5 = Outcome('crime', 25, 25, effect_size=0.5, variance=0.035)
    study2 = Study("hello", "Kris et al 2018", outcomes=[outcome3, outcome4, outcome5])

    study_pool = StudyPool([study1, study2], outcome_label='crime')
    fe_effect_size = study_pool.calculate_ivw_effect_size(method='fe')
    re_effect_size = study_pool.calculate_ivw_effect_size(method='re')
    assert math.isclose(fe_effect_size, 0.226086956521739, rel_tol=1e6)
    assert math.isclose(re_effect_size, 0.246115055719316, rel_tol=1e6)


def test_calculate_variance():
    outcome1 = Outcome('crime', 25, 25, effect_size=0.1, variance=0.02)
    outcome2 = Outcome('crime', 25, 25, effect_size=0.17, variance=0.03)
    study1 = Study("hello", "Kris et al 2019", outcomes=[outcome1, outcome2])
    outcome3 = Outcome('crime', 25, 25, effect_size=0.2, variance=0.01)
    outcome4 = Outcome('crime', 25, 25, effect_size=0.3, variance=0.025)
    outcome5 = Outcome('crime', 25, 25, effect_size=0.5, variance=0.035)
    study2 = Study("hello", "Kris et al 2018", outcomes=[outcome3, outcome4, outcome5])

    study_pool = StudyPool([study1, study2], outcome_label='crime')
    fe_variance = study_pool.calculate_variance(method='fe')
    re_variance = study_pool.calculate_variance(method='re')
    assert math.isclose(fe_variance, 0.003969754253308, rel_tol=1e6)
    assert math.isclose(re_variance, 0.017522267928502, rel_tol=1e6)


def test_meta_analysis():
    outcome1 = Outcome('crime', 25, 25, effect_size=0.1, variance=0.02)
    outcome2 = Outcome('crime', 25, 25, effect_size=0.17, variance=0.03)
    study1 = Study("hello", "Kris et al 2019", outcomes=[outcome1, outcome2])
    outcome3 = Outcome('crime', 25, 25, effect_size=0.2, variance=0.01)
    outcome4 = Outcome('crime', 25, 25, effect_size=0.3, variance=0.025)
    outcome5 = Outcome('crime', 25, 25, effect_size=0.5, variance=0.035)
    study2 = Study("hello", "Kris et al 2018", outcomes=[outcome3, outcome4, outcome5])

    study_pool = StudyPool([study1, study2], outcome_label='crime')
    fe_effect_size = study_pool.calculate_ivw_effect_size(method='fe')
    re_effect_size = study_pool.calculate_ivw_effect_size(method='re')
    fe_variance = study_pool.calculate_variance(method='fe')
    re_variance = study_pool.calculate_variance(method='re')

    meta_es_fe, meta_var_fe = study_pool.meta_analysis(method='fe')
    meta_es_re, meta_var_re = study_pool.meta_analysis(method='re')
    meta_es_auto, meta_var_auto = study_pool.meta_analysis(method='auto')

    assert math.isclose(fe_effect_size, meta_es_fe)
    assert math.isclose(re_effect_size, meta_es_re)
    assert math.isclose(re_effect_size, meta_es_auto)
    assert math.isclose(fe_variance, meta_var_fe)
    assert math.isclose(re_variance, meta_var_re)
    assert math.isclose(re_variance, meta_var_auto)
