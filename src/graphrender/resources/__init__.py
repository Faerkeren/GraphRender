from importlib import resources

__all__ = ["default_theme_css"]

def _bundled_default_theme_css() -> str:
    """Return the bundled default theme.css content as a fallback."""
    try:
        return resources.files("graphrender.resources").joinpath("default_theme.css").read_text()
    except Exception:
        return ""


def default_theme_css(theme_id: str = "default") -> str:
    """Return CSS for the selected theme id.

    Prefers GraphTheme package artifacts and falls back to GraphRender's bundled
    default stylesheet when theme_id is "default".
    """
    try:
        from graphtheme import get_theme_css
    except Exception as exc:
        if theme_id != "default":
            raise RuntimeError(
                "Theme resolution requires the 'GraphTheme' package for non-default theme ids."
            ) from exc
        return _bundled_default_theme_css()

    try:
        return get_theme_css(theme_id)
    except Exception:
        if theme_id == "default":
            return _bundled_default_theme_css()
        raise
