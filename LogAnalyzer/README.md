# Alembic revisions generate and deploy

docker compose up -d postgres

DATABASE_URL=postgresql://ci_ai_user:ci_ai_password@localhost:5432/ci_ai_db \
  alembic revision --autogenerate -m "init tables"

DATABASE_URL=postgresql://ci_ai_user:ci_ai_password@localhost:5432/ci_ai_db \
  alembic upgrade head

PGPASSWORD=ci_ai_password psql -h localhost -U ci_ai_user -d ci_ai_db -c "\dt"