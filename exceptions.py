ERROR_MESSAGE_USER_NOT_FOUND = 'User does not exist!'
ERROR_MESSAGE_WRONG_PASSWORD = 'Incorrect password!'
ERROR_MESSAGE_USER_ALREADY_EXISTS = 'User already exists!'
ERROR_MESSAGE_PASSWORD_CONFIRMATION_FAIL = 'Passwords do not match!'
ERROR_MESSAGE_COMMENT_CONTENT_EMPTY = 'Comment empty!'
ERROR_MESSAGE_TOPIC_NAME_EMPTY = 'Topic name not defined!'

class UserNotFoundError(Exception):
    def __init__(self):
       self.message = ERROR_MESSAGE_USER_NOT_FOUND


class WrongPasswordError(Exception):
    def __init__(self):
       self.message = ERROR_MESSAGE_WRONG_PASSWORD


class UserAlreadyExistsError(Exception):
    def __init__(self):
       self.message = ERROR_MESSAGE_USER_ALREADY_EXISTS


class PasswordConfirmationError(Exception):
    def __init__(self):
       self.message = ERROR_MESSAGE_PASSWORD_CONFIRMATION_FAIL


class EmptyCommentContentError(Exception):
    def __init__(self):
       self.message = ERROR_MESSAGE_COMMENT_CONTENT_EMPTY


class EmptyTopicNameError(Exception):
    def __init__(self):
       self.message = ERROR_MESSAGE_TOPIC_NAME_EMPTY
