"""
This module provides a function to fetch various addons for a list of GitHub repositories concurrently.

The addons include contributors, languages, releases, tags, topics, and workflows.

Functions:
- get_repo_addons: Fetches specified addons for a list of repositories using the provided configuration.

Dependencies:
- contributors: Contains the `get_contributors_for_repos` function for fetching contributors.
- languages: Contains the `get_languages_for_repos` function for fetching languages.
- releases: Contains the `get_releases_for_repos` function for fetching releases.
- topics: Contains the `get_topics_for_repos` function for fetching topics.
- tags: Contains the `get_tags_for_repos` function for fetching tags.
- workflows: Contains the `get_workflows_for_repos` function for fetching workflows.

Example usage:
    from .addons import get_repo_addons

    config = {
        "token": "your_github_token",
        "timeout": 10,
        "get_contributors": True,
        "get_languages": True,
        "get_releases": True,
        "get_tags": True,
        "get_topics": True,
        "get_workflows": True
    }

    repos = [{"full_name": "owner/repo1"}, {"full_name": "owner/repo2"}]
    repos_with_addons = get_repo_addons(repos, config)
"""

from typing import Any, Dict, List, Optional

from .branches import get_branches_for_repos
from .contributors import get_contributors_for_repos
from .languages import get_languages_for_repos
from .releases import get_releases_for_repos
from .topics import get_topics_for_repos
from .tags import get_tags_for_repos
from .workflows import get_workflows_for_repos


def get_repo_addons(repos: List[Dict[str, Any]], config: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """
    Fetch specified addons for a list of GitHub repositories using the provided configuration.

    Arguments:
        repos (List[Dict[str, Any]]): The list of repositories for which to fetch addons.
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            - get_contributors (bool): Flag to fetch contributors. Default is False.
            - get_languages (bool): Flag to fetch languages. Default is False.
            - get_releases (bool): Flag to fetch releases. Default is False.
            - get_tags (bool): Flag to fetch tags. Default is False.
            - get_topics (bool): Flag to fetch topics. Default is False.
            - get_workflows (bool): Flag to fetch workflows. Default is False.
            Default is an empty dictionary.

    Returns:
        List[Dict[str, Any]]: The list of repositories with the specified addons fetched and added.

    Example usage:
        config = {
            "token": "your_github_token",
            "timeout": 10,
            "get_contributors": True,
            "get_languages": True,
            "get_releases": True,
            "get_tags": True,
            "get_topics": True,
            "get_workflows": True
        }

        repos = [{"full_name": "owner/repo1"}, {"full_name": "owner/repo2"}]
        repos_with_addons = get_repo_addons(repos, config)
    """
    if config is None:
        config = {}

    get_branches: bool = config.get('get_branches', False)
    get_contributors: bool = config.get('get_contributors', False)
    get_languages: bool = config.get('get_languages', False)
    get_releases: bool = config.get('get_releases', False)
    get_tags: bool = config.get('get_tags', False)
    get_topics: bool = config.get('get_topics', False)
    get_workflows: bool = config.get('get_workflows', False)

    if get_branches:
        repos = get_branches_for_repos(repos, config)

    if get_contributors:
        repos = get_contributors_for_repos(repos, config)

    if get_languages:
        repos = get_languages_for_repos(repos, config)

    if get_releases:
        repos = get_releases_for_repos(repos, config)

    if get_topics:
        repos = get_topics_for_repos(repos, config)

    if get_tags:
        repos = get_tags_for_repos(repos, config)

    if get_workflows:
        repos = get_workflows_for_repos(repos, config)

    return repos
