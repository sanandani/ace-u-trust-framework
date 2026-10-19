def score(profile: dict) -> dict:
    skills, prior = set(profile.get('skills', [])), set(profile.get('prior_skills', []))
    roles, old_roles = set(profile.get('roles', [])), set(profile.get('prior_roles', []))
    def consistency(a, b): return len(a & b) / len(a | b) if a | b else 1.0
    authored = set(profile.get('authored_skills', []))
    overlap = len(skills & authored) / len(skills) if skills else 1.0
    value = max(0., min(1., .4*consistency(skills, prior)+.3*consistency(roles, old_roles)+.3*overlap))
    return {'value': value, 'uncertainty': .15 if profile.get('history') else .35, 'flags': ['unsupported profile shift; human review required'] if profile.get('unsupported_shift') else []}
