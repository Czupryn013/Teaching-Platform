

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

class EmailTakenError(UserCredentialsError):
    def __init__(self):
        self.message = "Email alreday regisered, use a diffrent one."
        self.status = 409
        

class PasswordToWeakError(UserCredentialsError):
    def __init__(self, message="Given password is to weak."):
        self.message = message
        self.status = 406
        

class IncorrectUsername(UserCredentialsError):
    def __init__(self):
        self.message = "Incorrect username."
        self.status = 406
        

class UserDosentExistError(ResourceDosentExistError):
    def __init__(self):
        self.message = "User with this id dosen't exist."
        self.status = 404
        

class AuthError(Exception):
    def __init__(self):
        self.message = "Authorization failed."
        self.status = 401
        

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"


class IncorrectRoleError(Exception):
    def __init__(self):
        self.message = "Incorrect role value passed"
        self.status = 400

    def __str__(self):
        return f"Error: {self.message} Status: {self.status}"









