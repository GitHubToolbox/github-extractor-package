"""
This module provides a generic way to interact with the GitHub API and collate the response into JSON format.

It handles pagination and error handling for the API requests.

Functions:
- generate_github_headers: Generates the necessary headers for authenticating GitHub API requests using a provided token.
- github_api: Makes a GET request to the specified GitHub API URL using the provided token, handles pagination, and returns the
  response as a list of dictionaries.

Dependencies:
- requests: Used for making HTTP requests to the GitHub API.
- exceptions: Contains custom exceptions for handling errors.

Example usage:
    from .github_api import github_api

    token = "your_github_token"
    url = "https://api.github.com/user/orgs"
    response_data = github_api(url, token)
"""

from typing import Any, Dict, List, Optional

import requests

from .constants import DEFAULT_TIMEOUT
from .exceptions import AuthenticationError, RateLimitExceededError, RequestError, RequestTimeoutError, NotFoundError


def generate_github_headers(token: Optional[str] = None, accept_header: Optional[str] = None) -> Dict[str, str]:
    """
    Generate the necessary headers for authenticating GitHub API requests using a provided token.

    Arguments:
        token (Optional[str]): The GitHub API token. Default is None.
        accept_header (Optional[str]): The Accept header for the request. Default is 'application/vnd.github.v3+json'.

    Returns:
        Dict[str, str]: A dictionary containing the headers for the GitHub API request.
    """
    headers: Dict[str, str] = {
        'Accept': accept_header or 'application/vnd.github.v3+json'
    }
    if token:
        headers['Authorization'] = f'token {token}'
    return headers


def github_api(  # noqa: C901  pylint: disable=too-many-branches
    url: str,
    token: Optional[str] = None,
    timeout: Optional[int] = DEFAULT_TIMEOUT,
    accept_header: Optional[str] = None
) -> List[Dict]:
    """
    Make a GET request to the specified GitHub API URL using the provided token, handles pagination, and returns the response as a list of dictionaries.

    Arguments:
        url (str): The GitHub API URL to request.
        token (Optional[str]): The GitHub API token. Default is None.
        timeout (int): Timeout for the request in seconds. Default is 10 seconds.
        accept_header (Optional[str]): The Accept header for the request. Default is 'application/vnd.github.v3+json'.

    Returns:
        List[Dict]: A list of dictionaries representing the API response data if successful, otherwise an empty list.

    Raises:
        AuthenticationError: If authentication fails due to bad credentials.
        requests.exceptions.HTTPError: For other HTTP errors.
        requests.exceptions.Timeout: If the request times out.
        requests.exceptions.RequestException: For other request exceptions.
    """
    headers: Dict[str, str] = generate_github_headers(token, accept_header)
    json_data: List[Dict] = []
    page: int = 1
    next_url = None

    while True:
        try:
            response: requests.Response = requests.get(
                url, headers=headers, timeout=timeout, params={'page': page, 'per_page': 100}
            )
            response.raise_for_status()

            page_data: Any = response.json()

            if response.status_code == 200:
                if isinstance(page_data, list):
                    json_data.extend(page_data)
                elif isinstance(page_data, dict):
                    json_data.append(page_data)

                # Check for pagination
                links: Optional[str] = response.headers.get('Link')
                if not links:
                    break

                next_url = None
                for link in links.split(','):
                    if 'rel="next"' in link:
                        next_url = link[link.find('<') + 1:link.find('>')]
                        break

                if not next_url or next_url == url:
                    break
                url = next_url
                page += 1
                next_url = None
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


def github_api_no_paging(
    url: str,
    token: Optional[str] = None,
    timeout: Optional[int] = DEFAULT_TIMEOUT,
    accept_header: Optional[str] = None
) -> Dict[str, Any]:
    """
    Make a GET request to the specified GitHub API URL using the provided token and returns the response as a dictionary.

    Arguments:
        url (str): The GitHub API URL to request.
        token (Optional[str]): The GitHub API token. Default is None.
        timeout (int): Timeout for the request in seconds. Default is 10 seconds.
        accept_header (Optional[str]): The Accept header for the request. Default is 'application/vnd.github.v3+json'.

    Returns:
        Dict[str, Any]: A dictionary representing the API response data if successful, otherwise an empty dictionary.

    Raises:
        AuthenticationError: If authentication fails due to bad credentials.
        requests.exceptions.HTTPError: For other HTTP errors.
        requests.exceptions.Timeout: If the request times out.
        requests.exceptions.RequestException: For other request exceptions.
    """
    headers: Dict[str, str] = generate_github_headers(token, accept_header)

    try:
        response: requests.Response = requests.get(
            url, headers=headers, timeout=timeout
        )
        response.raise_for_status()

        json_data: Dict[str, Any] = response.json()
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
