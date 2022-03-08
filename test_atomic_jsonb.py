import pytest as pytest

from atomic_jsonb_set import atomic_jsonb_set
from models import Child, Parent, DBSession


@pytest.fixture(scope='function', autouse=True)
def setup():
    import transaction
    transaction.begin()
    yield
    transaction.abort()

def _create_obj(cls):
    model = cls()
    DBSession.add(model)
    DBSession.flush()
    return model


@pytest.fixture()
def parent():
    return _create_obj(Parent)


@pytest.fixture()
def child():
    return _create_obj(Child)


def test_can_update_parent_json_column(parent: Parent):
    atomic_jsonb_set(
        parent, dynamic_column_name="json_column", column_id="foo", value="bar"
    )
    assert parent.aliased_json_column["foo"] == "bar"
    assert parent.json_column["foo"] == "bar"


def test_can_update_child_json_column(child: Child):
    atomic_jsonb_set(
        child, dynamic_column_name="json_column", column_id="foo", value="bar"
    )
    assert child.aliased_json_column["foo"] == "bar"
    assert child.json_column["foo"] == "bar"


def test_can_update_with_synonym_column(parent: Parent):
    atomic_jsonb_set(
        parent, dynamic_column_name="aliased_json_column", column_id="foo", value="bar"
    )
    assert parent.aliased_json_column["foo"] == "bar"
    assert parent.json_column["foo"] == "bar"


def test_can_update_with_synonym_column_on_child(child: Child):
    atomic_jsonb_set(
        child, dynamic_column_name="aliased_json_column", column_id="foo", value="bar"
    )
    assert child.aliased_json_column["foo"] == "bar"
    assert child.json_column["foo"] == "bar"
