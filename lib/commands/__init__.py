"""
Déjà command implementations.

All commands return a tuple: (summary_line, data_dict)
"""

from commands.search import search
from commands.read import read
from commands.listing import recent, episodes
from commands.simple import note, edit_note, delete_note, projects

__all__ = ['search', 'read', 'recent', 'episodes', 'note', 'edit_note', 'delete_note', 'projects']
