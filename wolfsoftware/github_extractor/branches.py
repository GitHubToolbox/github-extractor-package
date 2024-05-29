"""
This module provides functions to fetch branches for repositories from GitHub concurrently.

Functions:
- fetch_branches: Fetches branches for a given repository using the provided configuration.
- get_branches_for_repos: Fetches branches for a list of repositories concurrently using the provided configuration.

Dependencies:
- concurrent.futures: Used for concurrent execution of fetching branches.
- github: Contains the `github_api` function for interacting with the GitHub API.

Example usage:
    from .branches import get_branches_for_repos

    config = {
        "token": "your_github_token",
        "timeout": 10
    }

    repos = [{"full_name": "owner/repo1"}, {"full_name": "owner/repo2"}]
    repos_with_branches = get_branches_for_repos(repos, config)
"""

from typing import Any, Dict, List, Optional
import concurrent.futures

from .constants import DEFAULT_TIMEOUT, DEFAULT_THREADS
from .github import github_api


def fetch_branches(repo: Dict[str, Any], config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Fetch branches for a specific repository.

    Arguments:
        repo (Dict[str, Any]): The repository for which to fetch branches.
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            Default is an empty dictionary.

    Returns:
        Dict[str, Any]: The repository with an added "branches" key containing the branches data and
                        "branch_errors" key containing any errors encountered.

    Raises:
        RateLimitExceededError: If the GitHub API rate limit is exceeded.
        requests.exceptions.RequestException: For other request exceptions.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)

    branches_url: str = f"https://api.github.com/repos/{repo['full_name']}/branches"

    try:
        branches: List[Dict] = github_api(branches_url, token, timeout)
        # Sort branches alphabetically by name
        branches = sorted(branches, key=lambda x: x.get('name', '').lower())
    except Exception as e:
        branches = []
        repo['branch_errors'] = {
            'error': str(e),
            'error_type': type(e).__name__
        }

    repo['branches'] = branches

    return repo


def get_branches_for_repos(repos: List[Dict[str, Any]], config: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """
    Fetch branches for a list of repositories concurrently using the provided configuration.

    Arguments:
        repos (List[Dict[str, Any]]): The list of repositories for which to fetch branches.
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            Default is an empty dictionary.

    Returns:
        List[Dict[str, Any]]: The list of repositories with added "branches" key containing the branches data for each repository.

    Raises:
        RateLimitExceededError: If the GitHub API rate limit is exceeded.
        requests.exceptions.RequestException: For other request exceptions.
    """
    threads: List = []
    results: List = []

    if config is None:
        config = {}

    user_threads: int = config.get('threads', DEFAULT_THREADS)
    max_workers: int = min(user_threads, len(repos))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for repo in repos:
            threads.append(executor.submit(fetch_branches, repo, config))

        for task in concurrent.futures.as_completed(threads):
            thread_result: Any = task.result()
            if thread_result:
                results.append(thread_result)

    return results
