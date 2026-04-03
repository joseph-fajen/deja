"""
Tests for edit_note and delete_note wrappers in lib/commands/simple.py.
"""

import os
import sys

import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib', 'commands'))

from notes import NotesSaveError
import simple


SESSION_ID = "abcdef1234567890"
SESSION_PREFIX = SESSION_ID[:8]


# ---------------------------------------------------------------------------
# edit_note — success path
# ---------------------------------------------------------------------------

def test_edit_note_success_summary_line():
    with patch('simple.edit_note_in_session', return_value="old text"):
        summary, _ = simple.edit_note(SESSION_ID, 1, "new text")
    assert summary == f"Edited note 1 on {SESSION_PREFIX}"


def test_edit_note_success_result_shape():
    with patch('simple.edit_note_in_session', return_value="old text"):
        _, result = simple.edit_note(SESSION_ID, 2, "new text")
    assert result['success'] is True
    assert result['sessionId'] == SESSION_ID
    assert result['index'] == 2
    assert result['oldNote'] == "old text"
    assert result['newNote'] == "new text"


def test_edit_note_passes_args_to_notes_module():
    with patch('simple.edit_note_in_session') as mock_edit:
        mock_edit.return_value = "old"
        simple.edit_note(SESSION_ID, 3, "updated")
    mock_edit.assert_called_once_with(SESSION_ID, 3, "updated")


# ---------------------------------------------------------------------------
# edit_note — error paths
# ---------------------------------------------------------------------------

def test_edit_note_index_error_returns_failure():
    with patch('simple.edit_note_in_session', side_effect=IndexError("Note 5 not found")):
        summary, result = simple.edit_note(SESSION_ID, 5, "x")
    assert result['success'] is False
    assert "Note 5 not found" in result['error']
    assert summary == result['error']


def test_edit_note_save_error_returns_failure():
    with patch('simple.edit_note_in_session', side_effect=NotesSaveError("disk full")):
        summary, result = simple.edit_note(SESSION_ID, 1, "x")
    assert result['success'] is False
    assert "disk full" in result['error']
    assert summary == result['error']


def test_edit_note_error_result_has_no_extra_keys():
    with patch('simple.edit_note_in_session', side_effect=IndexError("out of range")):
        _, result = simple.edit_note(SESSION_ID, 99, "x")
    assert set(result.keys()) == {'success', 'error'}


# ---------------------------------------------------------------------------
# delete_note — success path
# ---------------------------------------------------------------------------

def test_delete_note_success_summary_line():
    with patch('simple.delete_note_from_session', return_value="deleted text"):
        summary, _ = simple.delete_note(SESSION_ID, 1)
    assert summary == f"Deleted note 1 from {SESSION_PREFIX}"


def test_delete_note_success_result_shape():
    with patch('simple.delete_note_from_session', return_value="deleted text"):
        _, result = simple.delete_note(SESSION_ID, 2)
    assert result['success'] is True
    assert result['sessionId'] == SESSION_ID
    assert result['index'] == 2
    assert result['deletedNote'] == "deleted text"


def test_delete_note_passes_args_to_notes_module():
    with patch('simple.delete_note_from_session') as mock_delete:
        mock_delete.return_value = "gone"
        simple.delete_note(SESSION_ID, 4)
    mock_delete.assert_called_once_with(SESSION_ID, 4)


# ---------------------------------------------------------------------------
# delete_note — error paths
# ---------------------------------------------------------------------------

def test_delete_note_index_error_returns_failure():
    with patch('simple.delete_note_from_session', side_effect=IndexError("Note 3 not found")):
        summary, result = simple.delete_note(SESSION_ID, 3)
    assert result['success'] is False
    assert "Note 3 not found" in result['error']
    assert summary == result['error']


def test_delete_note_save_error_returns_failure():
    with patch('simple.delete_note_from_session', side_effect=NotesSaveError("write failed")):
        summary, result = simple.delete_note(SESSION_ID, 1)
    assert result['success'] is False
    assert "write failed" in result['error']
    assert summary == result['error']


def test_delete_note_error_result_has_no_extra_keys():
    with patch('simple.delete_note_from_session', side_effect=IndexError("bad index")):
        _, result = simple.delete_note(SESSION_ID, 0)
    assert set(result.keys()) == {'success', 'error'}
