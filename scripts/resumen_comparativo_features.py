from pathlib import Path

import pandas as pd


BASE = Path("/home/munasqa/MAESTRIA/opencode")


def jaccard(a: set, b: set) -> float:
    u = a.union(b)
    if not u:
        return 0.0
    return len(a.intersection(b)) / len(u)


def compare_target(target: str, topk: int = 30) -> tuple[pd.DataFrame, dict]:
    hybrid = pd.read_csv(BASE / f"top30_consenso_{target}.csv")
    moes = pd.read_csv(BASE / f"ranking_moes_{target}.csv")
    pareto = pd.read_csv(BASE / f"pareto_moes_{target}.csv")

    hybrid_set = set(hybrid["feature"].head(topk).tolist())
    moes_set = set(moes["feature"].head(topk).tolist())

    rows = []
    for f in sorted(hybrid_set.union(moes_set)):
        rows.append(
            {
                "target": target,
                "feature": f,
                "in_hybrid_top30": int(f in hybrid_set),
                "in_moes_top30": int(f in moes_set),
                "in_both": int((f in hybrid_set) and (f in moes_set)),
            }
        )

    f1_best = 1.0 - float(pareto.iloc[0]["obj_error"])
    nfeat_best = int(pareto.iloc[0]["obj_nfeat"])

    summary = {
        "target": target,
        "hybrid_topk": topk,
        "moes_topk": topk,
        "intersection": len(hybrid_set.intersection(moes_set)),
        "jaccard": round(jaccard(hybrid_set, moes_set), 6),
        "moes_pareto_best_f1": round(f1_best, 6),
        "moes_pareto_best_nfeat": nfeat_best,
    }

    return pd.DataFrame(rows), summary


def main() -> None:
    targets = ["tipo_violencia", "nivel_riesgo_victima"]
    detail_frames = []
    summary_rows = []

    for t in targets:
        detail, summary = compare_target(t, topk=30)
        detail_frames.append(detail)
        summary_rows.append(summary)

    detail_df = pd.concat(detail_frames, ignore_index=True)
    summary_df = pd.DataFrame(summary_rows)

    detail_out = BASE / "detalle_interseccion_hibrido_moes.csv"
    summary_out = BASE / "resumen_comparativo_features.csv"

    detail_df.to_csv(detail_out, index=False)
    summary_df.to_csv(summary_out, index=False)

    print("Generado:", detail_out)
    print("Generado:", summary_out)
    print("\nResumen:")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
