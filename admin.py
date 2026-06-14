"""
Admin Manager for LoveBot
Tracks warnings and word filters per chat
"""

from collections import defaultdict
from typing import Dict, List, Set


class AdminManager:
    def __init__(self):
        # {chat_id: {user_id: warn_count}}
        self._warns: Dict[int, Dict[int, int]] = defaultdict(lambda: defaultdict(int))
        # {chat_id: set of filtered words}
        self._filters: Dict[int, Set[str]] = defaultdict(set)

    # ── Warnings ──────────────────────────────────────────

    def add_warn(self, user_id: int, chat_id: int) -> int:
        """Add a warning and return the new count."""
        self._warns[chat_id][user_id] += 1
        return self._warns[chat_id][user_id]

    def get_warn_count(self, user_id: int, chat_id: int) -> int:
        return self._warns[chat_id].get(user_id, 0)

    def reset_warns(self, user_id: int, chat_id: int):
        self._warns[chat_id][user_id] = 0

    # ── Word Filters ──────────────────────────────────────

    def add_filter(self, chat_id: int, word: str):
        self._filters[chat_id].add(word.lower())

    def remove_filter(self, chat_id: int, word: str):
        self._filters[chat_id].discard(word.lower())

    def get_filters(self, chat_id: int) -> List[str]:
        return sorted(self._filters.get(chat_id, set()))

    def is_filtered(self, chat_id: int, text: str) -> bool:
        text_lower = text.lower()
        return any(word in text_lower for word in self._filters.get(chat_id, set()))
