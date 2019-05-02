#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

PID_FILE="$ROOT_DIR/.jupyter.pid"
LOG_FILE="$ROOT_DIR/.jupyter.log"
JUPYTER="$ROOT_DIR/.venv/bin/jupyter"

if [[ ! -x "$JUPYTER" ]]; then
	echo "Ambiente não encontrado. Rode: make configurar"
	exit 1
fi

if [[ -f "$PID_FILE" ]]; then
	old_pid="$(cat "$PID_FILE")"
	if kill -0 "$old_pid" 2>/dev/null; then
		echo "Jupyter já está em execução (PID $old_pid)"
		echo "Log: $LOG_FILE"
		exit 0
	fi
	rm -f "$PID_FILE"
fi

nohup "$JUPYTER" notebook mascaramento.ipynb >"$LOG_FILE" 2>&1 &
echo $! >"$PID_FILE"

# Aguarda a URL aparecer no log
url=""
for _ in $(seq 1 30); do
	if url="$(grep -oE 'http://127\.0\.0\.1:[0-9]+/[^ ]+' "$LOG_FILE" 2>/dev/null | head -n1)" && [[ -n "$url" ]]; then
		break
	fi
	sleep 0.2
done

echo "Jupyter iniciado (PID $(cat "$PID_FILE"))"
if [[ -n "$url" ]]; then
	echo "URL: $url"
fi
echo "Log: $LOG_FILE"
echo "Para encerrar: make parar"
