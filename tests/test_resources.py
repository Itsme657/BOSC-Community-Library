from src import Resource, ResourceIndex
import json


def test_resource_index_search_by_keyword_and_tags():
    index = ResourceIndex()
    index.add_resource(
        Resource(
            resource_id="r1",
            title="Community Mesh Guide",
            url="https://example.com/mesh",
            category="Documentation",
            tags=("mesh", "community"),
            description="A practical guide to building community wireless mesh networks.",
        )
    )

    results = index.search(query="mesh", tags=("community",))

    assert len(results) == 1
    assert results[0].resource_id == "r1"


def test_resource_index_returns_none_for_missing_id():
    index = ResourceIndex()

    assert index.get_resource_by_id("missing") is None


def test_resource_index_validates_bad_url():
    index = ResourceIndex()

    try:
        index.add_resource(
            Resource(
                resource_id="r2",
                title="Broken Link Resource",
                url="ftp://example.com/bad",
                category="Documentation",
                tags=("link",),
            )
        )
        assert False, "Expected ValueError for invalid URL"
    except ValueError as exc:
        assert "resource url must begin with http:// or https://" in str(exc)


def test_resource_index_localized_search_uses_translations():
    index = ResourceIndex()
    spanish = Resource(
        resource_id="r3",
        title="Security Checklist",
        url="https://example.com/checklist",
        category="Tools",
        tags=("security",),
        locale="es",
        description="Guía para revisar los controles de seguridad.",
        translations={
            "en": {
                "title": "Security Checklist",
                "description": "Guide for reviewing security controls.",
            }
        },
    )
    index.add_resource(spanish)

    results = index.search(query="seguridad", locale="es")

    assert len(results) == 1
    assert results[0].resource_id == "r3"


def test_resource_index_locale_falls_back_to_translated_text():
    index = ResourceIndex()
    index.add_resource(
        Resource(
            resource_id="r4",
            title="Lista de verificación de seguridad",
            url="https://example.com/seguridad",
            category="Tools",
            tags=("security",),
            locale="es",
            description="Guía para revisar los controles de seguridad.",
            translations={
                "en": {
                    "title": "Security Checklist",
                    "description": "Guide for reviewing security controls.",
                }
            },
        )
    )

    results = index.search(query="security", locale="en")

    assert len(results) == 1
    assert results[0].resource_id == "r4"


def test_resource_index_locale_search_falls_back_to_default_text():
    index = ResourceIndex()
    index.add_resource(
        Resource(
            resource_id="r11",
            title="Safety Guide",
            url="https://example.com/safety-guide",
            category="Tools",
            tags=("safety",),
            locale="en",
            description="A guide to safety checks.",
        )
    )

    results = index.search(query="safety", locale="es")

    assert len(results) == 1
    assert results[0].resource_id == "r11"


def test_resource_index_search_filters_category_and_tags_case_insensitive():
    index = ResourceIndex()
    index.add_resource(
        Resource(
            resource_id="r5",
            title="Local Network Planning",
            url="https://example.com/local-planning",
            category="Documentation",
            tags=("planning", "mesh"),
            description="A guide for community planning and deployments.",
        )
    )

    results = index.search(query="planning", category="documentation", tags=("MESH",))

    assert len(results) == 1
    assert results[0].resource_id == "r5"


def test_resource_index_search_by_resource_id():
    index = ResourceIndex()
    index.add_resource(
        Resource(
            resource_id="find-me",
            title="Resource ID Search",
            url="https://example.com/id-search",
            category="Tools",
            tags=("search",),
            description="Resource with searchable id.",
        )
    )

    results = index.search(query="find-me")

    assert len(results) == 1
    assert results[0].resource_id == "find-me"


def test_resource_index_search_with_category_and_tag_indexes():
    index = ResourceIndex()
    index.add_resource(
        Resource(
            resource_id="r6",
            title="Security Guide",
            url="https://example.com/security-guide",
            category="Guides",
            tags=("security", "checklist"),
            description="A searchable security guide.",
        )
    )
    index.add_resource(
        Resource(
            resource_id="r7",
            title="Network Tips",
            url="https://example.com/network-tips",
            category="Guides",
            tags=("network",),
            description="A guide to wireless network planning.",
        )
    )

    results = index.search(query="security", category="guides", tags=("checklist",))

    assert len(results) == 1
    assert results[0].resource_id == "r6"


def test_resource_index_validates_bad_translation_locale():
    index = ResourceIndex()

    try:
        index.add_resource(
            Resource(
                resource_id="r8",
                title="Invalid Translation",
                url="https://example.com/invalid",
                category="Tools",
                locale="en",
                translations={
                    "invalid": {
                        "title": "Invalid Locale",
                    }
                },
            )
        )
        assert False, "Expected ValueError for invalid translation locale"
    except ValueError as exc:
        assert "unsupported translation locale: invalid" in str(exc)


def test_resource_index_search_multi_word_and_logic():
    index = ResourceIndex()
    index.add_resource(
        Resource(
            resource_id="r9",
            title="Security Checklist Guide",
            url="https://example.com/security-checklist",
            category="Tools",
            tags=("security", "checklist"),
            description="A comprehensive guide for security reviews.",
        )
    )
    index.add_resource(
        Resource(
            resource_id="r10",
            title="Network Security",
            url="https://example.com/network-security",
            category="Tools",
            tags=("network", "security"),
            description="Guide for network security.",
        )
    )

    # Should find r9 because it has both "security" and "checklist"
    results = index.search(query="security checklist")

    assert len(results) == 1
    assert results[0].resource_id == "r9"

    # Should find both because both have "security"
    results = index.search(query="security")

    assert len(results) == 2


def test_resource_index_search_with_limit_and_sort():
    index = ResourceIndex()
    index.add_resource(
        Resource(
            resource_id="z-resource",
            title="Zebra Guide",
            url="https://example.com/zebra",
            category="Tools",
            description="Guide starting with Z.",
        )
    )
    index.add_resource(
        Resource(
            resource_id="a-resource",
            title="Apple Guide",
            url="https://example.com/apple",
            category="Tools",
            description="Guide starting with A.",
        )
    )

    # Sort by title ascending
    results = index.search(sort_by="title")

    assert len(results) == 2
    assert results[0].resource_id == "a-resource"
    assert results[1].resource_id == "z-resource"

    # Limit to 1
    results = index.search(limit=1, sort_by="title")

    assert len(results) == 1
    assert results[0].resource_id == "a-resource"


def test_resource_index_export_to_json():
    index = ResourceIndex()
    index.add_resource(
        Resource(
            resource_id="export-test",
            title="Export Test",
            url="https://example.com/export",
            category="Test",
            tags=("export",),
            description="Test resource for export.",
            locale="en",
            translations={
                "es": {
                    "title": "Prueba de Exportación",
                    "description": "Recurso de prueba para exportación.",
                }
            },
        )
    )

    json_str = index.to_json()
    data = json.loads(json_str)

    assert len(data) == 1
    assert data[0]["resource_id"] == "export-test"
    assert data[0]["title"] == "Export Test"
    assert data[0]["translations"]["es"]["title"] == "Prueba de Exportación"
