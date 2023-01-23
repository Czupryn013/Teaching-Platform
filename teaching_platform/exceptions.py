import logging


class UserCredentialsError(Exception):
    def __init__(self):
        self.message = "User credentials error."
        self.status = 401

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"

class ResourceDosentExistError(Exception):
    def __init__(self):
        self.message = "This resource dosen't exist"
        self.status = 404

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"

#------------------------------------------------------------
class UsernameTakenError(UserCredentialsError):
    def __init__(self):
        self.message = "Username alreday taken, pick a diffrent one."
        self.status = 409
        logging.warning(self.message)

class PasswordToWeakError(UserCredentialsError):
    def __init__(self, message="Given password is to weak."):
        self.message = message
        self.status = 406
        logging.warning(message)

class IncorrectUsername(UserCredentialsError):
    def __init__(self):
        self.message = "Incorrect username."
        self.status = 406
        logging.warning(self.message)

#------------------------------------------------------------
class TeacherDosentExistError(ResourceDosentExistError):
    def __init__(self):
        self.message = "User with given id and TEACHER role dosen't exist"
        self.status = 404
        logging.warning(self.message)

class UserDosentExistError(ResourceDosentExistError):
    def __init__(self):
        self.message = "User with this id dosen't exist."
        self.status = 404
        logging.warning("User with this id dosen't exist.")

class LessonDosentExistError(ResourceDosentExistError):
    def __init__(self):
        self.message = "Lesson with this id dosen't exist."
        self.status = 404
        logging.warning("Lesson with this id dosen't exist.")

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"
#------------------------------------------------------------

class UserAlreadyAddedError(Exception):
    def __init__(self):
        self.message = "User with this id has been already added to this lesson."
        self.status = 409
        logging.warning("User with this id has been already added to this lesson.")

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"

class AuthError(Exception):
    def __init__(self):
        self.message = "Authorization failed."
        self.status = 401
        logging.warning(self.message)

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"









