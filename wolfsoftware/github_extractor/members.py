"""
This module provides functions to fetch members for organizations from GitHub concurrently.

Functions:
- fetch_members: Fetches members for a given organization using the provided configuration.
- get_members_for_orgs: Fetches members for a list of organizations concurrently using the provided configuration.

Dependencies:
- concurrent.futures: Used for concurrent execution of fetching members.
- github: Contains the `github_api` function for interacting with the GitHub API.

Example usage:
    from .members import get_members_for_orgs

    config = {
        "token": "your_github_token",
        "timeout": 10
    }

    orgs = [{"login": "org1"}, {"login": "org2"}]
    orgs_with_members = get_members_for_orgs(orgs, config)
"""

from typing import Any, Dict, List, Optional
import concurrent.futures
from .constants import DEFAULT_TIMEOUT, DEFAULT_THREADS
from .github import github_api


def fetch_members(org: Dict[str, Any], config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Fetch members for a specific organization.

    Arguments:
        org (Dict[str, Any]): The organization for which to fetch members.
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            Default is an empty dictionary.

    Returns:
        Dict[str, Any]: The organization with an added "members" key containing the members data and
                        "member_errors" key containing any errors encountered.

    Raises:
        RateLimitExceededError: If the GitHub API rate limit is exceeded.
        requests.exceptions.RequestException: For other request exceptions.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)

    members_url: str = f"https://api.github.com/orgs/{org['login']}/members"

    try:
        members: List[Dict] = github_api(members_url, token, timeout)
        # Sort members alphabetically by login
        members = sorted(members, key=lambda x: x.get('login', '').lower())
    except Exception as e:
        members = []
        org['member_errors'] = {
            'error': str(e),
            'error_type': type(e).__name__
        }

    org['members'] = members

    return org


def get_members_for_orgs(orgs: List[Dict[str, Any]], config: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """
    Fetch members for a list of organizations concurrently using the provided configuration.

    Arguments:
        orgs (List[Dict[str, Any]]): The list of organizations for which to fetch members.
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            Default is an empty dictionary.

    Returns:
        List[Dict[str, Any]]: The list of organizations with added "members" key containing the members data for each organization.

    Raises:
        RateLimitExceededError: If the GitHub API rate limit is exceeded.
        requests.exceptions.RequestException: For other request exceptions.
    """
    threads: List = []
    results: List = []

    if config is None:
        config = {}

    user_threads: int = config.get('threads', DEFAULT_THREADS)
    max_workers: int = min(user_threads, len(orgs))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for org in orgs:
            threads.append(executor.submit(fetch_members, org, config))

        for task in concurrent.futures.as_completed(threads):
            thread_result: Any = task.result()
            if thread_result:
                results.append(thread_result)

    return results
