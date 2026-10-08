.PHONY: setup audit cv train api web test lint verify

setup:
	pip install -r requirements.txt

audit:
	python -m ml.preprocessing.audit

cv:
	python -m ml.training.cv

train:
	python -m ml.training.train

api:
	uvicorn backend.app.main:app --reload --port 8000

web:
	cd frontend && npm run dev

test:
	pytest && cd frontend && npm run test

lint:
	ruff check . && black --check .

verify:
	make lint && make test && python scripts/verify_phase.py --all
