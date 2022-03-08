
Demo project for SQLAlchemy issue

This has a demo function that using jsonb_set to update a jsonb column keypair.

The code was previously working on SQLAlchemy 1.3, but now fails with 1.4

The issue being returned is:
```python
sqlalchemy.exc.ArgumentError: subject table for an INSERT, UPDATE or DELETE expected, 
    got Column('json_column', JSONB(astext_type=Text()), table=<parent_table>, nullable=False, default=ColumnDefault({})).
```



## Setup
There is a docker compose file, to launch a postgres DB.
Tests can be run using Tox (`$ tox`), in a python 3.9 environment.
Tox is configured to run the tests with SQLAlchemy 1.3 and 1.4