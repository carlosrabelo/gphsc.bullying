#!/usr/bin/env python3
"""Formata e padroniza dados/original.csv sem remover respostas."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent
CSV_PATH = ROOT_DIR / "dados" / "original.csv"
BAK_PATH = ROOT_DIR / "dados" / "original.csv.bak"
EXEMPLO_PATH = ROOT_DIR / "dados" / "original.csv.exemplo"

EMPTY_FORM_COLUMNS = {
    "Digite o código de acesso.1",
    "Digite o código de acesso.2",
}

ORIENTACAO_MAP = {
    "heterossexual": "Heterossexual",
    "bissexual": "Bissexual",
    "homossexual": "Homossexual",
    "pansexual": "Pansexual",
}

ESCOLARIDADE_MAP = {
    "doutorado": "Doutorado",
    "mestrado": "Mestrado",
    "phd": "Phd",
    "pós graduação": "Pós Graduação",
    "pos graduacao": "Pós Graduação",
    "ensino médio": "Ensino Médio",
    "ensino medio": "Ensino Médio",
    "ensino fundamental": "Ensino Fundamental",
    "superior": "Superior",
}


def collapse_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def is_empty(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and pd.isna(value):
        return True
    return str(value).strip() == "" or str(value).lower() == "nan"


def clean_text(value: object) -> str:
    if is_empty(value):
        return ""
    return collapse_spaces(str(value))


def normalize_idade(value: object) -> str:
    if is_empty(value):
        return ""
    match = re.search(r"(\d+)", str(value))
    return match.group(1) if match else ""


def normalize_orientacao(value: object) -> str:
    if is_empty(value):
        return ""
    text = collapse_spaces(str(value))
    key = text.casefold()
    if key in ORIENTACAO_MAP:
        return ORIENTACAO_MAP[key]
    # Demais valores: só formatação leve (title case se estiver em CAPS total)
    if text.isupper():
        return text.title()
    if text.islower():
        return text.capitalize()
    return text


def normalize_escolaridade(value: object) -> str:
    if is_empty(value):
        return ""
    text = collapse_spaces(str(value))
    key = text.casefold().replace("á", "a").replace("é", "e").replace("í", "i")
    key = key.replace("ó", "o").replace("ú", "u").replace("ã", "a").replace("õ", "o")
    key = key.replace("ç", "c")
    if key in ESCOLARIDADE_MAP:
        return ESCOLARIDADE_MAP[key]
    if text.isupper() and len(text) > 2:
        return text.title()
    return text


def normalize_datetime(value: object) -> str:
    if is_empty(value):
        return ""
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return collapse_spaces(str(value))
    return parsed.strftime("%Y-%m-%d %H:%M:%S")


def main() -> int:
    if not CSV_PATH.exists():
        print(f"Arquivo não encontrado: {CSV_PATH}", file=sys.stderr)
        print("Coloque o CSV local em dados/original.csv e tente de novo.", file=sys.stderr)
        return 1

    before = pd.read_csv(CSV_PATH, encoding="utf-8", dtype=str, keep_default_na=False)
    rows_before, cols_before = before.shape

    shutil.copy2(CSV_PATH, BAK_PATH)

    df = before.copy()
    df.columns = [collapse_spaces(str(c)) for c in df.columns]

    drop_cols = [c for c in df.columns if c in EMPTY_FORM_COLUMNS]
    if drop_cols:
        df = df.drop(columns=drop_cols)

    for col in df.columns:
        df[col] = df[col].map(clean_text)

    idade_before = df["Idade:"].copy() if "Idade:" in df.columns else None
    if "Idade:" in df.columns:
        df["Idade:"] = df["Idade:"].map(normalize_idade)

    if "Orientação sexual" in df.columns:
        df["Orientação sexual"] = df["Orientação sexual"].map(normalize_orientacao)

    for col in ("Escolaridade da mãe:", "Escolaridade do pai:"):
        if col in df.columns:
            df[col] = df[col].map(normalize_escolaridade)

    if "Carimbo de data/hora" in df.columns:
        df["Carimbo de data/hora"] = df["Carimbo de data/hora"].map(normalize_datetime)

    df.to_csv(CSV_PATH, index=False, encoding="utf-8")

    # Cabeçalho de esquema versionável (sem respostas)
    pd.DataFrame(columns=df.columns).to_csv(EXEMPLO_PATH, index=False, encoding="utf-8")

    rows_after, cols_after = df.shape
    idade_norm = 0
    if idade_before is not None:
        idade_norm = int((idade_before != df["Idade:"]).sum())

    print("Limpeza concluída")
    print(f"  backup: {BAK_PATH.relative_to(ROOT_DIR)}")
    print(f"  exemplo: {EXEMPLO_PATH.relative_to(ROOT_DIR)}")
    print(f"  linhas: {rows_before} → {rows_after}")
    print(f"  colunas: {cols_before} → {cols_after}")
    if drop_cols:
        print(f"  colunas de formulário vazias removidas: {', '.join(drop_cols)}")
    print(f"  idades ajustadas: {idade_norm}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
