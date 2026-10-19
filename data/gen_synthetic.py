"""Seeded deterministic fixture generator. Contains no real profiles."""
import json, random
from pathlib import Path

SKILLS = ['python','sql','security','design','mentoring','ml','cloud','writing','testing','governance']
def generate(seed: int = 2026, count: int = 80) -> list[dict]:
    rng = random.Random(seed)
    rows=[]
    for i in range(count):
        skills=rng.sample(SKILLS, k=rng.randint(2,5))
        prior=skills.copy() if i%3 else rng.sample(SKILLS,k=rng.randint(1,3))
        signals=[{'status':'verified','strength':round(rng.uniform(.55,1),3)} for _ in range(rng.randint(0,2))]
        signals += [{'status':'inferred','strength':round(rng.uniform(.3,.9),3)} for _ in range(rng.randint(0,3))]
        interactions=[{'quality':round(rng.random(),3),'reciprocity':round(rng.random(),3),'type':rng.choice(['feedback','mentoring','recognition','collaboration'])} for _ in range(rng.randint(1,7))]
        rows.append({'id':f'synth-{i:03}','skills':skills,'prior_skills':prior,'roles':['contributor'],'prior_roles':['contributor'], 'history':['synthetic'], 'authored_skills':rng.sample(skills,k=rng.randint(0,len(skills))), 'credibility_signals':signals, 'context_relevance':round(rng.uniform(.5,1),3), 'interactions':interactions, 'rarity':round(rng.random(),3), 'complementarity':round(rng.random(),3), 'unsupported_shift': i%19==0, 'relevance':round(rng.random(),3), 'diversity':round(rng.random(),3), 'rater_score':round(rng.random(),3)})
    return rows
if __name__=='__main__':
    path=Path(__file__).with_name('synthetic_profiles.json')
    path.write_text(json.dumps(generate(),indent=2)+'\n')
    print(f'Wrote {path} (seed=2026, synthetic only)')
