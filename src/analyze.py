"""Statistical analysis + figures from results/scored.csv.

Outputs: results/summary_table.csv, results/tests.csv, results/hypotheses.json, figures/*.png
"""
import json, os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

ROOT = os.path.join(os.path.dirname(__file__), "..")
RES, FIG = os.path.join(ROOT, "results"), os.path.join(ROOT, "figures")
TIERS = ["minimal", "concise", "standard", "detailed", "exhaustive"]
CONDS = TIERS + ["padded"]
TASKS = {"cls": "Classification (AG News, acc)", "ext": "Extraction (SQuAD, token F1)",
         "gen": "Generation (CNN/DM, ROUGE-L)", "rsn": "Reasoning (GSM8K, acc)"}
MODEL_ORDER = ["qwen2.5-0.5b", "qwen2.5-1.5b", "qwen2.5-3b", "qwen2.5-7b", "llama3.1-8b-awq", "qwen2.5-14b", "qwen2.5-32b-awq"]
PARAMS_B = {"qwen2.5-0.5b": 0.5, "qwen2.5-1.5b": 1.5, "qwen2.5-3b": 3, "qwen2.5-7b": 7, "llama3.1-8b-awq": 8,
            "qwen2.5-14b": 14, "qwen2.5-32b-awq": 32}
rng = np.random.default_rng(42)
B = int(os.environ.get("N_BOOT", 10000))


def wide(df, model, task, col="score"):
    """items x conditions matrix (rows aligned by item id)."""
    d = df[(df.model == model) & (df.task == task)]
    return d.pivot(index="id", columns="condition", values=col)[CONDS].astype(float)


def boot_ci(x, b=B):
    idx = rng.integers(0, len(x), (b, len(x)))
    m = x[idx].mean(1)
    return np.percentile(m, [2.5, 97.5])


def paired(a, b, b_=B):
    """Paired difference a-b: mean, 95% bootstrap CI, two-sided sign-flip permutation p."""
    d = a - b
    lo, hi = boot_ci(d, b_)
    obs = d.mean()
    flips = rng.choice([-1, 1], (b_, len(d)))
    null = (flips * d).mean(1)
    p = (np.sum(np.abs(null) >= abs(obs) - 1e-12) + 1) / (b_ + 1)
    return obs, lo, hi, p


def main():
    df = pd.read_csv(os.path.join(RES, "scored.csv"))
    df["compliant"] = df.compliant.astype(float)
    models = [m for m in MODEL_ORDER if m in df.model.unique()]

    # ---------------- summary table ----------------
    rows = []
    for m in models:
        for t in TASKS:
            W, C = wide(df, m, t), wide(df, m, t, "compliant")
            P = wide(df, m, t, "prompt_tokens")
            for c in CONDS:
                lo, hi = boot_ci(W[c].values)
                rows.append(dict(model=m, task=t, condition=c, n=len(W), score=W[c].mean(), ci_lo=lo, ci_hi=hi,
                                 compliance=C[c].mean(), prompt_tokens=P[c].mean()))
    summ = pd.DataFrame(rows)
    summ.to_csv(os.path.join(RES, "summary_table.csv"), index=False)

    # ---------------- planned paired comparisons ----------------
    comps = [("standard", "exhaustive"), ("standard", "minimal"), ("detailed", "standard"),
             ("concise", "minimal"), ("standard", "concise"), ("exhaustive", "detailed"),
             ("padded", "standard"), ("exhaustive", "padded")]
    tests = []
    for m in models:
        for t in TASKS:
            W, C = wide(df, m, t), wide(df, m, t, "compliant")
            for a, b in comps:
                for metric, M in [("score", W), ("compliance", C)]:
                    obs, lo, hi, p = paired(M[a].values, M[b].values)
                    tests.append(dict(model=m, task=t, metric=metric, comparison=f"{a}-{b}",
                                      diff=obs, ci_lo=lo, ci_hi=hi, p=p))
    tests = pd.DataFrame(tests)
    tests["p_holm"] = np.nan
    for metric in ["score", "compliance"]:  # Holm within each metric family
        mask = tests.metric == metric
        tests.loc[mask, "p_holm"] = multipletests(tests.loc[mask, "p"], method="holm")[1]
    tests.to_csv(os.path.join(RES, "tests.csv"), index=False)

    # ---------------- hypothesis-specific analyses ----------------
    H = {}
    sget = lambda m, t, c, col="score": float(summ[(summ.model == m) & (summ.task == t) & (summ.condition == c)][col].iloc[0])
    tget = lambda m, t, comp, metric="score": tests[(tests.model == m) & (tests.task == t) & (tests.comparison == comp) & (tests.metric == metric)].iloc[0].to_dict()

    # H1: classification & extraction peak at standard, drop 3-7 pts at exhaustive
    H["H1"] = {}
    for t in ["cls", "ext"]:
        for m in models:
            sc = {c: sget(m, t, c) for c in TIERS}
            tt = tget(m, t, "standard-exhaustive")
            H["H1"][f"{t}/{m}"] = dict(peak_tier=max(sc, key=sc.get), scores={k: round(v, 4) for k, v in sc.items()},
                                       std_minus_exh=round(tt["diff"], 4), ci=[round(tt["ci_lo"], 4), round(tt["ci_hi"], 4)],
                                       p_holm=round(tt["p_holm"], 4))

    # H2: generation monotone minimal->detailed: item-level slope over tier index (0..3), bootstrap over items
    H["H2"] = {}
    for m in models:
        W = wide(df, m, "gen")[TIERS[:4]].values
        x = np.arange(4) - 1.5
        slopes = (W - W.mean(1, keepdims=True)) @ x / (x @ x)
        lo, hi = boot_ci(slopes)
        steps = [tget(m, "gen", c) for c in ["concise-minimal", "standard-concise", "detailed-standard"]]
        H["H2"][m] = dict(slope_per_tier=round(slopes.mean(), 4), ci=[round(lo, 4), round(hi, 4)],
                          step_diffs=[round(s["diff"], 4) for s in steps],
                          step_p_holm=[round(s["p_holm"], 4) for s in steps],
                          strictly_monotone=bool(all(s["diff"] > 0 for s in steps)),
                          exhaustive_minus_detailed=round(tget(m, "gen", "exhaustive-detailed")["diff"], 4))

    # H3: reasoning insensitive beyond concise: Cochran's Q over concise..exhaustive + max |diff|,
    # and equivalence (90% bootstrap CI of each diff vs concise within +-3 pts)
    H["H3"] = {}
    for m in models:
        W = wide(df, m, "rsn")[TIERS[1:]].values
        k = W.shape[1]
        T, R = W.sum(0), W.sum(1)
        denom = k * R.sum() - (R ** 2).sum()
        Q = (k - 1) * (k * (T ** 2).sum() - T.sum() ** 2) / denom if denom > 0 else 0.0
        pq = float(stats.chi2.sf(Q, k - 1))
        eq = {}
        for j, c in enumerate(TIERS[2:], start=1):
            d = W[:, j] - W[:, 0]
            idx = rng.integers(0, len(d), (B, len(d)))
            lo, hi = np.percentile(d[idx].mean(1), [5, 95])
            eq[c] = dict(diff_vs_concise=round(d.mean(), 4), ci90=[round(lo, 4), round(hi, 4)],
                         equivalent_3pt=bool(lo > -0.03 and hi < 0.03))
        H["H3"][m] = dict(scores={c: round(float(v), 4) for c, v in zip(TIERS[1:], W.mean(0))},
                          cochran_Q=round(Q, 3), p=round(pq, 4), equivalence=eq,
                          minimal=round(sget(m, "rsn", "minimal"), 4))

    # H4: scale - drop (standard - exhaustive) larger for 7B than for 14B / 32B; diff-in-diff bootstrap
    H["H4"] = {}
    for t in TASKS:
        drops = {}
        for m in models:
            W = wide(df, m, t)
            drops[m] = W["standard"].values - W["exhaustive"].values
        out = {m: round(float(v.mean()), 4) for m, v in drops.items()}
        for big in ["qwen2.5-14b", "qwen2.5-32b-awq"]:
            if "qwen2.5-7b" in drops and big in drops:
                # same items -> paired bootstrap on the item-level interaction
                dd = drops["qwen2.5-7b"] - drops[big]
                obs, lo, hi, p = paired(dd, np.zeros_like(dd))
                out[f"DiD_7b_minus_{big}"] = dict(diff=round(obs, 4), ci=[round(lo, 4), round(hi, 4)], p=round(p, 4))
        qm = [m for m in models if m.startswith("qwen")]
        if len(qm) >= 3:
            r, p = stats.spearmanr([np.log(PARAMS_B[m]) for m in qm], [drops[m].mean() for m in qm])
            out["spearman_logsize_vs_drop_qwen"] = dict(rho=round(float(r), 3), p=round(float(p), 4))
        H["H4"][t] = out

    # H5: compliance peaks at standard
    H["H5"] = {}
    for t in TASKS:
        for m in models:
            cc = {c: sget(m, t, c, "compliance") for c in TIERS}
            best = max(cc.values())
            H["H5"][f"{t}/{m}"] = dict(peak=[c for c in TIERS if cc[c] == best], rates={k: round(v, 3) for k, v in cc.items()},
                                       std_minus_exh=round(tget(m, t, "standard-exhaustive", "compliance")["diff"], 4))

    # H6: padding control
    H["H6"] = {}
    for t in TASKS:
        for m in models:
            a, b = tget(m, t, "padded-standard"), tget(m, t, "exhaustive-padded")
            H["H6"][f"{t}/{m}"] = dict(padded_minus_standard=round(a["diff"], 4), p_holm_ps=round(a["p_holm"], 4),
                                       exhaustive_minus_padded=round(b["diff"], 4), p_holm_ep=round(b["p_holm"], 4))
    with open(os.path.join(RES, "hypotheses.json"), "w") as f:
        json.dump(H, f, indent=1)

    # ---------------- figures ----------------
    colors = plt.cm.viridis(np.linspace(0, 0.9, len(models)))
    for col, fname, ylab in [("score", "score_by_tier.png", "task score"), ("compliance", "compliance_by_tier.png", "format compliance rate")]:
        fig, axes = plt.subplots(1, 4, figsize=(19, 4.4))
        for ax, (t, title) in zip(axes, TASKS.items()):
            for m, cl in zip(models, colors):
                s = summ[(summ.model == m) & (summ.task == t)].set_index("condition").loc[TIERS]
                ax.plot(range(5), s[col], "-o", color=cl, label=m, ms=4)
                if col == "score":
                    ax.fill_between(range(5), s.ci_lo, s.ci_hi, color=cl, alpha=0.12)
                pv = summ[(summ.model == m) & (summ.task == t) & (summ.condition == "padded")][col].iloc[0]
                ax.plot(4.25, pv, "x", color=cl, ms=7)
            ax.set_xticks(list(range(5)) + [4.25])
            ax.set_xticklabels(["min", "conc", "std", "det", "exh", "pad"], fontsize=8)
            ax.set_title(title, fontsize=10)
            ax.set_xlabel("instruction tier (x = length-matched padded control)", fontsize=8)
            ax.grid(alpha=0.3)
        axes[0].set_ylabel(ylab)
        axes[-1].legend(fontsize=7, loc="lower right")
        plt.tight_layout()
        plt.savefig(os.path.join(FIG, fname), dpi=150)
        plt.close()

    # drop vs model size
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for t, mk in zip(TASKS, "osD^"):
        y = [tget(m, t, "standard-exhaustive")["diff"] * 100 for m in models]
        e = [[(tget(m, t, "standard-exhaustive")["diff"] - tget(m, t, "standard-exhaustive")["ci_lo"]) * 100 for m in models],
             [(tget(m, t, "standard-exhaustive")["ci_hi"] - tget(m, t, "standard-exhaustive")["diff"]) * 100 for m in models]]
        x = np.arange(len(models)) + {"cls": -0.15, "ext": -0.05, "gen": 0.05, "rsn": 0.15}[t]
        ax.errorbar(x, y, yerr=e, fmt=mk, capsize=3, label=t)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(models, rotation=25, fontsize=8)
    ax.set_ylabel("standard − exhaustive (points, 95% CI)\n>0 means exhaustive hurts")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, "drop_by_model.png"), dpi=150)
    plt.close()

    pd.set_option("display.width", 200)
    print(summ.pivot_table(index=["task", "model"], columns="condition", values="score")[CONDS].round(3))
    print(summ.pivot_table(index=["task", "model"], columns="condition", values="compliance")[CONDS].round(3))
    print(json.dumps(H, indent=1)[:6000])


if __name__ == "__main__":
    main()
