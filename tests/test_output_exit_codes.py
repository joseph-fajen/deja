import sys
import types
import pytest
from pathlib import Path

# Load the deja script (no .py extension) as a module
_deja_path = Path(__file__).parent.parent / "deja"
_source = _deja_path.read_text()
deja_script = types.ModuleType("deja_script")
deja_script.__file__ = str(_deja_path)
exec(compile(_source, str(_deja_path), "exec"), deja_script.__dict__)
output = deja_script.output


def test_output_does_not_exit_when_success_true(capsys):
    # success=True — output() should return normally without calling sys.exit
    output("done", {"success": True, "note": "hello"})  # should not raise


def test_output_exits_0_when_success_absent(capsys):
    # success not in data defaults to True — should not exit 1
    try:
        output("done", {"note": "hello"})
    except SystemExit as e:
        assert e.code != 1, f"Expected exit 0 or no exit, got exit {e.code}"


def test_output_exits_1_when_success_false(capsys):
    with pytest.raises(SystemExit) as exc_info:
        output("error: note not found", {"success": False, "error": "not found"})
    assert exc_info.value.code == 1


def test_output_prints_summary_line(capsys):
    with pytest.raises(SystemExit):
        output("my summary", {"success": False})
    captured = capsys.readouterr()
    assert "my summary" in captured.out


def test_output_prints_json(capsys):
    with pytest.raises(SystemExit):
        output("summary", {"success": False, "detail": "gone"})
    captured = capsys.readouterr()
    assert '"success": false' in captured.out
    assert '"detail": "gone"' in captured.out


def test_output_prints_json_for_success(capsys):
    # Capture output without SystemExit by using a try/except
    try:
        output("ok", {"key": "value"})
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert '"key": "value"' in captured.out


def test_output_exits_1_with_only_success_false(capsys):
    with pytest.raises(SystemExit) as exc_info:
        output("failed", {"success": False})
    assert exc_info.value.code == 1


def test_output_does_not_exit_1_with_success_true(capsys):
    """success=True should never trigger exit(1)."""
    exited_with = None
    try:
        output("all good", {"success": True})
    except SystemExit as e:
        exited_with = e.code
    assert exited_with != 1
