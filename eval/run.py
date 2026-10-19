"""Synthetic offline comparison; not empirical validation."""
import json, math, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from aceu.scoring import score
from aceu.rank import rank
from data.gen_synthetic import generate

def corr(a,b):
    n=len(a); ma=sum(a)/n; mb=sum(b)/n
    den=math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/den if den else 0.
def run():
    profiles=generate()
    candidates=[]
    for p in profiles:
        s=score(p)
        candidates.append({'id':p['id'],'relevance':p['relevance'],'trust':s['score'],'credibility':s['vector']['C'],'diversity':p['diversity'],'rater_score':p['rater_score']})
    ace=rank(candidates); base=rank(candidates,baseline=True)
    k=20
    def diversity(rows): return len({x['id'] for x in rows[:k] if float(x['diversity'])>.5})/k
    def correlation(rows): return round(corr([x['rank_score'] for x in rows],[x['rater_score'] for x in rows]),4)
    report=f'''# Synthetic offline evaluation (synthetic data only)\n\nThis is a reproducible simulation, not empirical validation and not evidence of real-world effectiveness. Dataset seed: 2026; profiles: {len(profiles)}. Top-k: {k}.\n\n| Ranking | Top-k diversity (fraction with synthetic diversity > 0.5) | Score/rater Pearson correlation |\n|---|---:|---:|\n| ACE-U multi-objective | {diversity(ace):.3f} | {correlation(ace):.4f} |\n| Credibility-only baseline | {diversity(base):.3f} | {correlation(base):.4f} |\n\nSynthetic rater scores are generated independently; metrics are illustrative harness outputs only.\n'''
    out=ROOT/'eval'/'REPORT.md'; out.write_text(report); return out
if __name__=='__main__': print(run())
