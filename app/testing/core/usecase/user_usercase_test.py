from app.core.domain.user import GithubUser, GithubUserInformations, SaveUserDTO, User
from app.core.ports.user import GetUserInformationsFromGithubInterfacePort, GetUserMetricsGithubInterfacePort, GetUsersInformationsFromGithubWithUsername, LoadUserPort, SaveUserPort, UpdateUserPort
from unittest import TestCase
from unittest.mock import Mock

from app.core.usecase.user import LoadUserByEmailUsecase, LoadUserByUsernameUsecase, LoadUserProfileUsecase, LoadUsersUsecase, SaveUserUsecase, SaveUserWithGithubUsernameUsecase, UpdateUserUsecase


class InserNewUserTest(TestCase):
    def test_should_return_already_saved_email(self) -> None:
        mock_save_user_interface_port = SaveUserPort()
        mock_load_user_port = LoadUserPort()

        mock_load_user_port.load_user_by_email = Mock(return_value=User(
            id=1,
            bio="fake bio",
            email="any@email.com",
            last_name="Silver",
            name="John",
            username="johnsv"
        ))

        usecase = SaveUserUsecase(
            load_user_port=mock_load_user_port,
            save_user_interface_port=mock_save_user_interface_port
        )

        result, status_code = usecase.execute(
            userToSave=SaveUserDTO(
                username='fakeusername',
                email="fakeemail@email.com",
                name="fakename"
            )
        )
        mock_load_user_port.load_user_by_email.assert_called_with(
            email="fakeemail@email.com"
        )
        self.assertEqual(result['message'], 'User with same email saved')
        self.assertEqual(status_code, 400)

    def test_should_return_already_saved_user_username(self) -> None:
        mock_save_user_interface_port = SaveUserPort()
        mock_load_user_port = LoadUserPort()

        mock_load_user_port.load_user_by_email = Mock(return_value=None)

        mock_load_user_port.load_user_by_username = Mock(return_value=User(
            id=1,
            bio="fake bio",
            email="any@email.com",
            last_name="Silver",
            name="John",
            username="johnsv"
        ))

        usecase = SaveUserUsecase(
            load_user_port=mock_load_user_port,
            save_user_interface_port=mock_save_user_interface_port
        )

        result, status_code = usecase.execute(
            userToSave=SaveUserDTO(
                username='fakeusername',
                email="fakeemail@email.com",
                name="fakename"
            )
        )
        mock_load_user_port.load_user_by_email.assert_called_with(
            email="fakeemail@email.com"
        )
        mock_load_user_port.load_user_by_username.assert_called_with(
            username="fakeusername"
        )
        self.assertEqual(result['message'], 'User with same name saved')
        self.assertEqual(status_code, 400)

    def test_should_save_user(self) -> None:
        mock_save_user_interface_port = SaveUserPort()
        mock_load_user_port = LoadUserPort()

        mock_load_user_port.load_user_by_email = Mock(return_value=None)

        mock_load_user_port.load_user_by_username = Mock(return_value=None)

        mock_save_user_interface_port.save = Mock(return_value=User(
            id=1,
            bio="fake bio",
            email="any@email.com",
            last_name="Silver",
            name="John",
            username="johnsv"
        ))

        usecase = SaveUserUsecase(
            load_user_port=mock_load_user_port,
            save_user_interface_port=mock_save_user_interface_port
        )

        result, status_code = usecase.execute(
            userToSave=SaveUserDTO(
                username='fakeusername',
                email="fakeemail@email.com",
                name="fakename"
            )
        )
        saved_user: User = result['user']

        mock_save_user_interface_port.save.assert_called()
        mock_load_user_port.load_user_by_username.assert_called_with(
            username="fakeusername"
        )
        mock_load_user_port.load_user_by_email.assert_called_with(
            email="fakeemail@email.com",
        )
        self.assertEqual(saved_user.id, 1)
        self.assertEqual(status_code, 201)


class SaveUserWithGithubUsecaseTest(TestCase):
    def test_should_get_already_saved_user(self) -> None:
        mock_get_user_informations_port = GetUserInformationsFromGithubInterfacePort()
        mock_save_user_port = SaveUserPort()
        mock_load_user_port = LoadUserPort()
        mock_get_users_from_github_by_username_port = GetUsersInformationsFromGithubWithUsername()

        mock_load_user_port.load_user_by_username = Mock(return_value=User(
            id=1,
            bio="fake bio",
            email="any@email.com",
            last_name="Silver",
            name="John",
            username="johnsv"
        ))

        usecase = SaveUserWithGithubUsernameUsecase(
            get_github_informations_port=mock_get_user_informations_port,
            save_user_interface_port=mock_save_user_port,
            load_user_port=mock_load_user_port,
            get_users_from_github_by_username_port=mock_get_users_from_github_by_username_port,
        )

        result, status_code = usecase.execute(github_username="fakeusername")
        user_already_saved: User = result['user']

        mock_load_user_port.load_user_by_username.assert_called_with(
            username="fakeusername"
        )
        self.assertEqual(status_code, 201)
        self.assertEqual(user_already_saved.id, 1)

    def test_should_not_found_github_user(self) -> None:
        mock_get_user_informations_port = GetUserInformationsFromGithubInterfacePort()
        mock_save_user_port = SaveUserPort()
        mock_load_user_port = LoadUserPort()
        mock_get_users_from_github_by_username_port = GetUsersInformationsFromGithubWithUsername()

        mock_load_user_port.load_user_by_username = Mock(return_value=None)
        mock_get_user_informations_port.load_github_informations = Mock(
            return_value=None)
        mock_get_users_from_github_by_username_port.load_users_by_username = Mock(
            return_value=[])

        usecase = SaveUserWithGithubUsernameUsecase(
            get_github_informations_port=mock_get_user_informations_port,
            save_user_interface_port=mock_save_user_port,
            load_user_port=mock_load_user_port,
            get_users_from_github_by_username_port=mock_get_users_from_github_by_username_port,
        )

        result, status_code = usecase.execute(github_username="fakeusername")

        mock_load_user_port.load_user_by_username.assert_called_with(
            username="fakeusername"
        )
        mock_get_user_informations_port.load_github_informations.assert_called_with(
            username="fakeusername"
        )
        mock_get_users_from_github_by_username_port.load_users_by_username.assert_called_with(
            username="fakeusername", limit=50
        )

        self.assertEqual(result['message'], 'User not found on github')
        self.assertListEqual(result['availableUsers'], [])
        self.assertEqual(status_code, 404)

    def test_should_save_user_from_github(self) -> None:
        mock_get_user_informations_port = GetUserInformationsFromGithubInterfacePort()
        mock_save_user_port = SaveUserPort()
        mock_load_user_port = LoadUserPort()
        mock_get_users_from_github_by_username_port = GetUsersInformationsFromGithubWithUsername()

        mock_load_user_port.load_user_by_username = Mock(return_value=None)
        mock_get_user_informations_port.load_github_informations = Mock(
            return_value=GithubUser(
                name="fake name",
                bio="fake bio",
                email="any123@email.com",
                gender="",
                login="marlete",
                profileImageUrl="http://fakepath.com"
            ))
        mock_get_users_from_github_by_username_port.load_users_by_username = Mock(
            return_value=[])
        mock_save_user_port.save = Mock(return_value=User(
            id=21,
            bio="fake bio",
            email="any@email.com",
            last_name="Silver",
            name="John",
            username="johnsv"
        ))

        usecase = SaveUserWithGithubUsernameUsecase(
            get_github_informations_port=mock_get_user_informations_port,
            save_user_interface_port=mock_save_user_port,
            load_user_port=mock_load_user_port,
            get_users_from_github_by_username_port=mock_get_users_from_github_by_username_port,
        )

        result, status_code = usecase.execute(github_username="fakeusername")

        saved_user: User = result['user']

        mock_load_user_port.load_user_by_username.assert_called_with(
            username="fakeusername"
        )
        mock_get_user_informations_port.load_github_informations.assert_called_with(
            username="fakeusername"
        )
        mock_get_users_from_github_by_username_port.load_users_by_username.assert_not_called()
        self.assertEqual(saved_user.id, 21)
        self.assertEqual(saved_user.name, 'John')
        self.assertEqual(status_code, 201)


class LoadUserProfileUsecaseTest(TestCase):
    def test_should_not_found_user_by_id(self):
        mock_load_user_port = LoadUserPort()
        mock_get_user_metrics_port = GetUserMetricsGithubInterfacePort()

        mock_load_user_port.load_user_by_id = Mock(return_value=None)

        usecase = LoadUserProfileUsecase(
            get_user_metrics_port=mock_get_user_metrics_port,
            load_user_port=mock_load_user_port
        )

        result, status_code = usecase.execute(user_id=12)

        mock_load_user_port.load_user_by_id.assert_called_with(
            id=12
        )
        self.assertEqual(status_code, 404)
        self.assertEqual(result['message'], 'User not found')

    def test_should_return_user_without_metrics(self):
        mock_load_user_port = LoadUserPort()
        mock_get_user_metrics_port = GetUserMetricsGithubInterfacePort()

        mock_load_user_port.load_user_by_id = Mock(return_value=User(
            id=77,
            bio="any bio here",
            email="rigoni@email.com",
            last_name="Emidick",
            name="Rigonni",
            username="rigonni77"
        ))

        mock_get_user_metrics_port.load_user_metrics = Mock(return_value=GithubUserInformations(
            total_followers=10,
            profile_url="http://github.com/fakepage",
            total_following=20,
            total_public_repositories=21
        ))

        usecase = LoadUserProfileUsecase(
            get_user_metrics_port=mock_get_user_metrics_port,
            load_user_port=mock_load_user_port
        )

        result, status_code = usecase.execute(user_id=1)

        user: dict = result['user']

        mock_load_user_port.load_user_by_id.assert_called_with(
            id=1
        )
        mock_get_user_metrics_port.load_user_metrics.assert_called_with(
            user_login="rigonni77"
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(user['id'], 77)
        self.assertEqual(user['total_followers'], 10)
        self.assertEqual(user['total_following'], 20)
        self.assertEqual(user['total_public_repositories'], 21)


class LoadUserByEmailUsecaseTest(TestCase):
    def test_should_not_found_user(self):
        mock_load_user_port = LoadUserPort()
        mock_load_user_port.load_user_by_email = Mock(return_value=None)
        usecase = LoadUserByEmailUsecase(
            load_user_port=mock_load_user_port
        )

        result, status_code = usecase.execute(user_email="email@email.com")
        mock_load_user_port.load_user_by_email.assert_called_with(
            email="email@email.com"
        )
        self.assertEqual(status_code, 404)
        self.assertEqual(result['message'], 'User not found')

    def test_should_return_user(self):
        mock_load_user_port = LoadUserPort()
        mock_load_user_port.load_user_by_email = Mock(return_value=User(
            id=10,
            bio="i'm a holf",
            email="benitez@email.com",
            last_name="Benitez",
            name="Silva",
            username="benitez10"
        ))

        usecase = LoadUserByEmailUsecase(
            load_user_port=mock_load_user_port
        )

        result, status_code = usecase.execute(user_email="email@email.com")
        user: User = result['user']

        mock_load_user_port.load_user_by_email.assert_called_with(
            email="email@email.com"
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(user.id, 10)
        self.assertEqual(user.username, "benitez10")


class LoadUserByUsernameUsecaseTest(TestCase):
    def test_should_not_found_user(self) -> None:
        mock_load_user_port = LoadUserPort()
        mock_load_user_port.load_user_by_username = Mock(return_value=None)
        usecase = LoadUserByUsernameUsecase(
            load_user_port=mock_load_user_port
        )

        result, status_code = usecase.execute(user_username="jocaleri")

        mock_load_user_port.load_user_by_username.assert_called_with(
            username="jocaleri"
        )
        self.assertEqual(status_code, 404)
        self.assertEqual(result['message'], 'User not found')

    def test_should_return_user(self):
        mock_load_user_port = LoadUserPort()
        mock_load_user_port.load_user_by_username = Mock(return_value=User(
            id=9,
            bio="killer",
            email="jocaleri@email.com",
            last_name="Calleri",
            name="",
            username="jocaleri9"
        ))
        usecase = LoadUserByUsernameUsecase(
            load_user_port=mock_load_user_port
        )

        result, status_code = usecase.execute(user_username="jocaleri")
        user: User = result['user']

        mock_load_user_port.load_user_by_username.assert_called_with(
            username="jocaleri"
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(user.id, 9)
        self.assertEqual(user.username, 'jocaleri9')


class LoadUsersUsecaseTestCase(TestCase):
    def test_should_return_users(self):
        mock_load_user_port = LoadUserPort()
        mock_load_user_port.load_users = Mock(return_value=[])
        usecase = LoadUsersUsecase(
            load_user_port=mock_load_user_port
        )

        _, status_code = usecase.execute(limit=1, offset=2)

        mock_load_user_port.load_users.assert_called_with(
            limit=1, offset=2
        )
        self.assertEqual(status_code, 200)


class UpdateUserUsecaseTest(TestCase):
    def test_should_not_found_user(self):
        mock_load_user_port = LoadUserPort()
        mock_update_user_port = UpdateUserPort()
        mock_load_user_port.load_user_by_id = Mock(return_value=None)
        mock_update_user_port.update_user = Mock(return_value=None)

        usecase = UpdateUserUsecase(
            load_user_port=mock_load_user_port,
            update_user_port=mock_update_user_port
        )

        response, status_code = usecase.execute(50, User(
            id=50,
            bio="killer",
            email="johnwick@email.com",
            last_name="johnwixi",
            name="john",
            username="johnwick"
        ))
        mock_load_user_port.load_user_by_id.assert_called_with(50)
        mock_update_user_port.update_user.assert_not_called()
        self.assertEqual(status_code, 400)
        self.assertEqual(response['message'], 'User not found')

    def test_should_update_user(self):
        user_saved = User(
            id=54,
            bio="killer",
            email="johnwick@email.com",
            last_name="johnwixi2",
            name="johnw",
            username="johnwick2"
        )

        mock_load_user_port = LoadUserPort()
        mock_update_user_port = UpdateUserPort()

        mock_load_user_port.load_user_by_id = Mock(return_value=user_saved)
        mock_update_user_port.update_user = Mock(return_value=user_saved)

        usecase = UpdateUserUsecase(
            load_user_port=mock_load_user_port,
            update_user_port=mock_update_user_port
        )

        response, status_code = usecase.execute(54, User(
            id=54,
            bio="killer",
            email="johnwick@email.com",
            last_name="johnwixi",
            name="john",
            username="johnwick"
        ))
        user: User = response['user']

        mock_load_user_port.load_user_by_id.assert_called_with(54)
        mock_update_user_port.update_user.assert_called_once()

        self.assertEqual(status_code, 200)
        self.assertEqual(user.name, 'johnw')
        self.assertEqual(user.username, 'johnwick2')
