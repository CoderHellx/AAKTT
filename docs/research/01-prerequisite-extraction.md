How well do LLMs extract prerequisite relations between concepts, and how do papers measure it?

I have found:

ESCO-PrereqSkill: Evaluates models against expert-defined prerequisite links derived from standardized labor and educational taxonomies.
Curriculum & Knowledge Graphs: Extracting concept pairs (Concept A, Concept B) from textbooks, course descriptions, or scientific literature to test directed edges in a knowledge graph.
Pairwise Scoring: Feeding concept pairs into LLMs with specific instructions to output a continuous numerical score (e.g., ranging from -1 to 1) representing the likelihood or strength of a prerequisite dependency (A → B).
Zero-shot vs. Few-shot / Fine-tuned: Comparing models operating purely via natural language descriptions (zero-shot) against parameter-efficient fine-tuning or domain-specific relation classifiers.

## Datasets

- **LectureBank** (Yale LILY): https://github.com/Yale-LILY/LectureBank
  Lecture files on NLP/ML/AI topics, with expert-annotated prerequisite relations between concepts. Candidate gold set for our graph-quality evals (Phase 1, milestone 4).

## Metrics we'll use (decided 2026-10-19)

All of them, because they answer different questions:

| Metric | Needs | Answers |
|---|---|---|
| Precision (edges) | Predicted edges vs. gold edges | "Of the prerequisites the LLM claimed, how many are real?" |
| Recall (edges) | Same | "Of the real prerequisites, how many did the LLM find?" |
| F1 | Precision + recall | One number that balances both |
| AUC | A **score** per concept pair (pairwise scoring) | "Does the model rank true prerequisite pairs above false ones?" (independent of any threshold) |

Note: precision, recall and F1 work on a generated graph directly. AUC only becomes available once we add pairwise edge scoring.
