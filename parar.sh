#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

PID_FILE="$ROOT_DIR/.jupyter.pid"

if [[ ! -f "$PID_FILE" ]]; then
	echo "Jupyter não está em execução"
	exit 0
fi

pid="$(cat "$PID_FILE")"
if kill -0 "$pid" 2>/dev/null; then
	# Encerra o processo e filhos do Jupyter
	pkill -P "$pid" 2>/dev/null || true
	kill "$pid" 2>/dev/null || true
	for _ in 1 2 3 4 5; do
		kill -0 "$pid" 2>/dev/null || break
		sleep 0.2
	done
	if kill -0 "$pid" 2>/dev/null; then
		kill -9 "$pid" 2>/dev/null || true
	fi
	echo "Jupyter parado (PID $pid)"
else
	echo "Processo $pid não encontrado"
fi

rm -f "$PID_FILE"
