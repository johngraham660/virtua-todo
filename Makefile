# Makefile for TODO Application

.PHONY: help dev build test clean docker-build docker-run k8s-deploy k8s-clean

# Default target
help:
	@echo "Available commands:"
	@echo "  dev           - Start development servers"
	@echo "  build         - Build frontend for production"
	@echo "  test          - Run tests"
	@echo "  clean         - Clean build artifacts"
	@echo "  docker-build  - Build Docker images"
	@echo "  docker-run    - Run with Docker Compose"
	@echo "  k8s-deploy    - Deploy to Kubernetes"
	@echo "  k8s-clean     - Remove from Kubernetes"

# Development
dev:
	@echo "Starting development servers..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:5173"
	@make -j2 dev-backend dev-frontend

dev-backend:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

# Build
build:
	cd frontend && npm run build

# Testing
test:
	cd backend && pytest
	@echo "Frontend tests not implemented yet"

# Clean
clean:
	cd frontend && rm -rf build dist node_modules/.cache
	cd backend && find . -type d -name __pycache__ -exec rm -rf {} +
	cd backend && find . -name "*.pyc" -delete

# Docker
docker-build:
	docker build -t todo-backend:latest ./backend
	docker build -t todo-frontend:latest ./frontend

docker-run:
	docker-compose up -d

# Kubernetes
k8s-deploy:
	kubectl apply -f k8s/

k8s-clean:
	kubectl delete -f k8s/ --ignore-not-found=true

# Install dependencies
install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install