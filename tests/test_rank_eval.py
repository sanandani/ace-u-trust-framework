from aceu.rank import rank
from eval.run import run

def test_baseline_uses_credibility_only():
    rows=[{'id':'a','relevance':.2,'credibility':.9,'trust':0},{'id':'b','relevance':.9,'credibility':.1,'trust':1}]
    assert rank(rows,baseline=True)[0]['id']=='b'

def test_evaluation_writes_synthetic_report():
    path=run(); report=path.read_text()
    assert 'synthetic data only' in report and 'not empirical validation' in report and 'Credibility-only baseline' in report
