def score(profile: dict) -> dict:
    signals = profile.get('credibility_signals', [])
    if not signals: return {'value': .5, 'uncertainty': .5, 'verified': 0, 'inferred': 0}
    verified = [float(x['strength']) for x in signals if x.get('status') == 'verified']
    inferred = [float(x['strength']) for x in signals if x.get('status') == 'inferred']
    value = (sum(verified)+.5*sum(inferred))/(len(verified)+.5*len(inferred)) if verified or inferred else .5
    value = max(0., min(1., value*float(profile.get('context_relevance', 1.))))
    uncertainty = min(1., .1+.2*len(inferred)/len(signals)+.15/len(signals))
    return {'value': value, 'uncertainty': uncertainty, 'verified': len(verified), 'inferred': len(inferred)}
