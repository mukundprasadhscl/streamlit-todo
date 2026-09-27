# Streamlit Todo App

A minimal todo app built with [Streamlit](https://streamlit.io).  
Add, complete, and delete todos — state lives in the session.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Run tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Project layout

```
app.py              # Streamlit UI
todo_state.py       # Pure logic (add / toggle / delete) — no Streamlit dependency
tests/
  test_todo_state.py
requirements.txt
requirements-dev.txt
pyproject.toml
.github/workflows/ci.yml
```

## Design notes

- **Logic/UI split**: `todo_state.py` contains pure functions that operate on plain
  `Todo` dataclass instances. No Streamlit import means the tests run fast and
  without a browser.
- **Immutable updates**: every function returns a new list rather than mutating
  the input, which makes session-state assignment explicit and avoids subtle
  Streamlit rerun bugs.
- **No persistence**: todos live in `st.session_state` for the duration of the
  browser session. Adding a backend (SQLite, a file, an API) is a separate
  concern and is intentionally out of scope here.
