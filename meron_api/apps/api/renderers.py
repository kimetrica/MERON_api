"""Renderer that disable the forms in the API browser."""
from rest_framework.renderers import BrowsableAPIRenderer


class ReadOnlyBrowsableAPIRenderer(BrowsableAPIRenderer):
    """Renders the browsable api, but excludes the forms."""

    def get_context(self, *args, **kwargs):
        """Override get_context to be able to set display_edit_forms to False."""
        context = super().get_context(*args, **kwargs)
        context["display_edit_forms"] = False
        return context
