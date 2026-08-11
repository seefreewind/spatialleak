"""Split result container with JSON serialization."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import List


@dataclass
class Split:
    name: str
    method: str
    params: dict
    seed: int
    train_idx: List[int]
    val_idx: List[int]
    test_idx: List[int]
    dropped_idx: List[int] = field(default_factory=list)

    def check_valid(self, n: int) -> None:
        """Assert disjointness and full coverage of indices."""
        sets = [set(self.train_idx), set(self.val_idx), set(self.test_idx), set(self.dropped_idx)]
        for i in range(len(sets)):
            for j in range(i + 1, len(sets)):
                assert sets[i].isdisjoint(sets[j]), f"{self.name}: overlapping sets {i},{j}"
        covered = set().union(*sets)
        assert covered == set(range(n)), f"{self.name}: coverage {len(covered)}/{n}"
        assert all(0 <= i < n for i in covered), f"{self.name}: index out of range"

    def save(self, path) -> None:
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)

    @staticmethod
    def load(path) -> "Split":
        with open(path) as f:
            d = json.load(f)
        return Split(**d)
