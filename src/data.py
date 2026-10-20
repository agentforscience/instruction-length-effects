"""Build fixed evaluation samples (n per task, seed 42) from the local HF cache -> datasets/*.jsonl."""
import glob, json, os, random
import pandas as pd

HUB = os.environ.get("HF_HUB_CACHE", "/data/transformers/hub")
N = int(os.environ.get("N_ITEMS", 250))
SEED = 42
OUT = os.path.join(os.path.dirname(__file__), "..", "datasets")
AG_LABELS = ["World", "Sports", "Business", "Sci/Tech"]


def pq(pattern):
    files = sorted(glob.glob(os.path.join(HUB, pattern)))
    assert files, pattern
    return pd.read_parquet(files[0])


def main():
    os.makedirs(OUT, exist_ok=True)
    # Classification: AG News test, stratified (N/4 per class)
    ag = pq("datasets--fancyzhx--ag_news/snapshots/*/data/test-*.parquet")
    ag = ag.groupby("label").sample(n=N // 4, random_state=SEED)
    cls = [{"id": f"ag{i}", "input": r.text, "label": AG_LABELS[r.label]} for i, r in ag.iterrows()]
    # Extraction: SQuAD v1.1 validation, one question per passage
    sq = pq("datasets--rajpurkar--squad/snapshots/*/plain_text/validation-*.parquet")
    sq = sq.drop_duplicates("context").sample(N, random_state=SEED)
    ext = [{"id": r.id, "context": r.context, "question": r.question,
            "answers": list(dict.fromkeys(r.answers["text"].tolist()))} for _, r in sq.iterrows()]
    # Generation: CNN/DailyMail test; articles truncated to 500 words to bound prompt length
    cnn = pq("datasets--abisee--cnn_dailymail/snapshots/*/3.0.0/test-*.parquet").sample(N, random_state=SEED)
    gen = [{"id": r.id, "input": " ".join(r.article.split()[:500]), "reference": r.highlights}
           for _, r in cnn.iterrows()]
    # Reasoning: GSM8K test
    gs = pq("datasets--openai--gsm8k/snapshots/*/main/test-*.parquet").sample(N, random_state=SEED)
    rsn = [{"id": f"gsm{i}", "input": r.question, "answer": r.answer.split("####")[-1].strip().replace(",", "")}
           for i, r in gs.iterrows()]
    for name, rows in [("cls", cls), ("ext", ext), ("gen", gen), ("rsn", rsn)]:
        rng = random.Random(SEED); rng.shuffle(rows)
        with open(os.path.join(OUT, f"{name}.jsonl"), "w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        print(name, len(rows), json.dumps(rows[0])[:300])


if __name__ == "__main__":
    main()
