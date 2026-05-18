# AGENTS Notes

## Scope and source of truth
- This repo is notebook-first. The active workflow is in `seleccion_caracteristicas_multimetodo_FULL.ipynb` (not the non-FULL notebook).
- Current operational context is tracked in `ESTADO_ACTUAL.md`; check it before editing parameters.
- Methodology rationale and citations live in `marco_metodologico_algoritmos.md`.

## High-value commands
- ETL refresh (official pipeline):
  - `python scripts/update_parquet_pipeline.py --new-csv /ruta/nueva_data.csv --ubigeo-csv /home/munasqa/MAESTRIA/opencode/ubigeo_trabajar.csv --base-parquet /home/munasqa/MAESTRIA/opencode/base_modelado.parquet --out-parquet /home/munasqa/MAESTRIA/opencode/base_modelado.parquet`
- Hybrid vs MOES comparison summary:
  - `python scripts/resumen_comparativo_features.py`

## Repo-specific modeling constraints
- Targets are zero-based classes (`tipo_violencia`, `nivel_riesgo_victima`).
- Always exclude leakage columns from feature sets:
  - direct/derived targets (`tipo_violencia`, `nivel_riesgo_victima`, `*_orig`, `*_lbl`, obvious proxies).
- Current MOES settings expected by project docs/results:
  - `SAMPLE_SIZE=50000`, seeds `42/52/62`, `min_features=8`, `n_generations=10`, `pop_size=40`.

## Expected artifacts after FULL notebook run
- Hybrid outputs: `ranking_cv_*`, `ranking_mi_*`, `ranking_rfimp_*`, `ranking_perm_*`, `ranking_rfe_*`, `top30_consenso_*`.
- MOES outputs: `ranking_moes_*`, `pareto_moes_*`.
- Comparison outputs: `resumen_comparativo_features.csv`, `detalle_interseccion_hibrido_moes.csv`.

## Important implementation quirks
- `scripts/resumen_comparativo_features.py` uses a hardcoded absolute base path (`/home/munasqa/MAESTRIA/opencode`). If run elsewhere, update `BASE` first.
- Large raw data/parquet are intentionally ignored via `.gitignore` (`BD_2020-2025.csv`, `*.parquet`, `base_modelado_particionado/`).

## Commit hygiene for this repo
- Stage intentionally; workspace often contains local-only files (for example `.obsidian/`, `.~lock.*`, and deleted debug images) that should not be committed unless explicitly requested.
