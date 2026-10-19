How well do LLMs extract prerequisite relations between concepts, and how do papers measure it?

I have found:

ESCO-PrereqSkill: Evaluates models against expert-defined prerequisite links derived from standardized labor and educational taxonomies.
Curriculum & Knowledge Graphs: Extracting concept pairs (Concept A, Concept B) from textbooks, course descriptions, or scientific literature to test directed edges in a knowledge graph.
Pairwise Scoring: Feeding concept pairs into LLMs with specific instructions to output a continuous numerical score (e.g., ranging from -1 to 1) representing the likelihood or strength of a prerequisite dependency (A → B).
Zero-shot vs. Few-shot / Fine-tuned: Comparing models operating purely via natural language descriptions (zero-shot) against parameter-efficient fine-tuning or domain-specific relation classifiers.
