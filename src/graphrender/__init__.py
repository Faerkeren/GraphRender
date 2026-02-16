"""
GraphRender package initialization.
Exports the GraphRender converter and resource helpers.
"""

from .graphrender import GraphRender

from .resources import default_theme_css

__all__ = [
    "GraphRender",
    "default_theme_css",
]
