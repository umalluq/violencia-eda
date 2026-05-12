#!/usr/bin/env python3
"""
Pipeline ETL alineado al notebook EDA del proyecto.

Uso:
  python scripts/update_parquet_pipeline.py \
    --new-csv /ruta/nueva_data_2026.csv \
    --ubigeo-csv /home/munasqa/MAESTRIA/opencode/ubigeo_trabajar.csv \
    --base-parquet /home/munasqa/MAESTRIA/opencode/base_modelado.parquet \
    --out-parquet /home/munasqa/MAESTRIA/opencode/base_modelado.parquet
"""

from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd


def normalize_name(s: str) -> str:
    s = str(s).strip().lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols = [normalize_name(c) for c in df.columns]
    seen = {}
    out = []
    for c in cols:
        if c not in seen:
            seen[c] = 0
            out.append(c)
        else:
            seen[c] += 1
            out.append(f"{c}_{seen[c]}")
    df = df.copy()
    df.columns = out
    if "nivel_de_riesgo_victima" in df.columns and "nivel_riesgo_victima" not in df.columns:
        df = df.rename(columns={"nivel_de_riesgo_victima": "nivel_riesgo_victima"})
    return df


def clean_missing(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].astype(str).str.strip()
    df.replace(
        {
            "": pd.NA,
            "nan": pd.NA,
            "NaN": pd.NA,
            "none": pd.NA,
            "None": pd.NA,
            "null": pd.NA,
            "NULL": pd.NA,
            ".": pd.NA,
            "-": pd.NA,
            "*": pd.NA,
            "**": pd.NA,
        },
        inplace=True,
    )
    return df


def add_ubigeo(df: pd.DataFrame, ubigeo_csv: Path) -> pd.DataFrame:
    out = df.copy()
    ub = pd.read_csv(ubigeo_csv, dtype=str, low_memory=False)
    ub = normalize_columns(ub)

    for c in ["codigo_dpto", "codigo_prov", "codigo_dist"]:
        ub[c] = ub[c].astype(str).str.strip().str.zfill(2)

    ub["ubigeo_codigo"] = ub["codigo_dpto"] + ub["codigo_prov"] + ub["codigo_dist"]
    ub["ubigeo_nombre"] = (
        ub["dpto"].astype(str).str.strip()
        + " | "
        + ub["prov"].astype(str).str.strip()
        + " | "
        + ub["dist"].astype(str).str.strip()
    )
    ub_map = ub[["ubigeo_codigo", "ubigeo_nombre", "dpto", "prov", "dist"]].drop_duplicates()

    required = ["dpto_domicilio", "prov_domicilio", "dist_domicilio"]
    if not all(c in out.columns for c in required):
        return out

    for c in required:
        out[c] = out[c].astype(str).str.strip().replace({"<NA>": pd.NA}).str.zfill(2)

    mask = out[required].notna().all(axis=1)
    out["ubigeo_codigo"] = pd.NA
    out.loc[mask, "ubigeo_codigo"] = (
        out.loc[mask, "dpto_domicilio"]
        + out.loc[mask, "prov_domicilio"]
        + out.loc[mask, "dist_domicilio"]
    )

    for c in ["ubigeo_nombre", "dpto", "prov", "dist"]:
        if c in out.columns:
            out.drop(columns=[c], inplace=True)

    out = out.merge(ub_map, on="ubigeo_codigo", how="left")
    return out


def add_basic_types(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "fecha_ingreso" in out.columns:
        out["fecha_ingreso"] = pd.to_datetime(out["fecha_ingreso"], errors="coerce")
        out["anio"] = out["fecha_ingreso"].dt.year
        out["mes"] = out["fecha_ingreso"].dt.month
        out["anio_mes"] = out["fecha_ingreso"].dt.to_period("M").astype(str)

    for c in ["edad_victima", "edad_agresor", "hijas_vivas", "hijos_vivos"]:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def drop_high_null_columns(df: pd.DataFrame, threshold_pct: float = 99.0) -> tuple[pd.DataFrame, list[str]]:
    pct = df.isna().mean() * 100
    cols = pct[pct > threshold_pct].index.tolist()
    return df.drop(columns=cols), cols


def semantic_types(df: pd.DataFrame) -> dict[str, str]:
    numeric_real = {"edad_victima", "edad_agresor", "hijas_vivas", "hijos_vivos"}
    t = {}
    for c in df.columns:
        if c == "fecha_ingreso":
            t[c] = "fecha"
        elif c in {"anio", "mes"}:
            t[c] = "temporal_derivada"
        elif c in numeric_real:
            t[c] = "numerica_real"
        else:
            t[c] = "categorica_codificada"
    return t


def impute_by_semantic_type(df: pd.DataFrame, tmap: dict[str, str]) -> pd.DataFrame:
    out = df.copy()
    for c in out.columns:
        n_null = int(out[c].isna().sum())
        if n_null == 0:
            continue
        if tmap.get(c) in {"numerica_real", "temporal_derivada"}:
            out[c] = pd.to_numeric(out[c], errors="coerce")
            med = out[c].median()
            out[c] = out[c].fillna(med)
        elif tmap.get(c) == "fecha":
            out[c] = out[c].fillna(pd.Timestamp("1900-01-01"))
        else:
            out[c] = out[c].fillna("desconocido")
    return out


def drop_low_variance_binary(df: pd.DataFrame, tmap: dict[str, str], threshold_mode: float = 0.995) -> tuple[pd.DataFrame, list[str]]:
    low_cols = []
    for c in df.columns:
        if tmap.get(c) not in {"categorica_codificada", "numerica_real", "temporal_derivada"}:
            continue
        vc = df[c].value_counts(dropna=False)
        if len(vc) <= 2 and len(df[c]) > 0:
            p_top = vc.iloc[0] / len(df[c])
            if p_top >= threshold_mode:
                low_cols.append(c)
    return df.drop(columns=low_cols, errors="ignore"), low_cols


def remove_economic_domain(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str], int]:
    out = df.copy()
    n0 = len(out)

    if "tipo_violencia" in out.columns:
        tv = pd.to_numeric(out["tipo_violencia"], errors="coerce")
        out = out[tv != 0].copy()

    patterns = [
        "patrim",
        "econom",
        "ingreso",
        "salario",
        "alimentaria",
        "posesion",
        "tenencia",
        "recursos",
        "medios_indispensables",
    ]
    econ_cols = [c for c in out.columns if any(p in c for p in patterns) and c != "tipo_violencia"]
    out = out.drop(columns=econ_cols, errors="ignore")
    return out, econ_cols, (n0 - len(out))


def recode_targets_zero_based(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "tipo_violencia" in out.columns:
        out["tipo_violencia_orig"] = pd.to_numeric(out["tipo_violencia"], errors="coerce")
        out["tipo_violencia"] = out["tipo_violencia_orig"].map({1: 0, 2: 1, 3: 2})

    if "nivel_riesgo_victima" in out.columns:
        out["nivel_riesgo_victima_orig"] = pd.to_numeric(out["nivel_riesgo_victima"], errors="coerce")
        out["nivel_riesgo_victima"] = out["nivel_riesgo_victima_orig"] - 1
    return out


def align_to_base_schema(new_df: pd.DataFrame, base_df: pd.DataFrame) -> pd.DataFrame:
    out = new_df.copy()
    base_cols = list(base_df.columns)
    for c in base_cols:
        if c not in out.columns:
            out[c] = pd.NA
    out = out[base_cols]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--new-csv", required=True, help="CSV nuevo (ej. 2026)")
    ap.add_argument("--ubigeo-csv", required=True, help="Maestro ubigeo_trabajar.csv")
    ap.add_argument("--base-parquet", required=False, help="Parquet base actual")
    ap.add_argument("--out-parquet", required=True, help="Parquet de salida")
    args = ap.parse_args()

    new_csv = Path(args.new_csv)
    ubigeo_csv = Path(args.ubigeo_csv)
    out_parquet = Path(args.out_parquet)

    df = pd.read_csv(new_csv, dtype=str, low_memory=False)
    df = normalize_columns(df)
    df = clean_missing(df)
    df = add_ubigeo(df, ubigeo_csv)
    df = add_basic_types(df)

    df, dropped_null = drop_high_null_columns(df, threshold_pct=99.0)
    tmap = semantic_types(df)
    df = impute_by_semantic_type(df, tmap)
    df, low_var = drop_low_variance_binary(df, tmap, threshold_mode=0.995)
    df, econ_cols, rows_removed_econ = remove_economic_domain(df)

    if "nivel_de_riesgo_victima" in df.columns and "nivel_riesgo_victima" not in df.columns:
        df = df.rename(columns={"nivel_de_riesgo_victima": "nivel_riesgo_victima"})

    df = recode_targets_zero_based(df)

    if args.base_parquet and Path(args.base_parquet).exists():
        base = pd.read_parquet(args.base_parquet)
        if "nivel_de_riesgo_victima" in base.columns and "nivel_riesgo_victima" not in base.columns:
            base = base.rename(columns={"nivel_de_riesgo_victima": "nivel_riesgo_victima"})
        aligned = align_to_base_schema(df, base)
        final = pd.concat([base, aligned], ignore_index=True)
    else:
        final = df

    out_parquet.parent.mkdir(parents=True, exist_ok=True)
    final.to_parquet(out_parquet, index=False)

    print("--- ETL COMPLETADO ---")
    print(f"Filas nuevas procesadas: {len(df):,}")
    print(f"Filas removidas por tipo_violencia=0: {rows_removed_econ:,}")
    print(f"Columnas eliminadas por >99% nulos: {len(dropped_null)}")
    print(f"Columnas eliminadas por baja varianza: {len(low_var)}")
    print(f"Columnas economicas eliminadas: {len(econ_cols)}")
    print(f"Filas totales salida: {len(final):,}")
    print(f"Guardado en: {out_parquet}")


if __name__ == "__main__":
    main()
