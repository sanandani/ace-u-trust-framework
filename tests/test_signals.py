import pytest
from aceu.signals import authenticity, credibility, empathy, uniqueness
from aceu.scoring import score

@pytest.mark.parametrize('fn,profile',[(authenticity.score,{}),(credibility.score,{}),(empathy.score,{})])
def test_empty_signal_edges_are_bounded(fn,profile):
    result=fn(profile); assert 0 <= result['value'] <= 1 and 0 <= result['uncertainty'] <= 1

def test_authenticity_flags_unsupported_shift():
    assert authenticity.score({'unsupported_shift':True})['flags']

def test_authenticity_consistency_and_artifact_overlap():
    p={'skills':['python','sql'],'prior_skills':['python','sql'],'roles':['dev'],'prior_roles':['dev'],'authored_skills':['python']}
    assert authenticity.score(p)['value'] == pytest.approx(.85)

def test_credibility_separates_verified_inferred_and_context():
    r=credibility.score({'credibility_signals':[{'status':'verified','strength':1},{'status':'inferred','strength':1}], 'context_relevance':.5})
    assert r['verified']==1 and r['inferred']==1 and r['value']==pytest.approx(.5)

def test_empathy_uses_quality_reciprocity_and_diversity():
    a=empathy.score({'interactions':[{'quality':1,'reciprocity':1,'type':'feedback'}]})
    b=empathy.score({'interactions':[{'quality':0,'reciprocity':0,'type':'feedback'}]})
    assert a['value']>b['value']

def test_uniqueness_gate():
    dims={k:{'value':.2} for k in ['authenticity','credibility','empathy']}
    assert uniqueness.score({'rarity':1,'complementarity':1},dims)['value']==0

def test_scoring_explanation_uncertainty_and_weights():
    r=score({}, {'weights':{'A':1,'C':0,'E':0,'U':0}})
    assert set(r['vector'])=={'A','C','E','U'} and set(r['uncertainty'])==set(r['vector']) and r['explanation']
    assert r['score']==r['vector']['A']
