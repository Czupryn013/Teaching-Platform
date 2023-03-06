from unittest.mock import patch

import pytest
from werkzeug.security import check_password_hash

from teaching_platform.models.users.db_handler import *
from teaching_platform.models.models import User, Role
from teaching_platform.models.users import exceptions
from teaching_platform.models import validation

#in normal running validation.py needs ../config.yaml but in tests only config.yaml works


@pytest.fixture
def user_data():
    return {
        "id": 1,
        "username": "test_user",
        "password": "Testpassword123!!",
        "email": "testuser1@test.com"
    }


@pytest.fixture
def user(user_data):
    return User(
        id=1,
        username=user_data["username"],
        password=validation.validate_password(user_data["password"]),
        email=user_data["email"],
        role=Role.UNCOMFIRMED)


@patch("teaching_platform.models.users.db_handler.db.session")
@patch("teaching_platform.models.users.db_handler.User")
def test_add_user(mock_user, mock_session, user_data):
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_user.query.filter_by.return_value.all.return_value = None

    add_user(user_data["username"], user_data["password"], user_data["email"])

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

@patch("teaching_platform.models.users.db_handler.User")
def test_add_user_username_taken(mock_user, user_data, user):
    mock_user.query.filter_by.return_value.all.return_value = [user]

    with pytest.raises(exceptions.UsernameTakenError):
        add_user(user_data["username"], user_data["password"], "new_email@com.pl")

#test nie działa bo UsernameTakenError jest wyrzucane najpierw
# @patch("teaching_platform.models.users.db_handler.User")
# def test_add_user_email_taken(mock_user, user_data, user):
#     mock_user.query.filter_by.return_value.all.return_value = [user]
#
#     with pytest.raises(exceptions.EmailTakenError):
#         add_user("new_username", user_data["password"], user_data["email"])

@patch("teaching_platform.models.users.db_handler.db.session")
@patch("teaching_platform.models.users.db_handler.User")
def test_remove_user(mock_user, mock_session, user_data, user):
    mock_user.query.filter_by.return_value.first.return_value = user
    mock_user.query.filter_by.return_value.delete.return_value = None
    mock_session.commit.return_value = None

    remove_user(user_data["id"])

    #how to assert that user.lessons was deleted?

    mock_user.query.filter_by.return_value.delete.assert_called_once()
    mock_session.commit.assert_called_once()

@patch("teaching_platform.models.users.db_handler.db.session")
@patch("teaching_platform.models.users.db_handler.User")
def test_remove_user_user_dosent_exist(mock_user, mock_session, user_data, user):
    mock_user.query.filter_by.return_value.first.return_value = None
    mock_session.commit.return_value = None

    with pytest.raises(exceptions.UserDosentExistError):
        remove_user(user_data["id"])

@patch("teaching_platform.models.users.db_handler.User")
def test_get_all_users(mock_user):
    mock_user.query.all.return_value = [user]

    results = get_all_users()

    assert results == [user]

@patch("teaching_platform.models.users.db_handler.User")
def test_get_user(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = user

    result = get_user(user_data["id"])

    assert result == user

@patch("teaching_platform.models.users.db_handler.User")
def test_get_user_user_user_dosent_exist(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = None

    with pytest.raises(exceptions.UserDosentExistError):
        get_user(user_data["id"])

@patch("teaching_platform.models.users.db_handler.User")
def test_get_user_by_email(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = user

    result = get_user_by_email(user_data["email"])

    assert result == user

@patch("teaching_platform.models.users.db_handler.User")
def test_get_user_by_email_user_dosent_exist(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = None

    with pytest.raises(exceptions.UserDosentExistError):
        get_user_by_email(user_data["email"])

@patch("teaching_platform.models.users.db_handler.db.session")
@patch("teaching_platform.models.users.db_handler.User")
def test_update_username(mock_user, mock_session, user, user_data):
    new_username = "new_username"
    mock_user.query.filter_by.return_value.first.return_value = user
    mock_session.commit.return_value = None

    update_username(new_username, user_data["id"])

    assert user.username == new_username

@patch("teaching_platform.models.users.db_handler.User")
def test_update_username_validation(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = user


    with pytest.raises(exceptions.IncorrectUsername):
        update_username("", user_data["id"])

@patch("teaching_platform.models.users.db_handler.User")
def test_update_username_user_user_dosent_exist(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = None

    with pytest.raises(exceptions.UserDosentExistError):
        update_username("new_username", user_data["id"])

@patch("teaching_platform.models.users.db_handler.User")
def test_check_auth(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = user
    result = check_auth(user_data["username"], user_data["password"])

    assert result == user

@patch("teaching_platform.models.users.db_handler.User")
def test_check_auth_user_user_dosent_exist(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = None

    with pytest.raises(exceptions.AuthError):
        check_auth(user_data["username"], user_data["password"])

@patch("teaching_platform.models.users.db_handler.User")
def test_check_auth_wrong_password(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = user

    with pytest.raises(exceptions.AuthError):
        check_auth(user_data["username"], "wrong_password_123!")

@patch("teaching_platform.models.users.db_handler.db.session")
@patch("teaching_platform.models.users.db_handler.User")
def test_update_role(mock_user, mock_session, user, user_data):
    new_role = Role.STUDENT.value
    mock_user.query.filter_by.return_value.first.return_value = user
    mock_session.commit.return_value = None

    update_role(new_role, user_data["id"])

    assert user.role == new_role

@patch("teaching_platform.models.users.db_handler.User")
def test_update_role_user_dosent_exist(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = None


    with pytest.raises(exceptions.UserDosentExistError):
        update_role(Role.STUDENT, user_data["id"])

@patch("teaching_platform.models.users.db_handler.User")
def test_update_role_incorrect_role(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = user

    with pytest.raises(exceptions.IncorrectRoleError):
        update_role("not_a_role", user_data["id"])

@patch("teaching_platform.models.users.db_handler.db.session")
@patch("teaching_platform.models.users.db_handler.User")
def test_update_password(mock_user, mock_session, user, user_data):
    new_password = "New_Password123!"
    mock_user.query.filter_by.return_value.first.return_value = user
    mock_session.commit.return_value = None

    update_password(new_password, user_data["id"])

    assert check_password_hash(user.password, new_password)

@patch("teaching_platform.models.users.db_handler.User")
def test_update_password_validation(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = user

    with pytest.raises(exceptions.PasswordToWeakError):
        update_password("bad_pwd", user_data["id"])

@patch("teaching_platform.models.users.db_handler.User")
def test_update_password_user_dosent_exist(mock_user, user, user_data):
    mock_user.query.filter_by.return_value.first.return_value = None

    with pytest.raises(exceptions.UserDosentExistError):
        update_password("New_Password123!", user_data["id"])