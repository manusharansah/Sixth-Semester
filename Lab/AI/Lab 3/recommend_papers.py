"""
Paper Recommendation System
----------------------------
Computes top-N similar papers for every paper in the literature network,
using Jaccard similarity over a feature set built from each paper's:
  - Title tokens (significant words from the title)
  - Author (from the AUTHORED edge)
  - Methodology (from the UTILIZED edge)

Output: paper_recommendations.json
"""

import json
import os
import re
from itertools import combinations

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "network_data.json")
output_path = os.path.join(script_dir, "paper_recommendations.json")

with open(input_path, "r") as f:
    data = json.load(f)

nodes = data["nodes"]
links = data["links"]

# Identify all paper nodes
paper_ids = [n["id"] for n in nodes if n["group"] == "Paper"]

# Common stopwords to exclude from title-based features
STOPWORDS = {
    "a", "an", "the", "of", "for", "in", "on", "via", "and", "to", "with",
    "is", "are", "at", "by", "from", "into", "as", "or", "scale", "v2", "v3"
}

def tokenize_title(title):
    """Extract lowercase, alphanumeric tokens from a title, excluding stopwords."""
    title_clean = re.sub(r"[^a-zA-Z0-9\s\-]", " ", title)
    tokens = re.split(r"[\s\-:]+", title_clean.lower())
    return {t for t in tokens if t and t not in STOPWORDS and len(t) > 2}

# Build feature sets: author and methodology per paper from edges
paper_author = {}
paper_methodology = {}

for link in links:
    src, tgt, label = link["source"], link["target"], link["label"]
    if label == "AUTHORED" and tgt in paper_ids:
        paper_author[tgt] = src
    elif label == "UTILIZED" and src in paper_ids:
        paper_methodology[src] = tgt

# Build a combined feature set for each paper:
#   title tokens + author (prefixed) + methodology (prefixed)
# Prefixes prevent accidental overlap between, e.g., a title word and an author name.
paper_features = {}
for pid in paper_ids:
    features = set(tokenize_title(pid))
    if pid in paper_author:
        features.add(f"author::{paper_author[pid]}")
    if pid in paper_methodology:
        features.add(f"methodology::{paper_methodology[pid]}")
    paper_features[pid] = features


def jaccard_similarity(set_a, set_b):
    """Jaccard Similarity = |Intersection| / |Union|"""
    if not set_a and not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union else 0.0


def explain_overlap(pid_a, pid_b):
    """Return human-readable shared features between two papers."""
    shared = paper_features[pid_a] & paper_features[pid_b]
    shared_authors = [s.replace("author::", "") for s in shared if s.startswith("author::")]
    shared_methods = [s.replace("methodology::", "") for s in shared if s.startswith("methodology::")]
    shared_words = sorted(s for s in shared if "::" not in s)

    reasons = []
    if shared_authors:
        reasons.append(f"same author ({', '.join(shared_authors)})")
    if shared_methods:
        reasons.append(f"same methodology ({', '.join(shared_methods)})")
    if shared_words:
        reasons.append(f"shared title concepts ({', '.join(shared_words)})")
    return reasons


# Compute pairwise similarity scores
TOP_N = 3
recommendations = {}

for pid in paper_ids:
    scores = []
    for other_id in paper_ids:
        if other_id == pid:
            continue
        sim = jaccard_similarity(paper_features[pid], paper_features[other_id])
        if sim > 0:
            scores.append((other_id, sim))

    # Sort by similarity (descending), then alphabetically for stable ordering
    scores.sort(key=lambda x: (-x[1], x[0]))
    top_matches = scores[:TOP_N]

    recommendations[pid] = [
        {
            "title": match_id,
            "similarity": round(sim, 3),
            "reasons": explain_overlap(pid, match_id)
        }
        for match_id, sim in top_matches
    ]

# Save recommendations
with open(output_path, "w") as f:
    json.dump(recommendations, f, indent=4)

print(f"Computed top-{TOP_N} recommendations for {len(paper_ids)} papers.")
print(f"Saved to: {output_path}")

# Print a small preview
print("\n--- Sample Recommendations ---")
for pid in paper_ids[:3]:
    print(f"\nPaper: {pid}")
    for rec in recommendations[pid]:
        reason_str = "; ".join(rec["reasons"]) if rec["reasons"] else "no shared features"
        print(f"  -> {rec['title']} (similarity: {rec['similarity']}) [{reason_str}]")