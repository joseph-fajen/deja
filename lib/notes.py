"""
Notes storage - breadcrumbs left on sessions for future searches.
"""

import os
import sys
import json
from typing import Dict, List

from config import NOTES_PATH


# In-memory cache
_notes_cache: Dict[str, List[str]] = {}
_notes_loaded = False


def load_notes():
    """Load notes from disk"""
    global _notes_cache, _notes_loaded
    if _notes_loaded:
        return
    try:
        if os.path.exists(NOTES_PATH):
            with open(NOTES_PATH, 'r') as f:
                _notes_cache = json.load(f)
    except Exception as e:
        print(f"Error loading notes: {e}", file=sys.stderr)
        _notes_cache = {}
    _notes_loaded = True


def save_notes():
    """Save notes to disk"""
    try:
        os.makedirs(os.path.dirname(NOTES_PATH), exist_ok=True)
        with open(NOTES_PATH, 'w') as f:
            json.dump(_notes_cache, f, indent=2)
    except Exception as e:
        print(f"Error saving notes: {e}", file=sys.stderr)


def get_notes_for_session(session_id: str) -> List[str]:
    """Get notes for a specific session"""
    load_notes()
    return _notes_cache.get(session_id, [])


def add_note_to_session(session_id: str, note: str) -> int:
    """Add a note to a session, returns total notes count"""
    load_notes()

    if session_id not in _notes_cache:
        _notes_cache[session_id] = []

    _notes_cache[session_id].append(note)
    save_notes()

    return len(_notes_cache[session_id])


def edit_note_in_session(session_id: str, index: int, new_text: str) -> str:
    """
    Edit a note by 1-based index. Returns the old note text.
    Raises IndexError if index is out of range.
    """
    load_notes()

    notes = _notes_cache.get(session_id, [])
    if index < 1 or index > len(notes):
        raise IndexError(f"Note index {index} out of range (1-{len(notes)})")

    old_text = notes[index - 1]
    _notes_cache[session_id][index - 1] = new_text
    save_notes()

    return old_text


def delete_note_from_session(session_id: str, index: int) -> str:
    """
    Delete a note by 1-based index. Returns the deleted note text.
    Raises IndexError if index is out of range.
    """
    load_notes()

    notes = _notes_cache.get(session_id, [])
    if index < 1 or index > len(notes):
        raise IndexError(f"Note index {index} out of range (1-{len(notes)})")

    deleted = _notes_cache[session_id].pop(index - 1)
    save_notes()

    return deleted
