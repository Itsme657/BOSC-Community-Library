from src import Resource, ResourceIndex


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
