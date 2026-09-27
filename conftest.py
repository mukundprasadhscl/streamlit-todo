# Ensure the repo root is on sys.path so tests can import todo_state directly.
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
