"""
This module provides functions to fetch workflows for repositories from GitHub concurrently.

Functions:
- fetch_workflows: Fetches workflows for a given repository using the provided configuration.
- get_workflows_for_repos: Fetches workflows for a list of repositories concurrently using the provided configuration.

Dependencies:
- concurrent.futures: Used for concurrent execution of fetching workflows.
- github: Contains the `github_api` function for interacting with the GitHub API.

Example usage:
    from .workflows import get_workflows_for_repos

    config = {
        "token": "your_github_token",
        "timeout": 10
    }

    repos = [{"full_name": "owner/repo1"}, {"full_name": "owner/repo2"}]
    repos_with_workflows = get_workflows_for_repos(repos, config)
"""

from typing import Any, Dict, List, Optional
import concurrent.futures

from .constants import DEFAULT_TIMEOUT, DEFAULT_THREADS
from .github import github_api


def fetch_workflows(repo: Dict[str, Any], config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Fetch workflows for a specific repository.

    Arguments:
        repo (Dict[str, Any]): The repository for which to fetch workflows.
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            Default is an empty dictionary.

    Returns:
        Dict[str, Any]: The repository with an added "workflows" key containing the workflows data and
                        "workflow_errors" key containing any errors encountered.

    Raises:
        RateLimitExceededError: If the GitHub API rate limit is exceeded.
        requests.exceptions.RequestException: For other request exceptions.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)

    workflows_url: str = f"https://api.github.com/repos/{repo['full_name']}/actions/workflows"

    try:
        workflows: List[Dict] = github_api(workflows_url, token, timeout)
        workflows = workflows[0].get('workflows', []) if workflows else []
        workflows_by_status: Dict[str, List] = {
            "active": [],
            "deleted": [],
            "disabled_fork": [],
            "disabled_inactivity": [],
            "disabled_manually": [],
            "unknown": [],
        }
        for workflow in workflows:
            state = workflow.get('state', 'unknown').lower()
            if state in workflows_by_status:
                workflows_by_status[state].append(workflow)
            else:
                workflows_by_status["unknown"].append(workflow)

        # Sort workflows in each state alphabetically by name
        for status in workflows_by_status:
            workflows_by_status[status] = sorted(workflows_by_status[status], key=lambda x: x.get('name', '').lower())

        repo['workflows'] = workflows_by_status

    except Exception as e:
        repo['workflows'] = {
            "active": [],
            "deleted": [],
            "disabled_fork": [],
            "disabled_inactivity": [],
            "disabled_manually": [],
            "unknown": []
        }
        repo['workflow_errors'] = {
            'error': str(e),
            'error_type': type(e).__name__
        }

    return repo


def get_workflows_for_repos(repos: List[Dict[str, Any]], config: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """
    Fetch workflows for a list of repositories concurrently using the provided configuration.

    Arguments:
        repos (List[Dict[str, Any]]): The list of repositories for which to fetch workflows.
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.
            Default is an empty dictionary.

    Returns:
        List[Dict[str, Any]]: The list of repositories with added "workflows" key containing the workflows data for each repository.

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
            threads.append(executor.submit(fetch_workflows, repo, config))

        for task in concurrent.futures.as_completed(threads):
            thread_result: Any = task.result()
            if thread_result:
                results.append(thread_result)

    return results
