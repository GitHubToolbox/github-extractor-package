<!-- markdownlint-disable -->
<p align="center">
    <a href="https://github.com/GitHubToolbox/">
        <img src="https://cdn.wolfsoftware.com/assets/images/github/organisations/githubtoolbox/black-and-white-circle-256.png" alt="GitHubToolbox logo" />
    </a>
    <br />
    <a href="https://github.com/GitHubToolbox/github-extractor-package/actions/workflows/cicd.yml">
        <img src="https://img.shields.io/github/actions/workflow/status/GitHubToolbox/github-extractor-package/cicd.yml?branch=master&label=build%20status&style=for-the-badge" alt="Github Build Status" />
    </a>
    <a href="https://github.com/GitHubToolbox/github-extractor-package/blob/master/LICENSE.md">
        <img src="https://img.shields.io/github/license/GitHubToolbox/github-extractor-package?color=blue&label=License&style=for-the-badge" alt="License">
    </a>
    <a href="https://github.com/GitHubToolbox/github-extractor-package">
        <img src="https://img.shields.io/github/created-at/GitHubToolbox/github-extractor-package?color=blue&label=Created&style=for-the-badge" alt="Created">
    </a>
    <br />
    <a href="https://github.com/GitHubToolbox/github-extractor-package/releases/latest">
        <img src="https://img.shields.io/github/v/release/GitHubToolbox/github-extractor-package?color=blue&label=Latest%20Release&style=for-the-badge" alt="Release">
    </a>
    <a href="https://github.com/GitHubToolbox/github-extractor-package/releases/latest">
        <img src="https://img.shields.io/github/release-date/GitHubToolbox/github-extractor-package?color=blue&label=Released&style=for-the-badge" alt="Released">
    </a>
    <a href="https://github.com/GitHubToolbox/github-extractor-package/releases/latest">
        <img src="https://img.shields.io/github/commits-since/GitHubToolbox/github-extractor-package/latest.svg?color=blue&style=for-the-badge" alt="Commits since release">
    </a>
    <br />
    <a href="https://github.com/GitHubToolbox/github-extractor-package/blob/master/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Code%20of%20Conduct-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/GitHubToolbox/github-extractor-package/blob/master/.github/CONTRIBUTING.md">
        <img src="https://img.shields.io/badge/Contributing-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/GitHubToolbox/github-extractor-package/blob/master/.github/SECURITY.md">
        <img src="https://img.shields.io/badge/Report%20Security%20Concern-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/GitHubToolbox/github-extractor-package/issues">
        <img src="https://img.shields.io/badge/Get%20Support-blue?style=for-the-badge" />
    </a>
</p>

## Overview

The GitHub Extractor package is a Python library designed to facilitate the extraction of data from GitHub.

This package provides functions to fetch information about repositories, including languages used, releases, contributors, topics, workflows,
and more with robust error handling and configuration support.

## Features

- List organizations for a user from GitHub.
- List repositories for a user from GitHub.
- List repositories for a specified organization from GitHub.
- Support for authentication using GitHub API tokens.
- Filtering of organizations and repositories based on given patterns.
- Pagination handling for API requests.

## Installation

You can install GitHub Extractor via pip:

```bash
pip install wolfsoftware.github-extractor
```

## Usage

### Getting Token information

You an get basic information relating to the given token.

There is also a specific command line tool for this [Github Token Validator](https://github.com/GitHubToolbox/github-token-validator).

```python
from wolfsoftware.github_extractor import get_token_information

config = {
    "token": "your_github_token",
}
```

<details>

<summary>Parameters</summary>

| Name    | Required | Purpose                                                                    |
| :------ | :------: | :------------------------------------------------------------------------- |
| token   | Yes      | Authentication for the GitHub API.                                         |
| timeout | No       | The timeout to use when talking to the GitHub API (default is 10 seconds). |
| slugs   | No       | Should we return the results as slugs. (List of names and nothing else).   |

</details>

### Getting User Information

You an get basic information relating to the authenticated user (owner of the token). The information will be limited by the scope
of the token.

```python
from wolfsoftware.github_extractor import get_authenticated_user

config = {
    "token": "your_github_token",
}
```

<details>

<summary>Parameters</summary>

| Name    | Required | Purpose                                                                    |
| :------ | :------: | :------------------------------------------------------------------------- |
| token   | Yes      | Authentication for the GitHub API.                                         |
| timeout | No       | The timeout to use when talking to the GitHub API (default is 10 seconds). |
| slugs   | No       | Should we return the results as slugs. (List of names and nothing else).   |

</details>

### Listing Organizations

You can list organizations that you are a member of using British or American English spelling.

```python
from wolfsoftware.github_extractor import list_organisations, list_organizations

config = {
    "token": "your_github_token",
    "ignore_orgs": ["Test*"]
}

# Using British English spelling
organisations = list_organisations(config)

# Using American English spelling
organisations_us = list_organizations(config)
```

<details>

<summary>Parameters</summary>

| Name    | Required | Purpose                                                                    |
| :------ | :------: | :------------------------------------------------------------------------- |
| token   | Yes      | Authentication for the GitHub API.                                         |
| timeout | No       | The timeout to use when talking to the GitHub API (default is 10 seconds). |
| slugs   | No       | Should we return the results as slugs. (List of names and nothing else).   |

</details>

<details>

<summary>Filtering Parameters</summary>

| Name         | Required | Purpose                                                   |
| :----------- | :------: | :-------------------------------------------------------- |
| include_orgs | No       | A list of organisation names to include in the results.   |
| ignore_orgs  | No       | A list of organisation names to exclude from the results. |
| get_members  | No       | Should we include organisation members in the results.    |

</details>

### Listing User Repositories

You can list repositories for a user with optional filters:

```python
from wolfsoftware.github_extractor import list_user_repositories

config = {
    "token": "your_github_token",
    "ignore_repos": ["Test*"],
    "include_repos": ["Project*"]
}

repositories = list_user_repositories(config)
```

<details>

<summary>Parameters</summary>

| Name          | Required | Purpose                                                                                                  |
| :------------ | :------: | :------------------------------------------------------------------------------------------------------- |
| token         | No       | Authentication for the GitHub API.                                                                       |
| timeout       | No       | The timeout to use when talking to the GitHub API (default is 10 seconds).                               |
| slugs         | No       | Should we return the results as slugs. (List of names and nothing else).                                 |
| username      | No       | The GitHub username to list repositories for. (Authenticated user will be used is this is not supplied). |

</details>

<details>

<summary>Additional Data Parameter</summary>

| Name             | Required | Purpose                                                   |
| :--------------- | :------: | :-------------------------------------------------------- |
| get_branches     | No       | Add details about all branches to each repository.        |
| get_contributors | No       | Add details about all contributors to each repository.    |
| get_languages    | No       | Add the list of identified languages for each repository. |
| get_releases     | No       | Add details about all releases to each repository.        |
| get_tags         | No       | Add details about all tags to each  repository.           |
| get_topics       | No       | Add the list of defined topics to each repository.        |
| get_workflows    | No       | Add details about all workflows to each repository.       |

</details>

<details>

<summary>Filtering Parameter</summary>

| Name          | Required | Purpose                                                                       |
| :------------ | :------: | :---------------------------------------------------------------------------- |
| include_names | No       | A list of repository names to include in the results.                         |
| ignore_names  | No       | A list of repository names to exclude from the results.                       |
| include_repos | No       | A list of organisation names/repository names to include in the results.      |
| ignore_repos  | No       | A list of organisation names/repository names to exclude from the results.    |
| skip_private  | No       | Do not include private repositories, this is for the authenticated user only. |

> ignore and include names use the full name of the repository, which is the organisation name / repository name E.g. GitHubToolbox/github-extractor-package

</details>

### Listing Repositories by Organization

You can list repositories for a specific organization with optional filters:

```python
from wolfsoftware.github_extractor import list_repositories_by_org

config = {
    "token": "your_github_token",
    "org_name": "your_organization",
    "ignore_repos": ["Test*"],
    "include_repos": ["Project*"]
}

repositories = list_repositories_by_org(config)
```

<details>

<summary>Parameters</summary>

| Name     | Required | Purpose                                                                    |
| :------- | :------: | :------------------------------------------------------------------------- |
| token    | No       | Authentication for the GitHub API.                                         |
| timeout  | No       | The timeout to use when talking to the GitHub API (default is 10 seconds). |
| slugs    | No       | Should we return the results as slugs. (List of names and nothing else).   |
| org_name | No       | The GitHub organisation to list repositories for.                          |

</details>

<details>

<summary>Additional Data Parameter</summary>

| Name             | Required | Purpose                                                   |
| :--------------- | :------: | :-------------------------------------------------------- |
| get_branches     | No       | Add details about all branches to each repository.        |
| get_contributors | No       | Add details about all contributors to each repository.    |
| get_languages    | No       | Add the list of identified languages for each repository. |
| get_releases     | No       | Add details about all releases to each repository.        |
| get_tags         | No       | Add details about all tags to each  repository.           |
| get_topics       | No       | Add the list of defined topics to each repository.        |
| get_workflows    | No       | Add details about all workflows to each repository.       |

</details>

<details>

<summary>Filtering Parameter</summary>

| Name          | Required | Purpose                                                                       |
| :------------ | :------: | :---------------------------------------------------------------------------- |
| include_names | No       | A list of repository names to include in the results.                         |
| ignore_names  | No       | A list of repository names to exclude from the results.                       |
| include_repos | No       | A list of organisation names/repository names to include in the results.      |
| ignore_repos  | No       | A list of organisation names/repository names to exclude from the results.    |
| skip_private  | No       | Do not include private repositories, this is for the authenticated user only. |

> ignore and include names use the full name of the repository, which is the organisation name / repository name E.g. GitHubToolbox/github-extractor-package

</details>

### Listing all Organisation Repositories

You can list all repositories for all organisations you're a member of.

```python
from wolfsoftware.github_extractor import list_all_org_repositories

config = {
    "token": "your_github_token",
    "ignore_repos": ["Test*"],
    "include_repos": ["Project*"]
}

repositories = list_all_org_repositories(config)
```

<details>

<summary>Parameters</summary>

| Name          | Required | Purpose                                                                                                  |
| :------------ | :------: | :------------------------------------------------------------------------------------------------------- |
| token         | Yes      | Authentication for the GitHub API.                                                                       |
| timeout       | No       | The timeout to use when talking to the GitHub API (default is 10 seconds).                               |
| slugs         | No       | Should we return the results as slugs. (List of names and nothing else).                                 |

</details>

<details>

<summary>Additional Data Parameter</summary>

| Name             | Required | Purpose                                                   |
| :--------------- | :------: | :-------------------------------------------------------- |
| get_branches     | No       | Add details about all branches to each repository.        |
| get_contributors | No       | Add details about all contributors to each repository.    |
| get_languages    | No       | Add the list of identified languages for each repository. |
| get_releases     | No       | Add details about all releases to each repository.        |
| get_tags         | No       | Add details about all tags to each  repository.           |
| get_topics       | No       | Add the list of defined topics to each repository.        |
| get_workflows    | No       | Add details about all workflows to each repository.       |

</details>

<details>

<summary>Filtering Parameter</summary>

| Name          | Required | Purpose                                                                       |
| :------------ | :------: | :---------------------------------------------------------------------------- |
| include_names | No       | A list of repository names to include in the results.                         |
| ignore_names  | No       | A list of repository names to exclude from the results.                       |
| include_repos | No       | A list of organisation names/repository names to include in the results.      |
| ignore_repos  | No       | A list of organisation names/repository names to exclude from the results.    |
| skip_private  | No       | Do not include private repositories, this is for the authenticated user only. |

> ignore and include names use the full name of the repository, which is the organisation name / repository name E.g. GitHubToolbox/github-extractor-package

</details>

### Listing all Visible Repositories

You can list repositories that you are able to access.

```python
from wolfsoftware.github_extractor import list_all_visible_repositories

config = {
    "token": "your_github_token",
    "ignore_repos": ["Test*"],
    "include_repos": ["Project*"]
}

repositories = list_all_visible_repositories(config)
```

<details>

<summary>Parameters</summary>

| Name          | Required | Purpose                                                                                                  |
| :------------ | :------: | :------------------------------------------------------------------------------------------------------- |
| token         | Yes      | Authentication for the GitHub API.                                                                       |
| timeout       | No       | The timeout to use when talking to the GitHub API (default is 10 seconds).                               |
| slugs         | No       | Should we return the results as slugs. (List of names and nothing else).                                 |

</details>

<details>

<summary>Additional Data Parameter</summary>

| Name             | Required | Purpose                                                   |
| :--------------- | :------: | :-------------------------------------------------------- |
| get_branches     | No       | Add details about all branches to each repository.        |
| get_contributors | No       | Add details about all contributors to each repository.    |
| get_languages    | No       | Add the list of identified languages for each repository. |
| get_releases     | No       | Add details about all releases to each repository.        |
| get_tags         | No       | Add details about all tags to each  repository.           |
| get_topics       | No       | Add the list of defined topics to each repository.        |
| get_workflows    | No       | Add details about all workflows to each repository.       |

</details>

<details>

<summary>Filtering Parameter</summary>

| Name          | Required | Purpose                                                                       |
| :------------ | :------: | :---------------------------------------------------------------------------- |
| include_names | No       | A list of repository names to include in the results.                         |
| ignore_names  | No       | A list of repository names to exclude from the results.                       |
| include_repos | No       | A list of organisation names/repository names to include in the results.      |
| ignore_repos  | No       | A list of organisation names/repository names to exclude from the results.    |
| skip_private  | No       | Do not include private repositories, this is for the authenticated user only. |

> ignore and include names use the full name of the repository, which is the organisation name / repository name E.g. GitHubToolbox/github-extractor-package

</details>

### Exceptions

The following custom exceptions are used:

| Name                   | Purpose                                                                                        |
| :--------------------- | :--------------------------------------------------------------------------------------------- |
| AuthenticationError    | Raised when authentication fails. This is caused by an invalid token.                          |
| MissingOrgNameError    | Raised when the organization name is missing.                                                  |
| MissingTokenError      | Raised when the GitHub API token is missing but is required.                                   |
| NotFoundError          | Raised when a requested resource is not found. This is caused by incorrect scope of the token. |
| RateLimitExceededError | Raised when the GitHub API rate limit is exceeded.                                             |
| RequestError           | Raised for general request errors.                                                             |
| RequestTimeoutError    | Raised when a request times out.                                                               |

<br />
<p align="right"><a href="https://wolfsoftware.com/"><img src="https://img.shields.io/badge/Created%20by%20Wolf%20on%20behalf%20of%20Wolf%20Software-blue?style=for-the-badge" /></a></p>
