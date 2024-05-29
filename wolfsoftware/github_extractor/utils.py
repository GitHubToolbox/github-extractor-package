"""
This module provides utility functions for the GitHub extractor package.

Functions:
- create_slugs: Creates a list of slugs from a list of dictionaries based on a specified key.

Dependencies:
- typing: Used for type annotations.

Example usage:
    from .utils import create_slugs

    data = [{"name": "repo1"}, {"name": "repo2"}, {"name": "repo3"}]
    slugs = create_slugs(data, "name")
"""

from typing import Dict, List


def create_slugs(data: List[Dict], key: str) -> List[str]:
    """
    Create a list of slugs from the list of dictionaries based on the provided key.

    Arguments:
        data (List[Dict]): A list of dictionaries representing the data (e.g., repositories or organizations).
        key (str): The key to extract the slug from each dictionary.

    Returns:
        List[str]: A list of slugs (values of the specified key).
    """
    return [item[key] for item in data if key in item]
