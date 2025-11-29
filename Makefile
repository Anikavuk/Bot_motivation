run:
	uv run app

migrate:
	uv run alembic upgrade head

create_migration_dev:
	@read -p "Введите описание ревизии: " msg; \
	uv run alembic revision --autogenerate -m "$$msg"

run_prod: migrate
	$(MAKE) run
