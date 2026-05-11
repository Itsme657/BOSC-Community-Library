# Resource Index Performance Refactor

This refactor improves `ResourceIndex` search performance by maintaining internal lookup indexes for categories and tags.

- Category values are normalized and indexed on add.
- Tags are normalized and indexed for fast candidate selection.
- Search now prefilters by category/tag candidates before scanning results.

This change reduces the cost of repeated searches for large collections of community resources.
