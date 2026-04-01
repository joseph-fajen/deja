"""
Simple commands for Déjà: notes and project listing.
"""

import os
import glob as glob_module

from config import CLAUDE_PROJECTS_PATH
from notes import add_note_to_session, edit_note_in_session, delete_note_from_session


def note(session_id, note_text):
    """Add a note to a session"""
    total = add_note_to_session(session_id, note_text)

    summary_line = f"Added note to {session_id[:8]} ({total} total notes)"
    return summary_line, {
        'success': True,
        'sessionId': session_id,
        'note': note_text,
        'totalNotes': total
    }


def edit_note(session_id: str, index: int, new_text: str):
    """Edit a note by 1-based index"""
    try:
        old_text = edit_note_in_session(session_id, index, new_text)
    except IndexError as e:
        return str(e), {'success': False, 'error': str(e)}

    summary_line = f"Edited note {index} on {session_id[:8]}"
    return summary_line, {
        'success': True,
        'sessionId': session_id,
        'index': index,
        'oldNote': old_text,
        'newNote': new_text,
    }


def delete_note(session_id: str, index: int):
    """Delete a note by 1-based index"""
    try:
        deleted_text = delete_note_from_session(session_id, index)
    except IndexError as e:
        return str(e), {'success': False, 'error': str(e)}

    summary_line = f"Deleted note {index} from {session_id[:8]}"
    return summary_line, {
        'success': True,
        'sessionId': session_id,
        'index': index,
        'deletedNote': deleted_text,
    }


def projects():
    """List available projects"""
    project_dirs = [d for d in glob_module.glob(os.path.join(CLAUDE_PROJECTS_PATH, "*"))
                   if os.path.isdir(d)]
    project_list = [os.path.basename(d) for d in project_dirs]

    summary_line = f"{len(project_list)} projects"
    return summary_line, {'projects': project_list}
