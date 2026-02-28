"""Additional unit tests covering edge and boundary cases.

These tests cover:
- ItemRecord defaults and mutable attribute isolation
- ItemRecord created_at timezone handling (naive datetime)
- InteractionLog default created_at behavior
- _filter_by_item_id: no matches and multiple matches

"""

from datetime import datetime

from app.models.item import ItemRecord
from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def test_item_attributes_default_is_independent() -> None:
    """Each ItemRecord should get its own attributes dict (no shared mutable default)."""
    a = ItemRecord(id=1, title="A", description="a desc")
    b = ItemRecord(id=2, title="B", description="b desc")
    # mutate one instance
    a.attributes["x"] = 1
    # other instance should not see the change
    assert "x" not in b.attributes


def test_item_created_at_is_naive_datetime() -> None:
    """created_at should be a naive datetime (tzinfo is None) as implemented in the model."""
    item = ItemRecord(id=3, title="T", description="d")
    assert isinstance(item.created_at, datetime)
    assert item.created_at.tzinfo is None


def test_interactionlog_created_at_defaults_to_none() -> None:
    """When creating InteractionLog without created_at it remains None (explicit default)."""
    log = InteractionLog(id=1, learner_id=1, item_id=1, kind="view")
    assert log.created_at is None


def test_filter_by_item_id_returns_empty_when_no_matches() -> None:
    interactions = [
        InteractionLog(id=1, learner_id=1, item_id=10, kind="a"),
        InteractionLog(id=2, learner_id=2, item_id=11, kind="b"),
    ]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


def test_filter_by_item_id_returns_multiple_matches() -> None:
    interactions = [
        InteractionLog(id=1, learner_id=1, item_id=5, kind="a"),
        InteractionLog(id=2, learner_id=2, item_id=5, kind="b"),
        InteractionLog(id=3, learner_id=3, item_id=6, kind="c"),
    ]
    result = _filter_by_item_id(interactions, 5)
    assert len(result) == 2
    ids = {i.id for i in result}
    assert ids == {1, 2}
