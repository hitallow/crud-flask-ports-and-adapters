from unittest import TestCase

from app.core.domain.user import User, GithubUser, GithubUserInformations, SaveUserDTO


class TestUserModel(TestCase):
    def test_user_is_intances_with_success(self):
        user = User(
            id=1,
            bio="fake bio",
            email="any@email.com",
            last_name="Silver",
            name="John",
            username="johnsv"
        )
        self.assertEqual(user.id, 1)
        self.assertEqual(user.bio, "fake bio")
        self.assertEqual(user.email, "any@email.com")
        self.assertEqual(user.last_name, "Silver")
        self.assertEqual(user.name, "John")
        self.assertEqual(user.username, "johnsv")


class TesteGithubUser(TestCase):
    def teste_github_istance_correct(self) -> None:
        github_user = GithubUser(
            name="fake name",
            bio="fake bio",
            email="any123@email.com",
            gender="",
            login="marlete",
            profileImageUrl="http://fakepath.com"
        )

        self.assertEqual(github_user.name, "fake name")
        self.assertEqual(github_user.bio, "fake bio")
        self.assertEqual(github_user.email, "any123@email.com")
        self.assertEqual(github_user.gender, "")
        self.assertEqual(github_user.login, "marlete")
        self.assertEqual(github_user.profileImageUrl, "http://fakepath.com")


class TesteGithuUserMetrics(TestCase):
    def teste_github_metrics_instace_correct(self) -> None:
        github_metrics = GithubUserInformations(
            profile_url="http://github.com/fake",
            total_followers=10,
            total_following=20,
            total_public_repositories=50
        )
        self.assertEqual(github_metrics.profile_url, "http://github.com/fake")
        self.assertEqual(github_metrics.total_followers, 10)
        self.assertEqual(github_metrics.total_following, 20)
        self.assertEqual(github_metrics.total_public_repositories, 50)


class TesteUserDTO(TestCase):
    def test_instance_is_correct(self) -> None:
        user_dto = SaveUserDTO(
            email="fake@email.com",
            name="fakename",
            username="anylogin"
        )
        self.assertEqual(user_dto.email, "fake@email.com")
        self.assertEqual(user_dto.name, "fakename")
        self.assertEqual(user_dto.username, "anylogin")
