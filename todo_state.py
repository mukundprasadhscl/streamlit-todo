"""
Pure-logic layer for the todo list.

Kept separate from the Streamlit UI so it can be unit-tested without
starting a browser or importing streamlit.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import List


@dataclass
class Todo:
    text: str
    done: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


def add_todo(todos: List[Todo], text: str) -> List[Todo]:
    """Return a new list with the given text appended as an incomplete todo."""
    text = text.strip()
    if not text:
        raise ValueError("Todo text must not be empty.")
    return todos + [Todo(text=text)]


def toggle_todo(todos: List[Todo], todo_id: str) -> List[Todo]:
    """Return a new list with the matching todo's done flag flipped."""
    return [
        Todo(text=t.text, done=not t.done, id=t.id) if t.id == todo_id else t
        for t in todos
    ]


def delete_todo(todos: List[Todo], todo_id: str) -> List[Todo]:
    """Return a new list with the matching todo removed."""
    return [t for t in todos if t.id != todo_id]
