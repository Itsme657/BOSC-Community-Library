from dataclasses import dataclass, field
from typing import Final, Iterable, Optional

SUPPORTED_LOCALES: Final = ["en", "es", "fr", "pt"]


@dataclass(frozen=True)
class Resource:
    resource_id: str
    title: str
    url: str
    category: str
    tags: tuple[str, ...] = ()
    locale: str = "en"
    description: str = ""
    translations: dict[str, dict[str, str]] = field(default_factory=dict)

    def localized_title(self, locale: str = "en") -> str:
        return self.translations.get(locale, {}).get("title", self.title)

    def localized_description(self, locale: str = "en") -> str:
        return self.translations.get(locale, {}).get("description", self.description)

    def validate(self) -> None:
        if not self.resource_id.strip():
            raise ValueError("resource id is required")

        if not self.title.strip():
            raise ValueError("resource title is required")

        if not self.url.startswith(("http://", "https://")):
            raise ValueError("resource url must begin with http:// or https://")

        if not self.category.strip():
            raise ValueError("resource category is required")

        if self.locale not in SUPPORTED_LOCALES:
            raise ValueError(f"unsupported locale: {self.locale}")


class ResourceIndex:
    """A lightweight searchable collection of community resources."""

    def __init__(self) -> None:
        self._resources: dict[str, Resource] = {}

    def add_resource(self, resource: Resource) -> None:
        resource.validate()

        if resource.resource_id in self._resources:
            raise ValueError(f"resource with id '{resource.resource_id}' already exists")

        self._resources[resource.resource_id] = resource

    def get_resource_by_id(self, resource_id: str) -> Optional[Resource]:
        return self._resources.get(resource_id)

    def all_resources(self) -> list[Resource]:
        return list(self._resources.values())

    def search(
        self,
        query: str = "",
        category: str = "",
        tags: Iterable[str] = (),
        locale: str = "en",
    ) -> list[Resource]:
        query_text = query.strip().lower()
        normalized_tags = {tag.strip().lower() for tag in tags if tag.strip()}
        category_text = category.strip().lower()

        results: list[Resource] = []

        for resource in self._resources.values():
            if category_text and category_text != resource.category.lower():
                continue

            if normalized_tags and not normalized_tags.issubset({t.lower() for t in resource.tags}):
                continue

            title_text = resource.localized_title(locale) if locale else resource.title
            description_text = resource.localized_description(locale) if locale else resource.description
            searchable_text = (
                title_text
                + " "
                + description_text
                + " "
                + resource.category
                + " "
                + " ".join(resource.tags)
            ).lower()

            if query_text and query_text not in searchable_text:
                continue

            if locale and locale != resource.locale and locale not in resource.translations:
                continue

            results.append(resource)

        return results
