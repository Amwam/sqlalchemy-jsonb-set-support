from __future__ import annotations

import json

from sqlalchemy import func, inspect

from models import DeclarativeBase, DBSession


def atomic_jsonb_set(
    context: DeclarativeBase, dynamic_column_name: str, column_id, value,
):
    mapper = inspect(context.__class__)
    dynamic_column = getattr(context.__class__, dynamic_column_name)

    # We need to construct the query against the parent table
    query = DBSession.query(mapper.base_mapper.class_)

    # Filter by all the primary keys on the table
    for pk_col, pk_value in zip(
        mapper.primary_key, mapper.primary_key_from_instance(context)
    ):
        query = query.filter(pk_col == pk_value)

    query.update(
        {
            dynamic_column: func.jsonb_set(
                dynamic_column, f"{{{column_id}}}", json.dumps(value),
            )
        },
        synchronize_session="fetch",
    )
