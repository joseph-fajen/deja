"""
Tests for note management: add, edit, delete.
"""

import json
import os
import sys
import tempfile

import pytest

# Add lib to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))


@pytest.fixture()
def notes_mod(tmp_path, monkeypatch):
    """Fresh notes module state pointing at a temp file for each test."""
    import notes
    notes_file = str(tmp_path / "notes.json")
    monkeypatch.setattr(notes, "NOTES_PATH", notes_file)
    notes._notes_cache = {}
    notes._notes_loaded = False
    return notes


# ---------------------------------------------------------------------------
# add_note_to_session
# ---------------------------------------------------------------------------

def test_add_note_returns_count(notes_mod):
    count = notes_mod.add_note_to_session("sess1", "first note")
    assert count == 1


def test_add_multiple_notes_increments_count(notes_mod):
    notes_mod.add_note_to_session("sess1", "a")
    count = notes_mod.add_note_to_session("sess1", "b")
    assert count == 2


def test_add_note_persists(notes_mod):
    notes_mod.add_note_to_session("sess1", "persistent note")

    with open(notes_mod.NOTES_PATH) as f:
        data = json.load(f)

    assert "sess1" in data
    assert data["sess1"] == ["persistent note"]


def test_get_notes_returns_empty_for_unknown_session(notes_mod):
    result = notes_mod.get_notes_for_session("unknown")
    assert result == []


def test_get_notes_returns_added_notes(notes_mod):
    notes_mod.add_note_to_session("sess1", "note one")
    notes_mod.add_note_to_session("sess1", "note two")
    assert notes_mod.get_notes_for_session("sess1") == ["note one", "note two"]


# ---------------------------------------------------------------------------
# edit_note_in_session
# ---------------------------------------------------------------------------

def test_edit_note_changes_text(notes_mod):
    notes_mod.add_note_to_session("sess1", "original")
    notes_mod.edit_note_in_session("sess1", 1, "updated")
    assert notes_mod.get_notes_for_session("sess1") == ["updated"]


def test_edit_note_returns_old_text(notes_mod):
    notes_mod.add_note_to_session("sess1", "old text")
    old = notes_mod.edit_note_in_session("sess1", 1, "new text")
    assert old == "old text"


def test_edit_note_middle_of_list(notes_mod):
    notes_mod.add_note_to_session("sess1", "a")
    notes_mod.add_note_to_session("sess1", "b")
    notes_mod.add_note_to_session("sess1", "c")
    notes_mod.edit_note_in_session("sess1", 2, "B")
    assert notes_mod.get_notes_for_session("sess1") == ["a", "B", "c"]


def test_edit_note_index_zero_raises(notes_mod):
    notes_mod.add_note_to_session("sess1", "note")
    with pytest.raises(IndexError):
        notes_mod.edit_note_in_session("sess1", 0, "x")


def test_edit_note_index_too_large_raises(notes_mod):
    notes_mod.add_note_to_session("sess1", "only note")
    with pytest.raises(IndexError):
        notes_mod.edit_note_in_session("sess1", 2, "x")


def test_edit_note_on_empty_session_raises(notes_mod):
    with pytest.raises(IndexError):
        notes_mod.edit_note_in_session("empty_sess", 1, "x")


def test_edit_note_persists_to_disk(notes_mod):
    notes_mod.add_note_to_session("sess1", "before")
    notes_mod.edit_note_in_session("sess1", 1, "after")

    with open(notes_mod.NOTES_PATH) as f:
        data = json.load(f)

    assert data["sess1"] == ["after"]


# ---------------------------------------------------------------------------
# delete_note_from_session
# ---------------------------------------------------------------------------

def test_delete_note_removes_entry(notes_mod):
    notes_mod.add_note_to_session("sess1", "keep")
    notes_mod.add_note_to_session("sess1", "remove")
    notes_mod.delete_note_from_session("sess1", 2)
    assert notes_mod.get_notes_for_session("sess1") == ["keep"]


def test_delete_note_returns_deleted_text(notes_mod):
    notes_mod.add_note_to_session("sess1", "gone")
    deleted = notes_mod.delete_note_from_session("sess1", 1)
    assert deleted == "gone"


def test_delete_note_middle_of_list(notes_mod):
    notes_mod.add_note_to_session("sess1", "a")
    notes_mod.add_note_to_session("sess1", "b")
    notes_mod.add_note_to_session("sess1", "c")
    notes_mod.delete_note_from_session("sess1", 2)
    assert notes_mod.get_notes_for_session("sess1") == ["a", "c"]


def test_delete_note_index_zero_raises(notes_mod):
    notes_mod.add_note_to_session("sess1", "note")
    with pytest.raises(IndexError):
        notes_mod.delete_note_from_session("sess1", 0)


def test_delete_note_index_too_large_raises(notes_mod):
    notes_mod.add_note_to_session("sess1", "only")
    with pytest.raises(IndexError):
        notes_mod.delete_note_from_session("sess1", 2)


def test_delete_note_on_empty_session_raises(notes_mod):
    with pytest.raises(IndexError):
        notes_mod.delete_note_from_session("empty_sess", 1)


def test_delete_note_persists_to_disk(notes_mod):
    notes_mod.add_note_to_session("sess1", "first")
    notes_mod.add_note_to_session("sess1", "second")
    notes_mod.delete_note_from_session("sess1", 1)

    with open(notes_mod.NOTES_PATH) as f:
        data = json.load(f)

    assert data["sess1"] == ["second"]
