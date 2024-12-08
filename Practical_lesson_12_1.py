def request_in_github(path: str = "", url: str = "") -> dict:
    import requests

    if not url:
        url = f'https://api.github.com/repos/{path}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Ошибка при запросе в github")


def convert_user_data(user_info: dict, repo_name: str) -> str:
    data = {
        'company': user_info.get('company'),
        'created_at': user_info.get('created_at'),
        'email': user_info.get('email'),
        'id': user_info.get('id'),
        'name': user_info.get('login'),
        'url': user_info.get('url')
    }
    return '{\n' + ',\n'.join([f'"{key}": "{value}"' for key, value in data.items()]) + '\n}'


def main(path: str):
    try:
        github_info = request_in_github(path)
        user_url = github_info['owner']['url']
        user_info = request_in_github(url=user_url)
        result = convert_user_data(user_info, repo_name=path)
        print(result)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main(path="firehol/blocklist-ipsets")