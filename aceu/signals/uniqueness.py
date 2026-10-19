def score(profile: dict, dimensions: dict, context: dict | None = None) -> dict:
    context = context or {}
    raw = .5*float(profile.get('rarity', .5))+.5*float(profile.get('complementarity', .5))
    gate = min(dimensions[k]['value'] for k in ('authenticity', 'credibility', 'empathy'))
    value = max(0., min(1., raw*gate)) if gate >= float(context.get('uniqueness_gate', .25)) else 0.
    return {'value': value, 'uncertainty': .25}
