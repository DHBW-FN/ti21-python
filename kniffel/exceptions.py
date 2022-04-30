"""
Custom Exception classes for the kniffel game.
"""


class InvalidInputError(Exception):
    """
    Exception for invalid input
    """


class InvalidArgumentError(Exception):
    """
    Exception for invalid arguments
    """


class InvalidIndexError(Exception):
    """
    Exception for invalid index
    """


class InvalidCommandError(Exception):
    """
    Exception for invalid command
    """


class CategoryAlreadyFilledError(Exception):
    """
    Exception for already filled category
    """
