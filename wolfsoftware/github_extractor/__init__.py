"""
A simple Python package to interact with GitHub's API for listing organizations and repositories, with functionalities for authentication and filtering.

This package includes the following functionalities:
- Listing organizations from a GitHub extractor.
- Listing repositories for a user from GitHub.
- Listing repositories for a specified organization from GitHub.
- Retrieving the current version of the package.

Functions:
- get_authenticated_user: Retrieve the authenticated user's information from GitHub.
- list_organisations: List organizations using British English spelling.
- list_organizations: List organizations using American English spelling.
- list_user_repositories: List repositories for a user from GitHub.
- list_repositories_by_org: List repositories for a specified organization from GitHub.
- list_all_org_repositories: List all repositories for a user's organizations from GitHub.
- list_all_visible_repositories: List all visible repositories for a user from GitHub.

Attributes:
- __version__: The version of the package, retrieved from the package metadata.
- __all__: A list of all public symbols that the module exports.

Example usage:
    from wolfsoftware.github_extractor import (
        list_organisations,
        list_organizations,
        list_user_repositories,
        list_repositories_by_org
    )

    token = "your_github_token"
    orgs = list_organisations({'token': token})
    orgs_us = list_organizations({'token': token})
    user_repos = list_user_repositories({'token': token})
    org_repos = list_repositories_by_org({'token': token, 'org_name': "your_organization"})

This package is designed to be simple and intuitive, allowing users to easily retrieve organizational data from GitHub and manage repository listings.
"""

import importlib.metadata

from .exceptions import MissingTokenError, AuthenticationError, MissingOrgNameError, NotFoundError, RateLimitExceededError, RequestError, RequestTimeoutError
from .organisations import list_organisations, list_organizations, list_repositories_by_org, list_all_org_repositories
from .repositories import list_user_repositories, list_all_visible_repositories
from .token import get_token_information
from .user import get_authenticated_user

try:
    __version__: str = importlib.metadata.version('wolfsoftware.github_extractor')
except importlib.metadata.PackageNotFoundError:
    __version__ = 'unknown'

__all__: list[str] = [
    'get_token_information',
    'get_authenticated_user',
    'list_organisations',
    'list_organizations',
    'list_repositories_by_org',
    'list_all_org_repositories',
    'list_user_repositories',
    'list_all_visible_repositories',
    'MissingTokenError',
    'AuthenticationError',
    'MissingOrgNameError',
    'NotFoundError',
    'RateLimitExceededError',
    'RequestError',
    'RequestTimeoutError'
]
