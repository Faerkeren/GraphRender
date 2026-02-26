from importlib import resources

__all__ = ["default_theme_css"]


def default_theme_css() -> str:
    """Return the bundled default theme.css content."""
    try:
        return resources.files("graphrender.resources").joinpath("default_theme.css").read_text()
    except Exception:
        return ""
