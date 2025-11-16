.PHONY: help build up down restart logs test clean

help:
	@echo "AI Code Assistant - Comandos disponíveis:"
	@echo ""
	@echo "  make build     - Build dos containers Docker"
	@echo "  make up        - Inicia os serviços"
	@echo "  make down      - Para os serviços"
	@echo "  make restart   - Reinicia os serviços"
	@echo "  make logs      - Exibe logs dos serviços"
	@echo "  make test      - Executa todos os testes"
	@echo "  make clean     - Remove containers e volumes"
	@echo "  make dev       - Modo desenvolvimento"
	@echo ""

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Serviços iniciados!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/api/v1/docs"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

test:
	@echo "Executando testes do backend..."
	cd backend && pytest --cov=app
	@echo ""
	@echo "Executando testes do frontend..."
	cd frontend && npm test

clean:
	docker-compose down -v
	rm -rf backend/__pycache__
	rm -rf backend/.pytest_cache
	rm -rf frontend/node_modules
	rm -rf frontend/dist

dev:
	@echo "Iniciando modo desenvolvimento..."
	docker-compose up
