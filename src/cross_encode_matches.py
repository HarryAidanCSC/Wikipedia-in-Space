from sentence_transformers import CrossEncoder
import numpy as np


def find_best_matches(
    model: CrossEncoder, target: str, candidates: list[str], top_n: int = 5
) -> list[tuple[str, float]]:
    pairs = [[target, cand] for cand in candidates]

    scores = model.predict(pairs)

    exp_scores = np.exp(scores - np.max(scores))
    probabilities = exp_scores / exp_scores.sum()

    results = sorted(zip(candidates, probabilities), key=lambda x: x[1], reverse=True)[
        :top_n
    ]

    return results
