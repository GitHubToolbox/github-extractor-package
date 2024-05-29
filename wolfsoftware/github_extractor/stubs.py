"""
This module provides internal functions to list organizations and repositories from GitHub using a configuration dictionary.

It supports optional filtering and handles pagination.

Functions:
- internal_list_organisations: Lists organizations from GitHub using the provided configuration.
- internal_list_user_repositories: Lists repositories for a user from GitHub using the provided configuration.
- internal_list_repositories_by_org: Lists repositories for a specified organization from GitHub using the provided configuration.

Dependencies:
- github_api: A function for interacting with the GitHub API and handling pagination.

Example usage:
    from .stubs import internal_list_organisations, internal_list_user_repositories, internal_list_repositories_by_org

    config = {
        "token": "your_github_token",
        "timeout": 10
    }

    # List organizations
    organisations = internal_list_organisations(config)

    # List user repositories
    repositories = internal_list_user_repositories(config)

    # List repositories by organization
    org_config = {
        "token": "your_github_token",
        "org_name": "your_organization",
        "timeout": 10
    }
    repositories_by_org = internal_list_repositories_by_org(org_config)

Author: [Your Name]
Version: 1.0.0
"""

from typing import Dict, List, Optional

from .constants import DEFAULT_TIMEOUT
from .exceptions import MissingTokenError, MissingOrgNameError
from .github import github_api


def internal_list_organisations(config: Optional[Dict] = None) -> List[Dict]:
    """
    List organizations from GitHub using the provided configuration.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            Default is an empty dictionary.

    Returns:
        List[Dict]: A list of dictionaries representing the organizations if successful, otherwise an empty list.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)

    if not token:
        raise MissingTokenError("A token must be provided to list your organisational membership")

    # GitHub API URL to list organizations for the authenticated user
    list_orgs_url = "https://api.github.com/user/orgs"

    try:
        orgs: List[Dict] = github_api(list_orgs_url, token, timeout)
    except Exception:
        orgs = []

    return orgs


def internal_list_user_repositories(config: Optional[Dict] = None) -> List[Dict]:
    """
    List repositories for a user from GitHub using the provided configuration.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            Default is an empty dictionary.

    Returns:
        List[Dict]: A list of dictionaries representing the repositories if successful, otherwise an empty list.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    username: Optional[str] = config.get('username')

    # Determine the GitHub API URL to list repositories
    if username:
        list_user_repos_url: str = f"https://api.github.com/users/{username}/repos"
    else:
        list_user_repos_url = "https://api.github.com/user/repos"

    try:
        repos: List[Dict] = github_api(list_user_repos_url, token, timeout)
    except Exception:
        repos = []

    return repos


def internal_list_repositories_by_org(config: Optional[Dict] = None) -> List[Dict]:
    """
    List repositories for a specified organization from GitHub using the provided configuration.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - org_name (str): The name of the organization.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            Default is an empty dictionary.

    Returns:
        List[Dict]: A list of dictionaries representing the repositories if successful, otherwise an empty list.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    org_name: Optional[str] = config.get('org_name')

    if not org_name:
        raise MissingOrgNameError("Organization name is required.")

    # GitHub API URL to list repositories in an organization
    list_repos_url: str = f"https://api.github.com/orgs/{org_name}/repos"

    repos: List[Dict] = github_api(list_repos_url, token, timeout)
    return repos
