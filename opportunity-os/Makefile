.PHONY: install agents web db-up db-down pipeline test lint

install:
	cd apps/agents && pip install -e ".[dev]"
	cd apps/web && npm install

agents:
	cd apps/agents && uvicorn opportunity_os.api:app --reload --port 8000

web:
	cd apps/web && npm run dev

db-up:
	docker compose -f infra/docker-compose.yml up -d postgres redis

db-down:
	docker compose -f infra/docker-compose.yml down

# Example: make pipeline NICHE="sleep aid" GEO="US,UK,FR"
pipeline:
	cd apps/agents && python -m opportunity_os.cli pipeline \
		--niche "$(NICHE)" --geo "$(GEO)"

test:
	cd apps/agents && pytest -q

lint:
	cd apps/agents && ruff check .
	cd apps/web && npm run lint
