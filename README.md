# Provenance Guard

## What This Does

1. `POST /submit` validates the text and creator ID.
2. `detector.py` measures how predictable the text is.
3. `stylometry.py` measures sentence spread, vocabulary, and punctuation.
4. `scoring.py::combine_signals` combines both scores.
5. `scoring.py::score_to_label` chooses human, unsure, or AI.
6. `audit.py` records the decision and both signals.
7. The service returns the result and lets the writer appeal by content ID.

## Signals and Scoring

**Model signal:** `detector.py::model_signal` uses GPT-2 predictability. AI
text can be more predictable, but plain human writing can look predictable too.

**Style signal:** `stylometry.py::style_signal` measures sentence-length
spread, unique-word ratio, and punctuation density. Generated prose can be
more even, but edits, quotations, or typos can change the shape cheaply.

**Combining rule:** `scoring.py::combine_signals` uses 60% model signal and
40% style signal. Higher means more likely AI. On the AI sample, the signals
split at 0.7862 and 0.4826; the combined score was 0.6648.

## Label Variants

| Label | Range | Text shown to the reader |
|---|---|---|
| High-confidence human | 0.00–0.35 | This text is likely written by a person. |
| Unsure | above 0.35–below 0.65 | We could not determine how this text was written, so no accusation is being made. |
| High-confidence AI | 0.65–1.00 | This text is likely AI-generated. The writer may appeal if this is incorrect. |

The unsure label avoids accusing the writer when the two signals do not give
strong evidence.

## Sample Run

**Submission**

```text
POST /submit
{"creator_id":"writer-ai","text":"The implementation of the proposed framework requires careful consideration..."}
```

```json
{
  "confidence": 0.6648,
  "content_id": "1e2b3bd226f04febb7cab7307bc0e965",
  "guess": "ai",
  "label": "This text is likely AI-generated. The writer may appeal if this is incorrect.",
  "model_score": 0.7862,
  "style_score": 0.4826
}
```

**Appeal**

```text
POST /appeal
{"content_id":"1e2b3bd226f04febb7cab7307bc0e965","reasoning":"I wrote this paragraph myself and can provide drafts."}
```

```json
{
  "content_id": "1e2b3bd226f04febb7cab7307bc0e965",
  "message": "Your appeal was recorded for human review.",
  "status": "under_review"
}
```

**Audit entries**

```json
{"content_id":"1e2b3bd226f04febb7cab7307bc0e965","creator_id":"writer-ai","guess":"ai","model_score":0.7862,"style_score":0.4826,"combined_score":0.6648,"status":"decided"}
{"content_id":"1e2b3bd226f04febb7cab7307bc0e965","creator_id":"writer-ai","event":"appeal","reasoning":"I wrote this paragraph myself and can provide drafts.","status":"under_review"}
```

## How I Used AI

- AI helped review the endpoint contract. I added clear 4xx errors.
