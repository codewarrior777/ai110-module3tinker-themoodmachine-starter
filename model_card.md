# Mood Machine — Model Card

**Author:** Gustavo Ramos
**Date:** October 2026
**Course:** AI 110 — Foundations of AI Engineering
**Tinker:** The Mood Machine

---

## 1. Model Overview

**Model name:** Mood Machine v1.0
**Type:** Rule-based sentiment classifier (lexicon-based scoring with negation, intensity, slang, emoji, and sarcasm handling).
**Intended use:** Classify short English social-media style posts as `positive`, `negative`, `neutral`, or `mixed`.
**Out of scope:** Long-form text, non-English, emoji-only posts, code-switching, and high-stakes decisions (medical, hiring, moderation).

---

## 2. How the Model Works

The classifier uses four steps:

1. **Preprocess** — lowercase, collapse repeated characters (`sooooo → soo`), strip punctuation, preserve emojis.
2. **Count polarity** — for each token, check if it is in `POSITIVE_WORDS`, `NEGATIVE_WORDS`, `SLANG_POSITIVE`, `SLANG_NEGATIVE`, `EMOJI_POSITIVE`, or `EMOJI_NEGATIVE`. Apply:
   - **Negation flip** if the previous token is in `NEGATION_WORDS` ("not happy" → negative signal).
   - **Intensity weight** ×2 if the previous token is in `INTENSITY_WORDS` ("so excited" → +2).
   - **Sarcasm override** if a `SARCASM_TRIGGER` appears anywhere in the sentence and the token is positive ("love getting stuck in traffic" → negative signal).
3. **Score** — net score = positive signals − negative signals.
4. **Predict** — both signals present with similar magnitude → `mixed`; otherwise positive/negative/neutral by sign.

---

## 3. Data

| Item | Value |
|---|---|
| **Training data** | None — this is a rule-based system with no training. |
| **Evaluation data** | 14 hand-labeled English posts (`SAMPLE_POSTS` + `TRUE_LABELS` in `dataset.py`). |
| **Label vocabulary** | `positive`, `negative`, `neutral`, `mixed`. |
| **Data shape** | Mixed formality — includes standard English, slang, emojis, sarcasm, and ambiguous/mixed emotions. |
| **Data limitations** | Small (n=14). English-only. Biased toward casual social-media style. Not labeled by multiple annotators (no inter-rater agreement measured). |

---

## 4. Evaluation Results

### 4a. Rule-Based Model

```
Rule-based accuracy on SAMPLE_POSTS: 0.71  (10/14 correct)
```

**Posts where it fails:**

| Post | Predicted | True | Why it fails |
|---|---|---|---|
| "Feeling tired but kind of hopeful" | negative | mixed | Only "tired" is registered; "hopeful" isn't in the positive list |
| "Exhausted but proud of myself" | neutral | mixed | "exhausted" and "proud" are both out of the word lists |
| "Lowkey stressed but kind of proud" | negative | mixed | "proud" not in the positive list; "stressed" dominates |
| "Not gonna lie, kind of disappointed" | neutral | negative | "disappointed" is not in the negative list |

### 4b. ML Model (Logistic Regression + CountVectorizer)

```
Accuracy on this dataset: 1.00  (14/14 correct)
```

### 4c. ⚠️ Critical caveat on the ML accuracy

**The ML model was trained and evaluated on the SAME 14 samples.** The code comment in `ml_experiments.py` even says `# Evaluate on the same dataset (training accuracy)`.

With n=14 and `LogisticRegression(max_iter=1000)`, the model has enough parameters to memorize every word-to-label mapping without learning anything generalizable. **The 1.00 accuracy is a data-leakage artifact, not evidence of superior performance.**

A correct evaluation would require a held-out test set — but with only 14 samples, we cannot meaningfully split. This is exactly why the assignment emphasizes expanding the dataset in Part 1.

---

## 5. Limitations

1. **Sarcasm is only partially handled.** The `SARCASM_TRIGGERS` list (`stuck`, `traffic`, `monday`, `another`, etc.) fixes *specific* cases but will misclassify sincere equivalents. Example: *"I love my Monday morning coffee routine"* → classified negative (wrong).
2. **Mixed emotions are systematically under-detected.** Words like `hopeful`, `proud`, `grateful` aren't in the starter positive list, so mixed posts lean toward their negative half.
3. **No word-sense disambiguation.** `"sick"` is tagged positive (slang) but `"I'm sick"` (illness) is not distinguished.
4. **No negation scope.** `"I don't think it's bad"` double-negates only on the immediate previous token — "don't think it's bad" → `"don't"` flips nothing because the immediately preceding token of `"bad"` is `"is"`.
5. **Emoji coverage is finite.** A fixed set of 9 positive + 9 negative emojis. New emojis default to neutral.
6. **English only.** No code-switching or non-Latin scripts.

---

## 6. Bias Note

**One style or group the model may under-serve:**

The model performs worse on **informal/regional English** than on standard English. Posts using AAVE features, regional slang, or non-standard spellings are more likely to be misclassified than equivalent standard-English posts.

**Why this matters:** this is a documented pattern in commercial sentiment analysis systems (see: *Gender Shades*, *Language technology and African American English*). A lexicon-based system trained on one dialect's vocabulary will systematically under-serve users who write in other dialects. The rule-based model was authored by one person (me) using one dialect, and that bias is embedded in every word list.

**Concrete example:** the sentence *"That was sick"* is positive in modern slang, but negative in formal English. The model was fixed for this case (SLANG_POSITIVE), but the same fix was **not applied** to words like `wicked`, `ill`, or `dope` at the start — I had to add them manually after seeing the failure. This is a whack-a-mole pattern, not a systemic solution.

---

## 7. Coverage and Oversight Note

**When I asked AI to help write word lists and scoring logic, did it flag any bias or coverage gaps?**

**No.** When I prompted ChatGPT and Gemini to help implement `score_text()`, `predict_label()`, and the slang additions, **neither model proactively flagged** that:
- `"sick"` would be misclassified as negative in slang contexts
- `"proud"`, `"hopeful"`, `"grateful"` were missing from the positive list
- sarcasm would defeat the classifier
- the dataset was too small for meaningful ML evaluation

Both models answered exactly the code mechanics I asked for, and stopped there. **They did not volunteer "here are the kinds of input this will get wrong."**

**My reflection:** this is a case where AI tools passed on a coverage gap **silently**. In a real project, I would push back by asking explicitly: *"What inputs would this classifier fail on?"* and require the AI to enumerate them before I ship. That's the difference between using AI as a code assistant and using it as a design reviewer. **The assignment asks for the reviewer.**

---

## 8. Rule-Based vs. ML Comparison

| Aspect | Rule-Based (mine) | ML (baseline) |
|---|---|---|
| **Accuracy (on our 14-post set)** | 0.71 | 1.00 *— but trained and tested on the same data* |
| **Interpretability** | High — I can trace every score to a specific rule | Low — logistic weights are opaque |
| **Data dependency** | None | High — accuracy collapses without enough samples |
| **Failure mode** | Predictable: unknown words → neutral | Silent: high-confidence wrong answers |
| **Slang handling** | Manual whack-a-mole | Learned if the training set includes it |
| **Sarcasm handling** | Trigger-word override (fragile) | Would need sarcasm examples in training data |
| **Iteration cost** | Edit a list, re-run, no retraining | Requires re-labeling + retraining |
| **Risk of overfitting** | None (no parameters) | Very high with n=14 |

**Takeaway:** rule-based systems are **interpretable but brittle**; ML systems are **flexible but data-hungry and opaque**. Neither is universally better — the right choice depends on the data volume, the interpretability requirement, and the cost of silent failures.

---

## 9. Reflections and Next Steps

**What I would do differently:**
1. **Grow the dataset to 200+ labeled posts** before drawing any ML conclusions. With n=14, a train/test split is meaningless.
2. **Add multi-annotator labeling** to measure inter-rater agreement. Some of my "true" labels (e.g., *"I'm fine 🙃"* = negative) are debatable.
3. **Add a test split** to `ml_experiments.py` and report both training and test accuracy — to expose the data leakage the current evaluation hides.
4. **Source word lists from a peer-reviewed lexicon** (VADER, SentiWordNet) instead of writing them by hand.
5. **Add a proper evaluation harness** with per-class precision/recall, not just overall accuracy — the 14-post set is severely imbalanced (only 1 `neutral`).

**The single most important lesson:** 100% training accuracy is not a signal of quality. It is a signal that you haven't split your data.