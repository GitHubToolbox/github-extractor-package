"""
This module provides functionality to fetch information about a GitHub token.

It includes its scopes and reset information, using the GitHub API. It handles various HTTP exceptions that may
occur during the API request.

Classes:
    AuthenticationError: Raised when authentication fails.
    RateLimitExceededError: Raised when the rate limit for GitHub API is exceeded.
    NotFoundError: Raised when a requested resource is not found.
    RequestTimeoutError: Raised when the request times out.
    RequestError: Raised for general request-related errors.
    MissingTokenError: Raised when no token is provided.

Functions:
    get_token_information(config: Optional[Dict] = None) -> Dict: Fetches information about a GitHub token.
"""

from typing import Any, Dict, Optional

from datetime import datetime, timedelta

import requests

from .exceptions import AuthenticationError, RateLimitExceededError, NotFoundError, RequestTimeoutError, RequestError, MissingTokenError
from .constants import DEFAULT_TIMEOUT
from .github import generate_github_headers


def get_token_information(config: Optional[Dict] = None) -> Dict:  # noqa: C901  pylint: disable=too-many-locals
    """
    Fetch information about a GitHub token, including its scopes and associated user information.

    Arguments:
        config (Optional[Dict]): Configuration dictionary containing the following optional keys:
            - 'token' (str): The GitHub token to be used for authentication.
            - 'timeout' (int): The timeout for the API request in seconds. Defaults to DEFAULT_TIMEOUT.

    Returns:
        Dict: A dictionary containing the token information and scopes, or an error message.

    Raises:
        AuthenticationError: If authentication fails due to bad credentials.
        RateLimitExceededError: If the GitHub API rate limit is exceeded.
        NotFoundError: If the requested resource is not found.
        RequestTimeoutError: If the request times out.
        RequestError: If a general HTTP error or request exception occurs.
        MissingTokenError: If no token is provided.
    """
    json_data: Dict[str, Any] = {}

    if config is None:
        config = {}

    token: Optional[str] = config.get('token')
    timeout: int = config.get('timeout', DEFAULT_TIMEOUT)

    if not token:
        raise MissingTokenError("A token must be provided to get information about a token")

    url = "https://api.github.com/user"
    headers: Dict[str, str] = generate_github_headers(token)

    try:
        response: requests.Response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        if response.status_code == 200:
            json_data['scopes'] = response.headers.get("X-OAuth-Scopes")
            json_data['rate_limit_limit'] = response.headers.get("X-RateLimit-Limit")
            json_data['rate_limit_remaining'] = response.headers.get("X-RateLimit-Remaining")
            json_data['rate_limit_used'] = response.headers.get("X-RateLimit-Used")

            rate_limit_reset: Optional[str] = response.headers.get("X-RateLimit-Reset")

            if rate_limit_reset:
                reset_time: datetime = datetime.fromtimestamp(int(rate_limit_reset))
                current_time: datetime = datetime.now()
                time_till_reset: timedelta = reset_time - current_time
                hours, remainder = divmod(time_till_reset.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)

                json_data['rate_limit_reset'] = {
                    "rate_limit_reset_unix": rate_limit_reset,
                    "rate_limit_reset_time": reset_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "current_time": current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "time_till_reset": {
                        "hours": int(hours),
                        "minutes": int(minutes),
                        "seconds": int(seconds)
                    }
                }
        else:
            json_data['error'] = f"Unable to fetch token info. Status code: {response.status_code}"

    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            raise AuthenticationError("Authentication failed: Bad credentials") from e
        if response.status_code == 403:
            raise RateLimitExceededError(f"Rate limit exceeded for {url}") from e
        if response.status_code == 404:
            raise NotFoundError(f"Resource not found for URL: {url}") from e
        raise RequestError(f"HTTP error occurred: {e}") from e
    except requests.exceptions.Timeout as e:
        raise RequestTimeoutError(f"Request timed out after {timeout} seconds") from e
    except requests.exceptions.RequestException as e:
        raise RequestError(f"An error occurred: {e}") from e

    return json_data
