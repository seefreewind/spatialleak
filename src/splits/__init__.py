"""Split framework: random / matched spatial block / slide / patient / dataset held-out.

All splits operate on a pandas DataFrame `obs` with columns:
  barcode, slide, patient, array_row, array_col, pxl_col_in_fullres, pxl_row_in_fullres
plus optional `layer`, `total_counts`. Indices refer to rows of `obs`.
"""
from .base import Split
from .group_split import group_held_out_split
from .matched_block_split import matched_block_split
from .random_split import random_spot_split
from .stratified_split import stratified_spot_split

__all__ = [
    "Split",
    "random_spot_split",
    "matched_block_split",
    "group_held_out_split",
    "stratified_spot_split",
]
