from .signals import authenticity, credibility, empathy, uniqueness

def score(profile: dict, context: dict | None = None) -> dict:
    context = context or {}
    dims = {'A': authenticity.score(profile), 'C': credibility.score(profile), 'E': empathy.score(profile)}
    dims['U'] = uniqueness.score(profile, {'authenticity': dims['A'], 'credibility': dims['C'], 'empathy': dims['E']}, context)
    weights = context.get('weights', {'A': .25, 'C': .35, 'E': .25, 'U': .15})
    total = sum(max(0., float(weights.get(k, 0))) for k in dims) or 1.
    value = sum(dims[k]['value']*max(0., float(weights.get(k, 0))) for k in dims)/total
    return {'vector': {k: dims[k]['value'] for k in dims}, 'uncertainty': {k: dims[k]['uncertainty'] for k in dims}, 'score': value, 'explanation': '; '.join(f"{k}={dims[k]['value']:.2f} (±{dims[k]['uncertainty']:.2f})" for k in dims), 'flags': dims['A'].get('flags', [])}
