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
class MentorDosentExistError(ResourceDosentExistError):
    def __init__(self):
        self.message = "User with given id and TEACHER role dosen't exist"
        self.status = 404
        logging.warning(self.message)

class UserDosentExistError(ResourceDosentExistError):
    def __init__(self):
        self.message = "User with this id dosen't exist."
        self.status = 404
        logging.warning(self.message)

class ProjectDosentExistError(ResourceDosentExistError):
    def __init__(self):
        self.message = "Project with this id dosen't exist."
        self.status = 404
        logging.warning(self.message)

class StudentNotInProject(ResourceDosentExistError):
    def __init__(self):
        self.message = "Student with this id isn't a part of this project."
        self.status = 404
        logging.warning(self.message)

#------------------------------------------------------------
class UserAlreadyAddedError(Exception):
    def __init__(self):
        self.message = "User with this id has been already added to this project."
        self.status = 409
        logging.warning(self.message)

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"


class AuthError(Exception):
    def __init__(self):
        self.message = "Authorization failed."
        self.status = 401
        logging.warning(self.message)

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"
