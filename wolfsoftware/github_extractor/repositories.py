"""
This module provides functions to list repositories for a given organization or user from GitHub using a configuration dictionary.

It supports filtering of repositories based on given patterns and handles pagination.

Functions:
- list_all_visible_repositories: Lists all visible repositories for a user from GitHub using the provided configuration and applies optional filters.
- list_user_repositories: Lists repositories for a user from GitHub using the provided configuration and applies optional filters.

Dependencies:
- github: Contains functions for GitHub authentication and API interactions.
- exceptions: Contains custom exceptions for handling errors.
- repositories: Contains the filter_repositories function for filtering repositories.
- stubs: Contains internal stub functions for listing repositories by organization and user.
- utils: Contains utility functions such as creating slugs from data.

Example usage:
    from .repositories import list_all_visible_repositories, list_user_repositories

    config = {
        "token": "your_github_token",
        "ignore_repos": ["Test*"],
        "timeout": 10
    }
    all_repositories = list_all_visible_repositories(config)
    user_repositories = list_user_repositories(config)
"""

from typing import Any, Dict, List, Optional, Union

from .addons import get_repo_addons
from .constants import DEFAULT_TIMEOUT
from .exceptions import MissingTokenError
from .filters import filter_repositories
from .stubs import internal_list_user_repositories
from .user import get_authenticated_user_name
from .utils import create_slugs


def list_all_visible_repositories(config: Optional[Dict] = None) -> Union[List[Dict], List[str]]:
    """
    List repositories for a user from GitHub using the provided configuration.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            - ignore_repos (Optional[List[str]]): A list of repository full_names or regex patterns to ignore (case insensitive). Default is None.
            - include_repos (Optional[List[str]]): A list of repository full_names or regex patterns to include (case insensitive). Default is None.
            - ignore_names (Optional[List[str]]): A list of repository names or regex patterns to ignore (case insensitive). Default is None.
            - include_names (Optional[List[str]]): A list of repository names or regex patterns to include (case insensitive). Default is None.
            - slugs (bool): If True, return only the slugs of the repositories. Default is False.
            - skip_private (bool): If True, remove any repositories labelled as 'private'. Default is False.
            Default is an empty dictionary.

    Returns:
        Union[List[Dict], List[str]]: A list of dictionaries representing the repositories if successful, otherwise an empty list.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    slugs: bool = config.get('slugs', False)

    if not token:
        raise MissingTokenError("A token must be provided to list your repositories")

    repos: List[Dict[str, Any]] = internal_list_user_repositories({'token': token, 'timeout': timeout})

    filtered_repos: List[Dict[str, Any]] = filter_repositories(repos, config)

    if slugs:
        return create_slugs(filtered_repos, 'full_name')

    filtered_repos = get_repo_addons(filtered_repos, config)

    filtered_repos.sort(key=lambda repo: repo.get('full_name', '').lower())

    return filtered_repos


def list_user_repositories(config: Optional[Dict] = None) -> Union[List[Dict], List[str]]:
    """
    List repositories for a user from GitHub using the provided configuration.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            - ignore_repos (Optional[List[str]]): A list of repository full_names or regex patterns to ignore (case insensitive). Default is None.
            - include_repos (Optional[List[str]]): A list of repository full_names or regex patterns to include (case insensitive). Default is None.
            - ignore_names (Optional[List[str]]): A list of repository names or regex patterns to ignore (case insensitive). Default is None.
            - include_names (Optional[List[str]]): A list of repository names or regex patterns to include (case insensitive). Default is None.
            - slugs (bool): If True, return only the slugs of the repositories. Default is False.
            - skip_private (bool): If True, remove any repositories labelled as 'private'. Default is False.
            Default is an empty dictionary.

    Returns:
        Union[List[Dict], List[str]]: A list of dictionaries representing the repositories if successful, otherwise an empty list.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    slugs: bool = config.get('slugs', False)
    username: Optional[str] = config.get('username')

    if username:
        user_login: str = username
    else:
        if not token:
            raise MissingTokenError("A token must be provided to list your repositories")
        user_login = get_authenticated_user_name(config)

    repos: List[Dict[str, Any]] = internal_list_user_repositories(config)

    repos = [repo for repo in repos if repo['owner']['login'] == user_login]

    filtered_repos: List[Dict[str, Any]] = filter_repositories(repos, config)

    if slugs:
        return create_slugs(filtered_repos, 'full_name')

    filtered_repos = get_repo_addons(filtered_repos, config)

    filtered_repos.sort(key=lambda repo: repo.get('full_name', '').lower())

    return filtered_repos
