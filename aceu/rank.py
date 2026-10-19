def rank(candidates: list[dict], context: dict | None = None, weights: dict | None = None, baseline: bool = False) -> list[dict]:
    weights = weights or {'relevance': .4, 'trust': .4, 'diversity': .2}
    out = []
    for source in candidates:
        item = dict(source)
        w = {'relevance': 1., 'trust': 0., 'diversity': 0.} if baseline else weights
        trust = item.get('credibility', .5) if baseline else item.get('trust', .5)
        total = sum(w.values()) or 1.
        item['rank_score'] = (w.get('relevance', 0)*item.get('relevance', 0)+w.get('trust', 0)*trust+w.get('diversity', 0)*item.get('diversity', .5))/total
        out.append(item)
    return sorted(out, key=lambda x: x['rank_score'], reverse=True)
