# Makefile for SafeLink full-stack app

.PHONY: dev backend frontend db migrate test

dev:
	cd backend && flask run & cd ../frontend && npm run dev

backend:
	cd backend && flask run

frontend:
	cd frontend && npm run dev

db:
	docker-compose up db

migrate:
	cd backend && flask db migrate && flask db upgrade

test:
	cd backend && pytest 