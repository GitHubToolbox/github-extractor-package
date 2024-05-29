"""
This module provides a functions to filter repositories and organisations based on specified patterns for both name and/or full_name.

It supports excluding private repositories and handles multiple filtering criteria.

Functions:
- filter_organisations: Filters organisations based on ignore and include patterns for name.
- filter_repositories: Filters repositories based on ignore and include patterns for both name and full_name.

Dependencies:
- re: Used for regular expression operations.

Example usage:
    from .repositories import filter_repositories

    config = {
        "ignore_repos": ["test-repo"],
        "include_repos": ["main-repo"],
        "ignore_names": ["test"],
        "include_names": ["main"],
        "skip_private": True
    }

    filtered_repositories = filter_repositories(repositories, config)
"""

from typing import Any, Dict, List, Optional

import re


def filter_organisations(organisations: List[Dict[str, Any]], config: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """
    Filter organisations based on ignore and include patterns for name.

    Arguments:
        organisations (List[Dict[str, Any]]): The list of organisations to filter.
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - ignore_orgs (List[str]): A list of organisation logins or regex patterns to ignore.
            - include_org (List[str]): A list of organisation logins or regex patterns to include.

    Returns:
        List[Dict[str, Any]]: A filtered list of organisations.
    """
    if config is None:
        config = {}

    ignore_orgs: List[str] = config.get('ignore_orgs', [])
    include_orgs: List[str] = config.get('include_orgs', [])

    # Compile regex patterns for ignore_orgs and include_orgs
    ignore_patterns: List[re.Pattern] = [re.compile(pattern, re.IGNORECASE) for pattern in ignore_orgs]
    include_patterns: List[re.Pattern] = [re.compile(pattern, re.IGNORECASE) for pattern in include_orgs]

    # Filter out organizations to be ignored and only include specified organizations
    filtered_organisations: List[Dict] = [
        org for org in organisations
        if (not any(pattern.match(org.get('login', '')) for pattern in ignore_patterns)) and
           (not include_patterns or any(pattern.match(org.get('login', '')) for pattern in include_patterns))
    ]

    return filtered_organisations


def filter_repositories(repos: List[Dict[str, Any]], config: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """
    Filter repositories based on ignore and include patterns for both name and full_name.

    Arguments:
        repos (List[Dict[str, Any]]): The list of repositories to filter.
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - ignore_repos (List[str]): A list of repository full_names or regex patterns to ignore.
            - include_repos (List[str]): A list of repository full_names or regex patterns to include.
            - ignore_names (List[str]): A list of repository names or regex patterns to ignore.
            - include_names (List[str]): A list of repository names or regex patterns to include.
            - skip_private (bool): If True, skip private repositories. Default is False.

    Returns:
        List[Dict[str, Any]]: A filtered list of repositories.
    """
    if config is None:
        config = {}

    ignore_repos: List[str] = config.get('ignore_repos', [])
    include_repos: List[str] = config.get('include_repos', [])
    ignore_names: List[str] = config.get('ignore_names', [])
    include_names: List[str] = config.get('include_names', [])
    skip_private: bool = config.get('skip_private', False)

    if skip_private:
        repos = [repo for repo in repos if not repo['private']]

    # Compile regex patterns for ignore and include options
    ignore_repo_patterns: List[re.Pattern] = [re.compile(pattern, re.IGNORECASE) for pattern in ignore_repos]
    include_repo_patterns: List[re.Pattern] = [re.compile(pattern, re.IGNORECASE) for pattern in include_repos]
    ignore_name_patterns: List[re.Pattern] = [re.compile(pattern, re.IGNORECASE) for pattern in ignore_names]
    include_name_patterns: List[re.Pattern] = [re.compile(pattern, re.IGNORECASE) for pattern in include_names]

    # Filter out repositories to be ignored and only include specified repositories
    filtered_repos: List[Dict[str, Any]] = [
        repo for repo in repos
        if (not any(pattern.match(repo.get('full_name', '')) for pattern in ignore_repo_patterns)) and
           (not any(pattern.match(repo.get('name', '')) for pattern in ignore_name_patterns)) and
           (not include_repo_patterns or any(pattern.match(repo.get('full_name', '')) for pattern in include_repo_patterns)) and
           (not include_name_patterns or any(pattern.match(repo.get('name', '')) for pattern in include_name_patterns))
    ]

    return filtered_repos
