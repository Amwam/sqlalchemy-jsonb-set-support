from __future__ import annotations

import json

from sqlalchemy import func, inspect

from models import DeclarativeBase, DBSession


def atomic_jsonb_set(
    context: DeclarativeBase,
    dynamic_column_name: str,
    column_id,
    value,
):
    mapper = inspect(context.__class__)
    dynamic_column = getattr(context.__class__, dynamic_column_name)
    query = DBSession.query(dynamic_column)


    try:
        # needed for inheritance (persist_selectable is a Join)
        query = query.filter(mapper.persist_selectable.onclause)
    except AttributeError:
        # not a child class
        pass

    # filter by primary key
    id_key = [col for col in mapper.primary_key]
    for col in id_key:
        query = query.filter(col == getattr(context, col.name))

    query.update(
        {
            dynamic_column: func.jsonb_set(
                dynamic_column,
                f"{{{column_id}}}",
                json.dumps(value),
            )
        },
        synchronize_session="fetch",
    )
