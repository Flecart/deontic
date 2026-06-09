"""Generator protocol shared by the backends.

A "conversation" is a list of chat messages: [{"role": ..., "content": ...}, ...].
Backends apply the tokenizer's chat template, so callers work in messages, not
raw prompt strings.
"""

from __future__ import annotations

from typing import Protocol

Message = dict[str, str]
Conversation = list[Message]


class Generator(Protocol):
    def chat(
        self,
        conversations: list[Conversation],
        max_new_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
    ) -> list[str]:
        """Generate one completion per conversation. Returns assistant texts."""
        ...
