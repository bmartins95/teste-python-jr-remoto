import os
import requests

class GithubApi:

    def __init__(self):
        self.API_URL = os.environ.get("GITHUB_API_URL", "https://api.github.com")
        self.GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

    def get_organization(self, login: str):
        """Busca uma organização no Github

        :login: login da organização no Github
        """
        url = "{}/orgs/{}".format(self.API_URL, login)
        r = requests.get(url, headers={"Authorization": "Basic {}".format(self.GITHUB_TOKEN)})
        return r

    def get_organization_public_members(self, login: str) -> int:
        """Retorna o número de membros públicos de uma organização

        :login: login da organização no Github
        """
        url = "{}/orgs/{}/members".format(self.API_URL, login)
        r = requests.get(url, headers={"Authorization": "Basic {}".format(self.GITHUB_TOKEN)})
        return len(r.json())

    def get_organization_public_repositories(self, login: str) -> int:
        """Retorna o número de repositórios públicos de uma organização

        :login: login da organização no Github
        """
        url = "{}/orgs/{}".format(self.API_URL, login)
        r = requests.get(url, headers={"Authorization": "Basic {}".format(self.GITHUB_TOKEN)})
        return r.json()["public_repos"]

    def get_organization_score(self, login: str) -> int:
        """Retorna o índice de prioridade de uma organização

        :login: login da organização no Github
        """
        employees = self.get_organization_public_members(login)
        repositories = self.get_organization_public_repositories(login)
        priority = employees + repositories
        return priority
