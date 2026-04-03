import subprocess
import sys
import os

DEJA = os.path.join(os.path.dirname(__file__), '..', 'deja')


def run_deja(*args):
    result = subprocess.run(
        [sys.executable, DEJA] + list(args),
        capture_output=True,
        text=True,
    )
    return result


def test_note_edit_missing_index_and_text_exits_nonzero():
    result = run_deja('somesession', '=note')
    assert result.returncode == 1


def test_note_edit_missing_text_exits_nonzero():
    result = run_deja('somesession', '=note', '3')
    assert result.returncode == 1


def test_note_edit_missing_index_prints_error():
    result = run_deja('somesession', '=note')
    assert 'Error: =note requires an index and replacement text' in result.stderr


def test_note_edit_missing_index_prints_usage():
    result = run_deja('somesession', '=note')
    assert 'Usage:' in result.stderr


def test_note_edit_missing_text_prints_error():
    result = run_deja('somesession', '=note', '3')
    assert 'Error: =note requires an index and replacement text' in result.stderr
