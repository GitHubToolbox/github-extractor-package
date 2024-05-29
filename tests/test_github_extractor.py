"""
This test module provides unit tests for the GitHub Extractor module using pytest.
It includes tests for versioning and various GitHub listing functions, ensuring correct
handling of authentication and filtering options.

Functions:
- test_version: Tests that a version is defined for the package.
- test_get_authenticated_user_success: Tests the get_authenticated_user function to ensure it returns the correct user data
  when valid credentials are provided.
- test_get_authenticated_user_bad_credentials: Tests the get_authenticated_user function to ensure it raises an AuthenticationError
  when invalid credentials are provided.
- test_list_organisations: Tests the list_organisations function to ensure it returns a list of dictionaries with ignored organizations
  filtered out.
- test_list_organisations_include: Tests the list_organisations function to ensure it returns only included organizations.
- test_list_user_repositories: Tests the list_user_repositories function to ensure it returns a list of dictionaries with ignored repositories
  filtered out.
- test_list_user_repositories_include: Tests the list_user_repositories function to ensure it returns only included repositories.
- test_list_repositories_by_org: Tests the list_repositories_by_org function to ensure it returns a list of dictionaries with ignored repositories
  filtered out.
- test_list_repositories_by_org_include: Tests the list_repositories_by_org function to ensure it returns only included repositories.

Dependencies:
- pytest: Used for writing and running tests.
- importlib.metadata: Used for retrieving package metadata.
- wolfsoftware.github_extractor: The module being tested, which contains functions for listing GitHub organizations and repositories.

Example usage:
    To run these tests, use the following command:
    pytest test_github_extractor.py
"""

from typing import Any, Dict, List, Optional, cast

import importlib.metadata
import re

import pytest

from wolfsoftware.github_extractor import list_organisations, list_user_repositories, list_repositories_by_org, get_authenticated_user, AuthenticationError


def test_version() -> None:
    """
    Test that a version is defined.

    Should return the version of the package.
    """
    version: Optional[str] = None

    try:
        version = importlib.metadata.version('wolfsoftware.github_extractor')
    except importlib.metadata.PackageNotFoundError:
        version = None

    assert version is not None, "Version should be set"  # nosec: B101
    assert version != 'unknown', f"Expected version, but got {version}"  # nosec: B101


def test_get_authenticated_user_success(mock_requests) -> None:  # pylint: disable=unused-argument
    """
    Test the get_authenticated_user function to ensure it returns the correct user data
    when valid credentials are provided.

    Arguments:
        mock_requests: The pytest fixture for mocking requests.

    This test verifies that the function correctly retrieves the authenticated user's login
    from the GitHub API using a dummy token.
    """
    token = 'dummy_token'  # nosec: B105
    timeout = 5

    user_data: Dict[str, Any] = get_authenticated_user({'token': token, 'timeout': timeout})

    assert isinstance(user_data, dict)  # nosec: B101
    assert user_data['login'] == 'testuser'  # nosec: B101


def test_get_authenticated_user_bad_credentials(mock_requests) -> None:  # pylint: disable=unused-argument
    """
    Test the get_authenticated_user function to ensure it raises an AuthenticationError
    when invalid credentials are provided.

    Arguments:
        mock_requests: The pytest fixture for mocking requests.

    This test simulates a 401 Unauthorized error response from the GitHub API and verifies
    that the function raises the custom AuthenticationError with the appropriate message.
    """
    token = 'invalid_token'  # nosec: B105
    timeout = 5

    with pytest.raises(AuthenticationError, match="Authentication failed: Bad credentials"):
        get_authenticated_user({'token': token, 'timeout': timeout})


def test_list_organisations(mock_requests) -> None:  # pylint: disable=unused-argument
    """
    Test the list_organisations function to ensure it returns a list of dictionaries.

    Arguments:
        mock_requests: The pytest fixture for mocking requests.
    """
    ignore_orgs: List[str] = ["org[1-3]"]
    organisations: List[Dict] | List[str] = list_organisations({'token': "dummy_token", 'ignore_orgs': ignore_orgs})

    assert isinstance(organisations, list)  # nosec: B101
    for org in organisations:
        assert isinstance(org, dict)  # nosec: B101
        assert not re.match(r"org[1-3]", org['login'], re.IGNORECASE)  # nosec: B101
    organisations_sorted: List[Dict[str, Any]] = sorted(cast(List[Dict[str, Any]], organisations), key=lambda org: org['login'].lower())
    assert organisations == organisations_sorted  # nosec: B101


def test_list_organisations_include(mock_requests) -> None:  # pylint: disable=unused-argument
    """
    Test the list_organisations function to ensure it returns only included organizations.

    Arguments:
        mock_requests: The pytest fixture for mocking requests.
    """
    include_orgs: List[str] = ["org[4-6]"]
    organisations: List[Dict] | List[str] = list_organisations({'token': "dummy_token", 'include_orgs': include_orgs})

    assert isinstance(organisations, list)  # nosec: B101
    for org in organisations:
        assert isinstance(org, dict)  # nosec: B101
        assert re.match(r"org[4-6]", org['login'], re.IGNORECASE)  # nosec: B101
    organisations_sorted: List[Dict[str, Any]] = sorted(cast(List[Dict[str, Any]], organisations), key=lambda org: org['login'].lower())
    assert organisations == organisations_sorted  # nosec: B101


def test_list_user_repositories(mock_requests) -> None:  # pylint: disable=unused-argument
    """
    Test the list_user_repositories function to ensure it returns a list of dictionaries.

    Arguments:
        mock_requests: The pytest fixture for mocking requests.
    """
    ignore_repos: List[str] = ["user_repo[1-3]"]
    repositories: List[Dict] | List[str] = list_user_repositories({'token': "dummy_token", 'ignore_repos': ignore_repos})

    assert isinstance(repositories, list)  # nosec: B101
    for repo in repositories:
        assert isinstance(repo, dict)  # nosec: B101
        assert not re.match(r"user_repo[1-3]", repo['full_name'], re.IGNORECASE)  # nosec: B101
    repositories_sorted: List[Dict[str, Any]] = sorted(cast(List[Dict[str, Any]], repositories), key=lambda repo: repo['full_name'].lower())
    assert repositories == repositories_sorted  # nosec: B101


def test_list_user_repositories_include(mock_requests) -> None:  # pylint: disable=unused-argument
    """
    Test the list_user_repositories function to ensure it returns only included repositories.

    Arguments:
        mock_requests: The pytest fixture for mocking requests.
    """
    include_repos: List[str] = ["user_repo[4-6]"]
    repositories: List[Dict] | List[str] = list_user_repositories({'token': "dummy_token", 'include_repos': include_repos})

    assert isinstance(repositories, list)  # nosec: B101
    for repo in repositories:
        assert isinstance(repo, dict)  # nosec: B101
        assert re.match(r"user_repo[4-6]", repo['full_name'], re.IGNORECASE)  # nosec: B101
    repositories_sorted: List[Dict[str, Any]] = sorted(cast(List[Dict[str, Any]], repositories), key=lambda repo: repo['full_name'].lower())
    assert repositories == repositories_sorted  # nosec: B101


def test_list_repositories_by_org(mock_requests) -> None:  # pylint: disable=unused-argument
    """
    Test the list_repositories_by_org function to ensure it returns a list of dictionaries.

    Arguments:
        mock_requests: The pytest fixture for mocking requests.
    """
    ignore_repos: List[str] = ["repo[1-3]"]
    repositories: List[Dict] | List[str] = list_repositories_by_org({'token': "dummy_token", 'org_name': "dummy_org", 'ignore_repos': ignore_repos})

    assert isinstance(repositories, list)  # nosec: B101
    for repo in repositories:
        assert isinstance(repo, dict)  # nosec: B101
        assert not re.match(r"repo[1-3]", repo['full_name'], re.IGNORECASE)  # nosec: B101
    repositories_sorted: List[Dict[str, Any]] = sorted(cast(List[Dict[str, Any]], repositories), key=lambda repo: repo['full_name'].lower())
    assert repositories == repositories_sorted  # nosec: B101


def test_list_repositories_by_org_include(mock_requests) -> None:  # pylint: disable=unused-argument
    """
    Test the list_repositories_by_org function to ensure it returns only included repositories.

    Arguments:
        mock_requests: The pytest fixture for mocking requests.
    """
    include_repos: List[str] = ["repo[4-6]"]
    repositories: List[Dict] | List[str] = list_repositories_by_org({'token': "dummy_token", 'org_name': "dummy_org", 'include_repos': include_repos})

    assert isinstance(repositories, list)  # nosec: B101
    for repo in repositories:
        assert isinstance(repo, dict)  # nosec: B101
        assert re.match(r"repo[4-6]", repo['full_name'], re.IGNORECASE)  # nosec: B101
    repositories_sorted: List[Dict[str, Any]] = sorted(cast(List[Dict[str, Any]], repositories), key=lambda repo: repo['full_name'].lower())
    assert repositories == repositories_sorted  # nosec: B101
