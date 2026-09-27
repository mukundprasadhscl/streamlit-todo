"""
Tests for the pure-logic layer in todo_state.py.
These run without Streamlit — just pytest.
"""
import pytest

from todo_state import Todo, add_todo, delete_todo, toggle_todo


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture()
def two_todos():
    base: list[Todo] = []
    base = add_todo(base, "Buy milk")
    base = add_todo(base, "Write tests")
    return base


# ── add_todo ──────────────────────────────────────────────────────────────────

class TestAddTodo:
    def test_appends_to_empty_list(self):
        result = add_todo([], "Hello")
        assert len(result) == 1
        assert result[0].text == "Hello"
        assert result[0].done is False

    def test_appends_to_existing_list(self, two_todos):
        result = add_todo(two_todos, "Third")
        assert len(result) == 3
        assert result[-1].text == "Third"

    def test_strips_whitespace(self):
        result = add_todo([], "  spaces  ")
        assert result[0].text == "spaces"

    def test_raises_on_empty_string(self):
        with pytest.raises(ValueError):
            add_todo([], "")

    def test_raises_on_whitespace_only(self):
        with pytest.raises(ValueError):
            add_todo([], "   ")

    def test_original_list_is_not_mutated(self):
        original = add_todo([], "First")
        add_todo(original, "Second")
        assert len(original) == 1

    def test_each_todo_gets_unique_id(self):
        result = add_todo(add_todo([], "A"), "B")
        assert result[0].id != result[1].id


# ── toggle_todo ───────────────────────────────────────────────────────────────

class TestToggleTodo:
    def test_marks_pending_as_done(self, two_todos):
        target_id = two_todos[0].id
        result = toggle_todo(two_todos, target_id)
        assert result[0].done is True

    def test_marks_done_as_pending(self, two_todos):
        target_id = two_todos[0].id
        once = toggle_todo(two_todos, target_id)
        twice = toggle_todo(once, target_id)
        assert twice[0].done is False

    def test_only_target_is_changed(self, two_todos):
        target_id = two_todos[0].id
        result = toggle_todo(two_todos, target_id)
        assert result[1].done is False

    def test_unknown_id_leaves_list_unchanged(self, two_todos):
        result = toggle_todo(two_todos, "nonexistent-id")
        assert all(t.done is False for t in result)

    def test_original_list_is_not_mutated(self, two_todos):
        toggle_todo(two_todos, two_todos[0].id)
        assert two_todos[0].done is False


# ── delete_todo ───────────────────────────────────────────────────────────────

class TestDeleteTodo:
    def test_removes_target(self, two_todos):
        target_id = two_todos[0].id
        result = delete_todo(two_todos, target_id)
        assert len(result) == 1
        assert result[0].id != target_id

    def test_unknown_id_leaves_list_unchanged(self, two_todos):
        result = delete_todo(two_todos, "nonexistent-id")
        assert len(result) == 2

    def test_delete_from_single_item_list(self):
        todos = add_todo([], "Only one")
        result = delete_todo(todos, todos[0].id)
        assert result == []

    def test_original_list_is_not_mutated(self, two_todos):
        delete_todo(two_todos, two_todos[0].id)
        assert len(two_todos) == 2
