"""Error analysis / behavioural diagnostics by tier: output lengths, failure categories, examples.

Outputs: results/diagnostics.csv, results/error_examples.md
"""
import json, os, sys
from collections import Counter

import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
import score as S  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
CONDS = ["minimal", "concise", "standard", "detailed", "exhaustive", "padded"]


def categorize(task, out, item):
    """Coarse failure category for an incorrect / non-compliant output."""
    if task == "cls":
        p = S.cls_pred(out)
        if p is None:
            return "no_label"
        if not S.cls_compliant(out):
            return "extra_text"
        return f"confused:{item['label']}->{p}"
    if task == "ext":
        c = S.ext_clean(out)
        if not S.ext_compliant(out, item["context"]):
            return "not_verbatim_or_multiline"
        gl = min(len(g.split()) for g in item["answers"])
        if len(c.split()) > gl + 2:
            return "span_too_long"
        if len(c.split()) < gl:
            return "span_too_short"
        return "wrong_span"
    if task == "gen":
        n = len(out.split())
        if n > 80:
            return "over_80_words"
        k = len(S.sentences(out))
        if k < 2 or k > 4:
            return f"sentence_count_{k}"
        return "format_other"
    if task == "rsn":
        if not S.rsn_compliant(out):
            return "format_noncompliant"
        return "wrong_number"


def main():
    items = S.load_items()
    sc = pd.read_csv(os.path.join(ROOT, "results", "scored.csv"))
    rows, examples = [], []
    for fn in sorted(os.listdir(os.path.join(ROOT, "results", "raw"))):
        if "_pilot" in fn:
            continue
        tag = fn[:-6]
        recs = [json.loads(l) for l in open(os.path.join(ROOT, "results", "raw", fn))]
        for r in recs:
            r["model"] = tag
        df = pd.DataFrame(recs).merge(sc[["model", "task", "condition", "id", "score", "compliant"]],
                                      on=["model", "task", "condition", "id"])
        for (t, c), g in df.groupby(["task", "condition"]):
            cats = Counter()
            for _, r in g.iterrows():
                bad = (r.score < 1.0 if t in ("cls", "rsn") else False) or not r.compliant
                if t == "ext":
                    bad = r.score < 0.5 or not r.compliant
                if bad:
                    cats[categorize(t, r.output, items[(t, r.id)])] += 1
            rows.append(dict(model=tag, task=t, condition=c, mean_output_tokens=g.output_tokens.mean(),
                             truncated_rate=(g.finish_reason == "length").mean(),
                             mean_output_words=g.output.str.split().str.len().mean(),
                             top_failures="; ".join(f"{k}:{v}" for k, v in cats.most_common(4))))
        # paired examples where standard right and exhaustive wrong (cls/ext/rsn)
        for t in ["cls", "ext", "rsn"]:
            a = df[(df.task == t) & (df.condition == "standard")].set_index("id")
            b = df[(df.task == t) & (df.condition == "exhaustive")].set_index("id")
            flip = [i for i in a.index if a.loc[i, "score"] >= 0.99 and b.loc[i, "score"] < 0.5][:2]
            for i in flip:
                examples.append(f"### {tag} / {t} / {i}: standard correct, exhaustive wrong\n"
                                f"- gold: `{items[(t, i)].get('label') or items[(t, i)].get('answers') or items[(t, i)].get('answer')}`\n"
                                f"- standard: `{a.loc[i, 'output'][-250:]!r}`\n"
                                f"- exhaustive: `{b.loc[i, 'output'][-250:]!r}`\n")
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(ROOT, "results", "diagnostics.csv"), index=False)
    with open(os.path.join(ROOT, "results", "error_examples.md"), "w") as f:
        f.write("# Paired flips: standard correct -> exhaustive wrong\n\n" + "\n".join(examples))
    pd.set_option("display.width", 250, "display.max_colwidth", 120, "display.max_rows", 500)
    print(out.pivot_table(index=["task", "model"], columns="condition", values="mean_output_words")[CONDS].round(1))
    print(out[["model", "task", "condition", "top_failures"]].to_string())


if __name__ == "__main__":
    main()
