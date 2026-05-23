"""Acceptance tests for M5 Task 2 — tags stored on the note dict."""


def test_tags_parsed_into_list(client, app):
    app.notes.clear()
    client.post("/notes/new", data={
        "title": "T", "body": "B", "tags": "work, urgent, ideas",
    })
    assert app.notes[-1]["tags"] == ["work", "urgent", "ideas"]


def test_missing_tags_field_defaults_to_empty_list(client, app):
    app.notes.clear()
    client.post("/notes/new", data={"title": "T", "body": "B"})
    assert app.notes[-1]["tags"] == []


def test_tags_whitespace_and_empties_dropped(client, app):
    app.notes.clear()
    client.post("/notes/new", data={
        "title": "T", "body": "B", "tags": "  a , , b ",
    })
    assert app.notes[-1]["tags"] == ["a", "b"]


def test_every_note_has_tags_key(client, app):
    app.notes.clear()
    client.post("/notes/new", data={"title": "T", "body": "B"})
    assert "tags" in app.notes[-1]
