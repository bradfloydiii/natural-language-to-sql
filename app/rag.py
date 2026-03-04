import math
from typing import List, Tuple

def tokenize(text: str) -> set[str]:
    return set(text.lower().split())

def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

class SimpleRAG:
    def __init__(self, docs: List[Tuple[str, str]]):
        # docs: (doc_id, content)
        self.docs = docs
        self.doc_tokens = [(doc_id, tokenize(content), content) for doc_id, content in docs]

    def retrieve(self, query: str, k: int = 3) -> List[Tuple[str, str, float]]:
        qt = tokenize(query)
        scored = []
        for doc_id, toks, content in self.doc_tokens:
            scored.append((doc_id, content, jaccard(qt, toks)))
        scored.sort(key=lambda x: x[2], reverse=True)
        return scored[:k]