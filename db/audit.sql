-- Execute with a DBA account after db/schema.sql creates ACEU.SCORES.
CREATE AUDIT POLICY aceu_score_read_policy ACTIONS SELECT ON aceu.scores;
AUDIT POLICY aceu_score_read_policy;
