class UserDomainError(Exception):
    pass

class InvalidUserNameError(UserDomainError):
    pass

class InvalidUserMailError(UserDomainError):
    pass

class InvalidUserPasswordError(UserDomainError):
    pass

