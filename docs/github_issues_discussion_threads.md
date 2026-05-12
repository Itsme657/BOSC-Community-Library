# GitHub Issues - Five-Issue Mastery Challenge

This document provides the content for five GitHub Issues that serve as open discussion threads for the Phase 3 mastery challenge. Create these issues on GitHub using the repository's issue creation interface.

---

## Issue 1: BUG — ResourceIndex.search() fails with case-insensitive category/tag filters

**Title:** ResourceIndex.search() fails with case-insensitive category/tag filters

**Labels:** `bug`, `functional-bug`

**Description:**

### Problem
The `ResourceIndex.search()` method does not properly handle case-insensitive filtering for categories and tags. When searching with filters like `category="documentation"` against a resource with `category="Documentation"`, the search fails to match because the comparison is case-sensitive.

### Expected Behavior
- Category filtering should be case-insensitive
- Tag filtering should be case-insensitive
- Search queries should be case-insensitive

### Current Behavior
- Resources with different-cased category/tag values are incorrectly excluded

### Acceptance Criteria
- ✅ ResourceIndex normalizes category text to lowercase before comparison
- ✅ ResourceIndex normalizes tag text to lowercase before comparison
- ✅ Test `test_resource_index_search_filters_category_and_tags_case_insensitive` passes
- ✅ All existing tests continue to pass

**Branch:** `issue/bug-search-filter`

**Related PR:** Merged to main via merge commit

---

## Issue 2: BUG — ResourceIndex.search() does not search by resource_id

**Title:** ResourceIndex.search() does not search by resource_id

**Labels:** `bug`, `functional-bug`

**Description:**

### Problem
Users cannot find resources by their resource ID using the `search()` method. The full-text search only includes title, description, category, and tags, but not the resource_id field.

### Example
```python
index.add_resource(
    Resource(
        resource_id="find-me",
        title="Example",
        url="https://example.com",
        category="Tools",
    )
)

results = index.search(query="find-me")  # Should find 1 result, but finds 0
```

### Expected Behavior
- Searching for a resource's ID should locate the resource
- resource_id should be included in the full-text search field

### Acceptance Criteria
- ✅ resource_id is included in the searchable text pool
- ✅ Test `test_resource_index_search_by_resource_id` passes
- ✅ All existing tests continue to pass

**Branch:** `issue/bug-resource-id-search`

**Related PR:** Merged to main via merge commit

---

## Issue 3: FEATURE — Add searchable resource database

**Title:** Add searchable resource database with Resource and ResourceIndex classes

**Labels:** `enhancement`, `feature-enhancement`

**Description:**

### Goal
Implement a lightweight searchable resource collection system to help contributors discover and manage community resources.

### Requirements
- Create a `Resource` dataclass to represent individual resources
  - Fields: resource_id, title, url, category, tags, locale, description, translations
  - Include validation for required fields and URL format
  - Support localized titles and descriptions
- Create a `ResourceIndex` class to manage a collection of resources
  - Support adding resources with duplicate detection
  - Support full-text search by query string
  - Support filtering by category and tags
  - Support locale-aware search for multi-language content

### Acceptance Criteria
- ✅ `Resource` class is exportable from the main package
- ✅ `ResourceIndex` class is exportable from the main package
- ✅ Resource validation rejects invalid URLs, empty titles, etc.
- ✅ ResourceIndex prevents duplicate resource IDs
- ✅ Full-text search works across title, description, category, and tags
- ✅ Tests cover basic operations and error handling

**Branch:** `issue/feature-searchable-resource-db`

**Related PR:** Merged to main via merge commit

---

## Issue 4: FEATURE — Add localized resource support

**Title:** Add localized resource support with translation-aware search

**Labels:** `enhancement`, `feature-enhancement`, `internationalization`

**Description:**

### Goal
Enable contributors to manage resources in multiple languages and search across translations.

### Requirements
- Extend `Resource` to support translations for title and description
- Add a `translations` field: `dict[str, dict[str, str]]` mapping locale -> {title, description}
- Add methods:
  - `localized_title(locale)` — return title in requested locale or fall back to default
  - `localized_description(locale)` — return description in requested locale or fall back to default
- Update `ResourceIndex.search()` to use localized text when searching in a specific locale
- Fall back to the default text when the requested locale translation is unavailable
- Support a fixed set of locales: `en`, `es`, `fr`, `pt`
- Validate that resources use only supported locales

### Example
```python
resource = Resource(
    resource_id="sec-check",
    title="Security Checklist",
    url="https://example.com/security",
    category="Tools",
    locale="en",
    translations={
        "es": {
            "title": "Lista de verificación de seguridad",
            "description": "Guía para revisar los controles de seguridad.",
        }
    },
)

# Search in Spanish locale
results = index.search(query="seguridad", locale="es")
```

### Acceptance Criteria
- ✅ Resources support multi-language translations
- ✅ Localized search respects the requested locale
- ✅ Test `test_resource_index_localized_search_uses_translations` passes
- ✅ Documentation includes localization examples

**Branch:** `issue/feature-localized-resource-support`

**Related PR:** Merged to main via merge commit

---

## Issue 5: REFACTOR/MAINTENANCE — Optimize ResourceIndex search performance

**Title:** Optimize ResourceIndex search performance with internal category/tag indexes

**Labels:** `refactor`, `maintenance`, `performance`

**Description:**

### Problem
For large collections of resources, `ResourceIndex.search()` performs a full linear scan of all resources even when filtering by category or tag. This is inefficient and doesn't scale well.

### Solution
Implement internal normalized lookup indexes for categories and tags:
- Maintain `_resources_by_category: dict[str, set[str]]` mapping normalized category -> resource IDs
- Maintain `_resources_by_tag: dict[str, set[str]]` mapping normalized tag -> resource IDs
- Update indexes when resources are added
- Use indexes to prefilter candidates before scanning full-text search

### Performance Impact
- Category/tag filtering becomes O(1) lookup instead of O(n) scan
- Query filtering is applied to a candidate set instead of all resources
- Large collections now scale logarithmically instead of linearly

### Acceptance Criteria
- ✅ Category and tag indexes are created during resource addition
- ✅ Search prefilters using indexes before full-text search
- ✅ Test `test_resource_index_search_with_category_and_tag_indexes` verifies performance
- ✅ All existing tests pass with the new implementation
- ✅ No public API changes — refactor is internal

**Branch:** `issue/refactor-package-structure`

**Related PR:** Merged to main via merge commit

---

## How to Create These Issues on GitHub

1. Go to: https://github.com/Itsme657/BOSC-Community-Library/issues
2. Click "New Issue"
3. Copy the title and description from each section above
4. Add the labels listed
5. Click "Submit new issue"

Alternatively, if you have the GitHub CLI installed:

```bash
# Issue 1
gh issue create --title "BUG — ResourceIndex.search() fails with case-insensitive category/tag filters" \
  --body "$(cat issue_1_description.md)" \
  --label "bug,functional-bug"

# (Repeat for issues 2-5)
```

---

**Summary:**
These five issues serve as open discussion threads for the Phase 3 mastery challenge, documenting all functional bugs, feature enhancements, and maintenance improvements implemented in the repository.
