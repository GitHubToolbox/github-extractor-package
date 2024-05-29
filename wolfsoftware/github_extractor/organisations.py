"""
This module provides functions to list organizations and repositories from GitHub, with optional filtering and pagination handling.

Functions:
- list_organisations: Lists organizations from GitHub using the provided configuration dictionary, allowing for optional filters.
- list_organizations: Alias for list_organisations to accommodate American English spelling.
- list_repositories_by_org: Lists repositories for a specified organization from GitHub using the provided configuration.
- list_all_org_repositories: Lists repositories for a user's organizations from GitHub using the provided configuration.

Dependencies:
- exceptions: Contains custom exceptions for handling errors.
- github: Contains functions for GitHub authentication and API interactions.
- repositories: Contains the filter_repositories function for filtering repositories.
- stubs: Contains the internal functions for listing organizations and repositories from GitHub.
- utils: Contains utility functions such as creating slugs from data.

Example usage:
    from .organisations import list_organisations, list_organizations

    config = {
        "token": "your_github_token",
        "ignore_orgs": ["Test*"]
    }
    organisations = list_organisations(config)

    organisations_us = list_organizations(config)
"""

from typing import Any, Callable, Dict, List, Optional, Union

from .addons import get_repo_addons
from .constants import DEFAULT_TIMEOUT
from .exceptions import MissingTokenError, MissingOrgNameError
from .filters import filter_repositories, filter_organisations
from .members import get_members_for_orgs
from .stubs import internal_list_organisations, internal_list_repositories_by_org, internal_list_user_repositories
from .user import get_authenticated_user_name
from .utils import create_slugs


def list_organisations(config: Optional[Dict] = None) -> Union[List[Dict], List[str]]:
    """
    List organizations from GitHub using the provided configuration.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            - ignore_orgs (Optional[List[str]]): A list of organization names or regex patterns to ignore (case insensitive). Default is None.
            - include_orgs (Optional[List[str]]): A list of organization names or regex patterns to include (case insensitive). Default is None.
            - slugs (bool): If True, return only the slugs of the organizations. Default is False.
            Default is an empty dictionary.

    Returns:
        Union[List[Dict], List[str]]: A list of dictionaries representing the organizations if successful, otherwise an empty list.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    slugs: bool = config.get('slugs', False)
    get_members: bool = config.get('get_members', False)

    if not token:
        raise MissingTokenError("A token must be provided to list your organisational membership")

    organisations: List[Dict] = internal_list_organisations({'token': token, 'timeout': timeout})

    filtered_organisations: List[Dict[str, Any]] = filter_organisations(organisations, config)

    if slugs:
        return create_slugs(filtered_organisations, 'login')

    if get_members:
        filtered_organisations = get_members_for_orgs(filtered_organisations, config)

    filtered_organisations.sort(key=lambda org: org.get('login', '').lower())

    return filtered_organisations


# Alias for list_organisations to accommodate American English spelling
list_organizations: Callable[[Optional[Dict]], Union[List[Dict], List[str]]] = list_organisations


def list_repositories_by_org(config: Optional[Dict] = None) -> Union[List[Dict], List[str]]:
    """
    List repositories for a specified organization from GitHub using the provided configuration.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (Optional[str]): The GitHub API token.
            - org_name (str): The name of the organization.
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

    Raises:
        MissingOrgNameError: If the org_name is not provided in the configuration.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    org_name: Optional[str] = config.get('org_name')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    slugs: bool = config.get('slugs', False)

    if not org_name:
        raise MissingOrgNameError("Organization name is required.")

    repos: List[Dict[str, Any]] = internal_list_repositories_by_org({'token': token, 'org_name': org_name, 'timeout': timeout})

    filtered_repos: List[Dict[str, Any]] = filter_repositories(repos, config)

    if slugs:
        return create_slugs(filtered_repos, 'full_name')

    filtered_repos = get_repo_addons(filtered_repos, config)

    filtered_repos.sort(key=lambda repo: repo.get('full_name', '').lower())

    return filtered_repos


def list_all_org_repositories(config: Optional[Dict] = None) -> Union[List[Dict], List[str]]:
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

    user_login: str = get_authenticated_user_name(config)
    repos = [repo for repo in repos if repo['owner']['login'] != user_login]

    filtered_repos: List[Dict[str, Any]] = filter_repositories(repos, config)

    if slugs:
        return create_slugs(filtered_repos, 'full_name')

    filtered_repos = get_repo_addons(filtered_repos, config)

    filtered_repos.sort(key=lambda repo: repo.get('full_name', '').lower())

    return filtered_repos
