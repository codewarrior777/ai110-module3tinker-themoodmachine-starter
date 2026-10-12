# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class implements a lexicon-based classifier with:
  - Negation handling ("not happy" flips polarity)
  - Intensity amplification ("so excited" doubles weight)
  - Slang support (from dataset.py SLANG_POSITIVE / SLANG_NEGATIVE)
  - Emoji polarity signals (🙃, 😊, 🔥, 🙄, etc.)
  - A "mixed" label when both polarities are present
"""

import re
from typing import List, Optional, Tuple

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS

# Extended slang lists from dataset.py (added in Part 1)
try:
    from dataset import SLANG_POSITIVE, SLANG_NEGATIVE
except ImportError:
    SLANG_POSITIVE = []
    SLANG_NEGATIVE = []


# Words that flip the polarity of the following token
NEGATION_WORDS = {
    "not",
    "never",
    "no",
    "isn't",
    "aren't",
    "wasn't",
    "weren't",
    "don't",
    "doesn't",
    "didn't",
    "won't",
    "wouldn't",
    "can't",
    "couldn't",
}

# Words that amplify the following signal
INTENSITY_WORDS = {
    "very",
    "really",
    "so",
    "super",
    "extremely",
    "totally",
    "absolutely",
}

# Emojis as strong polarity signals
EMOJI_POSITIVE = {"🔥", "😊", "😂", "❤️", "💖", "👍", "🎉", "😍", "✨"}
EMOJI_NEGATIVE = {"🙃", "🙄", "💀", "😭", "😢", "😡", "👎", "😞", "🥲"}


class MoodAnalyzer:
    """A simple, rule-based mood classifier with negation and intensity."""

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        positive_words = (
            positive_words if positive_words is not None else POSITIVE_WORDS
        )
        negative_words = (
            negative_words if negative_words is not None else NEGATIVE_WORDS
        )

        # Merge base lists with slang lists (lowercased, deduplicated via set)
        self.positive_words = {w.lower() for w in positive_words} | {
            w.lower() for w in SLANG_POSITIVE
        }
        self.negative_words = {w.lower() for w in negative_words} | {
            w.lower() for w in SLANG_NEGATIVE
        }

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens.

        Improvements over the starter version:
          - Normalizes repeated characters ("sooooo" -> "soo")
          - Strips surrounding punctuation from each token
          - Preserves emojis (they carry polarity information)
        """
        text = text.lower().strip()

        # Collapse 3+ repeated characters to 2 (keeps "soo" but not "sooooo")
        text = re.sub(r"(.)\1{2,}", r"\1\1", text)

        raw_tokens = text.split()
        tokens = [t.strip(".,!?;:\"'()[]{}") for t in raw_tokens]

        return [t for t in tokens if t]

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def _count_polarity(self, text: str) -> Tuple[int, int]:
        """
        Return (positive_signals, negative_signals) after applying:
          - Negation flipping ("not happy" -> negative signal)
          - Intensity amplification ("so excited" -> weight 2)
          - Slang detection (via self.positive_words / self.negative_words)
          - Emoji polarity (EMOJI_POSITIVE / EMOJI_NEGATIVE)
        """
        tokens = self.preprocess(text)
        pos = 0
        neg = 0

        for i, token in enumerate(tokens):
            prev = tokens[i - 1] if i > 0 else ""
            is_negated = prev in NEGATION_WORDS
            is_intensified = prev in INTENSITY_WORDS
            weight = 2 if is_intensified else 1

            if token in self.positive_words:
                if is_negated:
                    neg += weight
                else:
                    pos += weight
            elif token in self.negative_words:
                if is_negated:
                    pos += weight
                else:
                    neg += weight
            elif token in EMOJI_POSITIVE:
                pos += 2  # emojis are strong signals
            elif token in EMOJI_NEGATIVE:
                neg += 2

        return pos, neg

    def score_text(self, text: str) -> int:
        """
        Compute a numeric mood score.

        Positive signals increase the score, negative signals decrease it.
        The score is the net difference after accounting for negation,
        intensity, slang, and emojis.
        """
        pos, neg = self._count_polarity(text)
        return pos - neg

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the score into a mood label.

        Mapping:
          - Both polarities present with similar magnitude -> "mixed"
          - net score > 0 -> "positive"
          - net score < 0 -> "negative"
          - net score == 0 -> "neutral"
        """
        pos, neg = self._count_polarity(text)

        # Mixed: both sides present, similar magnitude
        if pos > 0 and neg > 0 and abs(pos - neg) <= 1:
            return "mixed"

        net = pos - neg
        if net > 0:
            return "positive"
        if net < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """Return a short human-readable explanation of the score."""
        tokens = self.preprocess(text)
        positive_hits: List[str] = []
        negative_hits: List[str] = []

        for i, token in enumerate(tokens):
            prev = tokens[i - 1] if i > 0 else ""
            is_negated = prev in NEGATION_WORDS

            if token in self.positive_words or token in EMOJI_POSITIVE:
                if is_negated:
                    negative_hits.append(f"not {token}")
                else:
                    positive_hits.append(token)
            elif token in self.negative_words or token in EMOJI_NEGATIVE:
                if is_negated:
                    positive_hits.append(f"not {token}")
                else:
                    negative_hits.append(token)

        pos, neg = self._count_polarity(text)
        score = pos - neg
        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
