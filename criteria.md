# Acceptance Criteria

These targets were written before the service was built.

## 1. At most 1 of 10 clearly human samples is labeled high-confidence AI in each trial.

**Why this target:** A false accusation harms a real writer, so the service
should prefer uncertainty over confidently flagging human work.

## 2. The average combined score for five clearly AI samples is at least 0.20 higher than for five clearly human samples.

**Why this target:** The two groups need a visible gap for the score to carry
more information than a simple guess.

## 3. All three label variants are reached at least once across 10 deliberately varied submissions.

**Why this target:** Human, unsure, and AI labels are only useful if every
configured range can actually occur.

## 4. Five of five valid appeals return success and create an `under_review` log entry containing the submitted reasoning.

**Why this target:** An appeal is the protection against a wrong accusation,
so every valid appeal must be traceable and must change status.

## 5. Five of five invalid submissions return a 4xx response without creating a decision entry.

**Why this target:** Missing, empty, non-text, or oversized input should fail
clearly instead of crashing or polluting the audit log.
