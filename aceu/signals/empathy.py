def score(profile: dict) -> dict:
    interactions = profile.get('interactions', [])
    if not interactions: return {'value': .5, 'uncertainty': .5}
    q = sum(float(i.get('quality', 0)) for i in interactions)/len(interactions)
    r = sum(float(i.get('reciprocity', 0)) for i in interactions)/len(interactions)
    d = len({i.get('type', 'unknown') for i in interactions})/max(1, int(profile.get('interaction_type_space', 4)))
    return {'value': max(0., min(1., .45*q+.35*r+.20*min(1., d))), 'uncertainty': min(.5, .3/len(interactions))}
