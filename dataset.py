"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Extended word lists (added for Part 1)
# These help the rule-based classifier handle slang and modern usage.
# ---------------------------------------------------------------------

# Slang terms that mean "positive" in modern usage (but not in a dictionary)
SLANG_POSITIVE = [
    "slaps",
    "fire",
    "wicked",
    "sick",
    "lit",
    "dope",
    "goat",
    "based",
]

# Slang terms that mean "negative" in modern usage
SLANG_NEGATIVE = [
    "yikes",
    "cringe",
    "trash",
    "mid",
    "sus",
    "flop",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    # --- Original 6 from starter ---
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",

    # --- Part 1: 8 new posts with modern language, slang, emojis, sarcasm ---
    "This slaps, no cap 🔥",
    "Big yikes, that was rough",
    "I'm fine 🙃",
    "Exhausted but proud of myself",
    "Great, another Monday 🙄",
    "Lowkey stressed but kind of proud",
    "Not gonna lie, kind of disappointed",
    "Actually feeling really good today 😊",
]

# Human labels for each post above.
# Allowed labels:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    # --- Original 6 ---
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"

    # --- Part 1: labels for the 8 new posts ---
    "positive",  # "This slaps, no cap 🔥"
    "negative",  # "Big yikes, that was rough"
    "negative",  # "I'm fine 🙃" (the emoji flips it — sarcasm)
    "mixed",     # "Exhausted but proud of myself"
    "negative",  # "Great, another Monday 🙄" (sarcasm: "great" is a cue)
    "mixed",     # "Lowkey stressed but kind of proud"
    "negative",  # "Not gonna lie, kind of disappointed"
    "positive",  # "Actually feeling really good today 😊"
]

# ---------------------------------------------------------------------
# Sanity check
# ---------------------------------------------------------------------

# This assert protects against the #1 silent bug in labeled datasets:
# features and labels drifting out of alignment.
assert len(SAMPLE_POSTS) == len(TRUE_LABELS), (
    f"Dataset is misaligned: {len(SAMPLE_POSTS)} posts vs "
    f"{len(TRUE_LABELS)} labels."
)