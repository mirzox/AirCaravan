
# init migration 
```alembic init alembic```

# create migration
```alembic revision --autogenerate -m "create table user"```

# upgrade
```alembic upgrade head```

# downgrade
```alembic downgrade -1```

# show history
```alembic history```

# show current
```alembic current```

