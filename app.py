"""
Streamlit Todo App
------------------
Add, complete, and delete todos.
State is stored in st.session_state so it survives reruns within a session.
"""
import streamlit as st

from todo_state import Todo, add_todo, delete_todo, toggle_todo

# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Todo", page_icon="✅", layout="centered")

# ── session state bootstrap ───────────────────────────────────────────────────
if "todos" not in st.session_state:
    st.session_state.todos: list[Todo] = []

# ── header ────────────────────────────────────────────────────────────────────
st.title("✅ Todo")

# ── add form ──────────────────────────────────────────────────────────────────
with st.form("add_form", clear_on_submit=True):
    new_text = st.text_input("New todo", placeholder="What needs doing?", label_visibility="collapsed")
    submitted = st.form_submit_button("Add", use_container_width=True)

if submitted:
    if new_text.strip():
        st.session_state.todos = add_todo(st.session_state.todos, new_text)
    else:
        st.warning("Please enter some text before adding.")

# ── list ──────────────────────────────────────────────────────────────────────
todos = st.session_state.todos

if not todos:
    st.info("No todos yet — add one above.")
else:
    pending = [t for t in todos if not t.done]
    done    = [t for t in todos if t.done]

    def _render_item(todo: Todo) -> None:
        col_check, col_text, col_del = st.columns([0.07, 0.80, 0.13])
        with col_check:
            if st.button("☑" if todo.done else "☐", key=f"toggle_{todo.id}", help="Toggle complete"):
                st.session_state.todos = toggle_todo(st.session_state.todos, todo.id)
                st.rerun()
        with col_text:
            label = f"~~{todo.text}~~" if todo.done else todo.text
            st.markdown(label)
        with col_del:
            if st.button("🗑", key=f"del_{todo.id}", help="Delete"):
                st.session_state.todos = delete_todo(st.session_state.todos, todo.id)
                st.rerun()

    if pending:
        st.subheader(f"Pending ({len(pending)})")
        for t in pending:
            _render_item(t)

    if done:
        st.subheader(f"Done ({len(done)})")
        for t in done:
            _render_item(t)

    # ── bulk clear ────────────────────────────────────────────────────────────
    if done:
        if st.button("Clear completed", type="secondary"):
            st.session_state.todos = [t for t in st.session_state.todos if not t.done]
            st.rerun()
