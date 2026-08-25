import requests
from collections import Counter

API_BASE = "https://api.github.com"


def get_user(username):
    response = requests.get(
        f"{API_BASE}/users/{username}",
        timeout=20
    )
    response.raise_for_status()
    return response.json()


def get_repositories(username):
    repositories = []
    page = 1

    while True:
        response = requests.get(
            f"{API_BASE}/users/{username}/repos",
            params={
                "per_page": 100,
                "page": page,
                "sort": "updated",
            },
            timeout=20,
        )
        response.raise_for_status()

        batch = response.json()

        if not batch:
            break

        repositories.extend(batch)
        page += 1

    return repositories


def analyze_profile(username):
    user = get_user(username)
    repos = get_repositories(username)

    languages = Counter(
        repo["language"]
        for repo in repos
        if repo.get("language")
    )

    total_stars = sum(repo["stargazers_count"] for repo in repos)
    total_forks = sum(repo["forks_count"] for repo in repos)

    print("\n" + "=" * 55)
    print("GITHUB RESEARCH PROFILE ANALYZER")
    print("=" * 55)

    print(f"\nName              : {user.get('name') or username}")
    print(f"Username          : {user['login']}")
    print(f"Public repositories: {user['public_repos']}")
    print(f"Followers         : {user['followers']}")
    print(f"Following         : {user['following']}")
    print(f"Total stars       : {total_stars}")
    print(f"Total forks       : {total_forks}")

    print("\nMost Used Languages")
    print("-" * 30)

    if languages:
        for language, count in languages.most_common():
            print(f"{language:<20} {count}")
    else:
        print("No language information available.")

    print("\nRecently Updated Repositories")
    print("-" * 30)

    for repo in repos[:5]:
        print(f"- {repo['name']}")

    print("\nGitHub API:")
    print("https://api.github.com")
    print("=" * 55)


if __name__ == "__main__":
    username = input("Enter a GitHub username: ").strip()

    try:
        analyze_profile(username)
    except requests.RequestException as error:
        print(f"GitHub API request failed: {error}")
