from password_strength import PasswordPolicy
from werkzeug.security import generate_password_hash

from teaching_platform.users import exceptions


def validate_password(password):
    policy = PasswordPolicy.from_names(length=5, uppercase=1, numbers=2, special=1, nonletters=2)
    test = policy.test(password)

    if test: raise exceptions.PasswordToWeakError(f"Password breaks the following rules {test}.")

    return generate_password_hash(password, method="sha256")

def validate_username(username):
    if not username or " " in username or len(username) > 20: raise exceptions.IncorrectUsername()
    else: return username