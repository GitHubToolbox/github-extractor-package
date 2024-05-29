"""
This module provides functions to fetch additional information about the authenticated user from GitHub.

Functions:
- fetch_user_profile: Fetches profile information for the authenticated user.
- fetch_user_emails: Fetches email addresses for the authenticated user.
- fetch_user_followers: Fetches followers for the authenticated user.
- fetch_user_following: Fetches the list of users the authenticated user is following.
- fetch_user_gpg_keys: Fetches GPG keys for the authenticated user.
- fetch_user_ssh_keys: Fetches SSH keys for the authenticated user.
- fetch_user_repos: Fetches repositories owned by the authenticated user.
- fetch_user_starred_repos: Fetches repositories starred by the authenticated user.
- fetch_user_subscriptions: Fetches repositories watched by the authenticated user.

Dependencies:
- github: Contains the `github_api` function for interacting with the GitHub API.

Example usage:
    from .user_info import fetch_user_profile, fetch_user_emails

    config = {
        "token": "your_github_token",
        "timeout": 10
    }

    user_profile = fetch_user_profile(config)
    user_emails = fetch_user_emails(config)
"""
from typing import Any, Dict, Optional

import requests

from .exceptions import AuthenticationError, RateLimitExceededError, NotFoundError, RequestError, RequestTimeoutError
from .constants import DEFAULT_TIMEOUT
from .github import github_api


def get_authenticated_user_name(config: Optional[Dict] = None) -> str:
    """
    Retrieve the username of the authenticated user from GitHub.

    This function makes a request to the GitHub API to get the details of the authenticated user
    using the provided token. It returns the login (username) of the authenticated user.

    Arguments:
        token (str): The GitHub API token for authentication.
        timeout (int): The timeout for the request in seconds.

    Returns:
        str: The username (login) of the authenticated user.

    Raises:
        requests.RequestException: If the request fails or the server returns an error status code.
    """
    auth_user: Dict = get_authenticated_user(config)

    return auth_user.get('login', '')


def get_authenticated_user(config: Optional[Dict] = None) -> Dict:  # noqa: C901  pylint: disable=too-many-locals, too-many-branches
    """
    Retrieve the username of the authenticated user from GitHub.

    This function makes a request to the GitHub API to get the details of the authenticated user
    using the provided token. It returns the login (username) of the authenticated user.

    Arguments:
        token (str): The GitHub API token for authentication.
        timeout (int): The timeout for the request in seconds.

    Returns:
        str: The username (login) of the authenticated user.

    Raises:
        requests.RequestException: If the request fails or the server returns an error status code.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)

    user_url = "https://api.github.com/user"

    headers: Dict[str, str] = {'Authorization': f'token {token}'} if token else {}

    # Do not use github_api as this end point returns just a dict not a list[dict]]
    try:
        response: requests.Response = requests.get(user_url, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            raise AuthenticationError("Authentication failed: Bad credentials") from e
        if response.status_code == 403:
            raise RateLimitExceededError(f"Rate limit exceeded for {user_url}") from e
        if response.status_code == 404:
            raise NotFoundError(f"Resource not found for URL: {user_url}") from e
        raise RequestError(f"HTTP error occurred: {e}") from e
    except requests.exceptions.Timeout as e:
        raise RequestTimeoutError(f"Request timed out after {timeout} seconds") from e
    except requests.exceptions.RequestException as e:
        raise RequestError(f"An error occurred: {e}") from e

    user: Any = response.json()

    get_emails: bool = config.get('get_emails', False)
    get_followers: bool = config.get('get_followers', False)
    get_following: bool = config.get('get_following', False)
    get_gpg_keys: bool = config.get('get_gpg_keys', False)
    get_ssh_keys: bool = config.get('get_ssh_keys', False)
    get_repos: bool = config.get('get_repos', False)
    get_starred_repos: bool = config.get('get_starred_repos', False)
    get_subscriptions: bool = config.get('get_subscriptions', False)

    if get_emails:
        user = fetch_user_emails(user, config)

    if get_followers:
        user = fetch_user_followers(user, config)

    if get_following:
        user = fetch_user_following(user, config)

    if get_gpg_keys:
        user = fetch_user_gpg_keys(user, config)

    if get_ssh_keys:
        user = fetch_user_ssh_keys(user, config)

    if get_repos:
        user = fetch_user_repos(user, config)

    if get_starred_repos:
        user = fetch_user_starred_repos(user, config)

    if get_subscriptions:
        user = fetch_user_subscriptions(user, config)

    return user


def fetch_user_emails(user: Any, config: Optional[Dict] = None) -> Any:
    """
    Fetch email addresses for the authenticated user.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.

    Returns:
        Dict[str, Any]: A dictionary containing the user's email addresses.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    emails_url: str = "https://api.github.com/user/emails"

    try:
        user['emails'] = github_api(emails_url, token, timeout)
    except Exception as e:
        user['emails'] = []
        user['emails_errors'] = {
            'error': str(e),
            'error_type': type(e).__name__
        }

    return user


def fetch_user_followers(user: Any, config: Optional[Dict] = None) -> Any:
    """
    Fetch followers for the authenticated user.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.

    Returns:
        Dict[str, Any]: A dictionary containing the user's followers.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    followers_url: str = "https://api.github.com/user/followers"

    try:
        user['followers_list'] = github_api(followers_url, token, timeout)
    except Exception as e:
        user['followers_list'] = []
        user['followers_list_errors'] = {
            'error': str(e),
            'error_type': type(e).__name__
        }

    return user


def fetch_user_following(user: Any, config: Optional[Dict] = None) -> Any:
    """
    Fetch the list of users the authenticated user is following.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.

    Returns:
        Dict[str, Any]: A dictionary containing the users the authenticated user is following.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    following_url: str = "https://api.github.com/user/following"

    try:
        user['following_list'] = github_api(following_url, token, timeout)
    except Exception as e:
        user['following_list'] = []
        user['following_list_errors'] = {
            'error': str(e),
            'error_type': type(e).__name__
        }

    return user


def fetch_user_gpg_keys(user: Any, config: Optional[Dict] = None) -> Any:
    """
    Fetch GPG keys for the authenticated user.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.

    Returns:
        Dict[str, Any]: A dictionary containing the user's GPG keys.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    gpg_keys_url: str = "https://api.github.com/user/gpg_keys"

    try:
        user['gpg_keys'] = github_api(gpg_keys_url, token, timeout)
    except Exception as e:
        user['gpg_keys'] = []
        user['gpg_keys_errors'] = {
            'error': str(e),
            'error_type': type(e).__name__
        }

    return user


def fetch_user_ssh_keys(user: Any, config: Optional[Dict] = None) -> Any:
    """
    Fetch SSH keys for the authenticated user.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.

    Returns:
        Dict[str, Any]: A dictionary containing the user's SSH keys.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    ssh_keys_url: str = "https://api.github.com/user/keys"

    try:
        user['ssh_keys'] = github_api(ssh_keys_url, token, timeout)
    except Exception as e:
        user['ssh_keys'] = []
        user['ssh_keys_errors'] = {
            'error': str(e),
            'error_type': type(e).__name__
        }

    return user


def fetch_user_repos(user: Any, config: Optional[Dict] = None) -> Any:
    """
    Fetch repositories owned by the authenticated user.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.

    Returns:
        Dict[str, Any]: A dictionary containing the user's repositories.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    repos_url: str = "https://api.github.com/user/repos"

    try:
        user['repos'] = github_api(repos_url, token, timeout)
    except Exception as e:
        user['repos'] = []
        user['repos'] = {
            'error': str(e),
            'error_type': type(e).__name__
        }

    return user


def fetch_user_starred_repos(user: Any, config: Optional[Dict] = None) -> Any:
    """
    Fetch repositories starred by the authenticated user.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.

    Returns:
        Dict[str, Any]: A dictionary containing the repositories starred by the user.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    starred_repos_url: str = "https://api.github.com/user/starred"

    try:
        user['starred_repos'] = github_api(starred_repos_url, token, timeout)
    except Exception as e:
        user['starred_repos'] = []
        user['starred_repos'] = {
            'error': str(e),
            'error_type': type(e).__name__
        }

    return user


def fetch_user_subscriptions(user: Any, config: Optional[Dict] = None) -> Any:
    """
    Fetch repositories watched by the authenticated user.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following keys:
            - token (str): The GitHub API token.
            - timeout (int): Timeout for the request in seconds. Default is 10 seconds.

    Returns:
        Dict[str, Any]: A dictionary containing the repositories watched by the user.
    """
    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)
    subscriptions_url: str = "https://api.github.com/user/subscriptions"

    try:
        user['subscriptions'] = github_api(subscriptions_url, token, timeout)
    except Exception as e:
        user['subscriptions'] = []
        user['subscriptions'] = {
            'error': str(e),
            'error_type': type(e).__name__
        }

    return user
