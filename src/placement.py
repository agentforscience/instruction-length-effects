"""Robustness: instruction in user turn (main) vs in system message (sys_*), same models/items.

Output: results/placement.csv and printed table.
"""
import os

import pandas as pd

ROOT = os.path.join(os.path.dirname(__file__), "..")
CONDS = ["minimal", "concise", "standard", "detailed", "exhaustive", "padded"]


def main():
    df = pd.read_csv(os.path.join(ROOT, "results", "scored.csv"))
    sys_models = sorted(m for m in df.model.unique() if m.startswith("sys_"))
    rows = []
    for sm in sys_models:
        base = sm[4:]
        for placement, m in [("user", base), ("system", sm)]:
            g = df[df.model == m].groupby(["task", "condition"])[["score", "compliant"]].mean().reset_index()
            g["model"], g["placement"] = base, placement
            rows.append(g)
    out = pd.concat(rows)
    out.to_csv(os.path.join(ROOT, "results", "placement.csv"), index=False)
    pd.set_option("display.width", 200)
    print(out.pivot_table(index=["model", "task", "placement"], columns="condition", values="score")[CONDS].round(3))
    print(out.pivot_table(index=["model", "task", "placement"], columns="condition", values="compliant")[CONDS].round(3))


if __name__ == "__main__":
    main()
