# ACE-U framework

The paper presents ACE-U as a conceptual, four-dimensional representation; this repository implements its Section VI reference architecture and evaluation pathway on synthetic data only. All signal weights and definitions are configurable by context.

| Dimension | Paper framing | Example signals in this implementation |
|---|---|---|
| Authenticity | Coherence between expressed identity and observable work over time | Skill and role consistency, overlap of stated skills with authored artifact skills; unsupported shifts are flagged for human review |
| Credibility | Contextual competence and reliability, distinguishing verified and inferred evidence | Verified credential/contribution strengths, inferred endorsements, contextual relevance and uncertainty |
| Empathy | Orientation toward peers and community | Interaction quality, reciprocity and diversity of interaction types; raw counts are not a proxy |
| Uniqueness | Contextual differentiation, bounded by trust | Skill-combination rarity and complementarity; gated by authenticity, credibility and empathy |

## Interactions and governance

The dimensions are a vector with per-dimension uncertainty, not a fixed claim about a person. High uniqueness alone does not earn a benefit: it is gated by A, C and E. Context changes weights and signal definitions. The sample ranking balances relevance, trust alignment and diversity, and provides a relevance-only credibility baseline for comparison. Credibility-only comparisons are intentionally explicit in the evaluation harness.

Consent precedes inclusion; scores are auditable, and people can contest or correct inferred signals and request overrides. Unsupported shifts require human review. Keep collection purpose-limited, expose explanations, retain uncertainty, audit feature distributions, and avoid treating unequal visibility or online participation as a lack of trustworthiness. These are design safeguards for this reference implementation, not evidence that the framework prevents bias.

## Section VI pathway implemented

The data ingestion layer reads only generated fixtures. Feature extraction is implemented by `aceu/signals/`; ACE-U estimation and explanations are in `aceu/scoring.py`; application ranking and offline evaluation are in `aceu/rank.py` and `eval/run.py`. The paper proposes human annotation and field or qualitative studies; these are not performed here. No empirical validation is claimed.
