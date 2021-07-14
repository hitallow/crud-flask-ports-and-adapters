from typing import List, Optional
import requests
import os


from app.core.ports.user import GetUserInformationsFromGithubInterfacePort, GetUserMetricsGithubInterfacePort, GetUsersInformationsFromGithubWithUsername
from app.core.domain.user import GenderEnum, GithubUser, GithubUserInformations


class LoadGithubInformations(GetUserInformationsFromGithubInterfacePort,
                             GetUserMetricsGithubInterfacePort,
                             GetUsersInformationsFromGithubWithUsername
                             ):
    def __init__(self) -> None:
        self._base_url = os.environ.get('GITHU_URL', '')

    def _get_headers(self) -> dict:
        token = os.environ.get('GITHUB_API_TOKEN', '')
        return {
            'Content-Type': 'application/json',
            'Authorization': 'bearer %s' % (token)
        }

    def _build_graphql_body(self, graphql_query: str, variables: dict) -> dict:
        return {'query': graphql_query, 'variables': variables}

    def load_github_informations(self, username: str) -> Optional[GithubUser]:
        headers = self._get_headers()

        param_query: str = (
            """
            query getUser($login: String!){
                user(login:$login){
                    name
                    avatarUrl
                    email
                    login
                    bio
                }
            }
            """
        )

        body = self._build_graphql_body(
            graphql_query=param_query, variables={'login': username})

        response = requests.post(self._base_url, json=body, headers=headers)

        response_data = response.json()

        user: Optional[GithubUser] = None

        if response.status_code == 200 and 'data' in response_data and 'user' in response_data['data'] and response_data['data']['user'] is not None:
            json_user: dict = response.json()['data']['user']
            user = GithubUser(
                name=json_user['name'], profileImageUrl=json_user['avatarUrl'], bio=json_user[
                    'bio'], email=json_user['email'], login=json_user['login'], gender=json_user.get('gender', GenderEnum.NOTSPECIFIED)
            )

        return user

    def load_user_metrics(self, username: str) -> Optional[GithubUserInformations]:
        query: str = (
            """
            query getDetailProfile($login:String!){
                user(login:$login){
                    url 
                    repositories { totalCount }
                    followers { totalCount }
                    following { totalCount }
                }
            }
            """
        )
        body = self._build_graphql_body(
            graphql_query=query, variables={'login': username})
        headers = self._get_headers()

        response = requests.post(self._base_url,
                                 json=body, headers=headers)
        response_data = response.json()

        user: GithubUserInformations = None
        if response.status_code == 200 and 'data' in response_data and 'user' in response_data['data']:
            json_user: dict = response.json()['data']['user']
            total_followers = json_user['followers']['totalCount']
            total_following = json_user['following']['totalCount']
            total_public_repositories = json_user['repositories']['totalCount']
            profile_url = json_user['url']

            user = GithubUserInformations(
                profile_url=profile_url,
                total_followers=total_followers,
                total_following=total_following,
                total_public_repositories=total_public_repositories,
            )

        return user

    def load_users_by_username(self, username: str, limit: int = 50) -> List[GithubUser]:
        query = (
            """
            query getUsersByLogin($login : String!, $limit: Int!){
                search(type:USER,first:$limit,query:$login){
                    nodes {
                        ... on User{
                            name
                            avatarUrl
                            email
                            login
                            bio
                        }
                    }
                }
            }
            """
        )
        body = self._build_graphql_body(
            query, {'login': username, 'limit': limit})
        headers = self._get_headers()
        response = requests.post(self._base_url,
                                 json=body, headers=headers)
        response_json = response.json()
        users: List[GithubUser] = []
        if response.status_code == 200 and 'data' in response_json and 'search' in response_json['data'] and 'nodes' in response_json['data']['search']:
            item: dict
            for item in response_json['data']['search']['nodes']:
                users.append(
                    GithubUser(
                        name=item.get('name', ''),
                        email=item.get('email', ''),
                        login=item.get('login', ''),
                        bio=item.get('bio', ''),
                        profileImageUrl=item.get('avatarUrl', ''),
                        gender=item.get('gender', GenderEnum.NOTSPECIFIED)
                    )
                )

        return users
