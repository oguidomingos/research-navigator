#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v docker >/dev/null 2>&1; then
  echo "Erro: Docker nao encontrado. Instale Docker Desktop para subir backend/db/redis."
  exit 1
fi

cd "$ROOT_DIR"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Arquivo .env criado a partir de .env.example"
fi

docker compose up -d

echo "Backend: http://localhost:8000/docs"
echo "Agora rode o frontend:"
echo "  cd frontend && [ -f .env ] || cp .env.example .env && npm install && npm run dev"
