"""
This module provides pytest fixtures for mocking HTTP requests in tests for the GitHub Extractor package.

Fixtures:
    - mock_requests: Mocks the requests.get and requests.put methods to simulate GitHub API responses,
    including handling of pagination headers.

Dependencies:
    - pytest: Used for writing and running tests.
    - requests: Used for making HTTP requests in the functions being tested.

MockResponse Class:
    - A mock response class to simulate the JSON response, status code, and headers of an HTTP request.
    - Includes methods to return JSON data, status code, headers, and to raise HTTP errors.

Functions:
    - create_paged_response: Creates a mock response for paginated GitHub API requests.
    - mock_get: Simulates the requests.get method with paging support, returning appropriate mock responses.
    - mock_put: Simulates the requests.put method, returning a generic mock response.

Example usage:
    To use the mock_requests fixture in a test, include it as an argument to the test function:

    def test_some_function(mock_requests):
        # Test code here

This allows you to test functions that make HTTP requests to the GitHub API without actually making network calls,
ensuring tests are fast, reliable, and do not depend on external services.
"""

from typing import Any, Dict, List, Optional

import re
import requests
import pytest


@pytest.fixture
def mock_requests(monkeypatch: Any) -> None:  # noqa: C901
    """
    Mock the requests.get and requests.put methods to simulate GitHub API responses.

    Arguments:
        monkeypatch (Any): The pytest monkeypatch fixture.

    Returns:
        None
    """
    class MockResponse:
        """A mock response class to simulate the JSON response and status code of an HTTP request."""

        def __init__(self, json_data: Any, status_code: int, headers: Optional[Dict[str, str]] = None) -> None:
            """
            Initialize the MockResponse instance.

            Arguments:
                json_data (Any): The JSON data to return in the response.
                status_code (int): The HTTP status code to return in the response.
                headers (Optional[Dict[str, str]]): The headers to return in the response.
            """
            self._json_data: Any = json_data
            self._status_code: int = status_code
            self._headers: Dict[str, str] = headers or {}

        def json(self) -> Any:
            """
            Simulate the JSON response of an HTTP request.

            Returns:
                Any: A dictionary representing the JSON response.
            """
            return self._json_data

        @property
        def status_code(self) -> int:
            """
            Simulate the status code of an HTTP response.

            Returns:
                int: The HTTP status code.
            """
            return self._status_code

        @property
        def headers(self) -> Dict[str, str]:
            """
            Simulate the headers of an HTTP response.

            Returns:
                Dict[str, str]: The headers of the HTTP response.
            """
            return self._headers

        def raise_for_status(self) -> None:
            """Simulate raising an exception for HTTP error responses."""
            if not 200 <= self._status_code < 300:
                raise requests.exceptions.HTTPError(response=self)

    def create_paged_response(items: List[Dict], page: int, per_page: int, total_items: int) -> MockResponse:
        """
        Create a paged response for the given items.

        Arguments:
            items (List[Dict]): The list of items to paginate.
            page (int): The current page number.
            per_page (int): The number of items per page.
            total_items (int): The total number of items available.

        Returns:
            MockResponse: The mock response for the given page.
        """
        start: int = (page - 1) * per_page
        end: int = start + per_page
        page_items: List[Dict] = items[start:end]
        next_url: str = f"https://api.github.com/resource?page={page + 1}"
        last_page: int = (total_items + per_page - 1) // per_page
        last_url: str = f"https://api.github.com/resource?page={last_page}"

        headers: Dict[str, str] = {
            'Link': f'<{next_url}>; rel="next", <{last_url}>; rel="last"'
        } if end < total_items else {}

        return MockResponse(page_items, 200, headers)

    def mock_get(url: str, headers: Dict[str, str], timeout: int, params: Optional[Dict[str, int]] = None) -> MockResponse:  # pylint: disable=unused-argument
        """
        Simulate the requests.get method with paging support.

        Arguments:
            url (str): The URL for the request.
            headers (Dict[str, str]): The headers for the request.
            timeout (int): The timeout for the request.
            params (Dict[str, int]): The query parameters for the request, including paging information.

        Returns:
            MockResponse: An instance of the MockResponse class.
        """
        if re.search(r"/user$", url):
            if headers.get('Authorization') == 'token invalid_token':
                return MockResponse({}, 401)
            return MockResponse({'login': 'testuser'}, 200)

        page: int = params.get("page", 1) if params else 1
        per_page: int = params.get("per_page", 100) if params else 100

        if re.search(r"/orgs/.*/repos", url):
            items: List[Dict] = [{"owner": {"login": "nottestuser"}, "full_name": f"repo{i}"} for i in range(1, 11)]
            total_items = 10
        elif re.search(r"/user/orgs", url):
            items = [{"owner": {"login": "nottestuser"}, "login": f"org{i}"} for i in range(1, 11)]
            total_items = 10
        elif re.search(r"/user/repos", url):
            items = [{"owner": {"login": "nottestuser"}, "full_name": f"user_repo{i}"} for i in range(1, 11)]
            total_items = 10
        else:
            return MockResponse({}, 404)

        return create_paged_response(items, page, per_page, total_items)

    def mock_put(*args: Any, **kwargs: Any) -> MockResponse:  # pylint: disable=unused-argument
        """
        Simulate the requests.put method.

        Arguments:
            *args (Any): Positional arguments.
            **kwargs (Any): Keyword arguments.

        Returns:
            MockResponse: An instance of the MockResponse class.
        """
        return MockResponse({}, 200)

    monkeypatch.setattr("requests.get", mock_get)
    monkeypatch.setattr("requests.put", mock_put)
