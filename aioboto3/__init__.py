# -*- coding: utf-8 -*-

"""Top-level package for Async AWS SDK for Python."""
import logging
from aioboto3.session import Session
from boto3.compat import _warn_deprecated_python
import threading

__author__ = """Terry Cain"""
__email__ = "terry@terrys-home.co.uk"
__version__ = "8.3.0"

DEFAULT_SESSIONS = {}


def setup_default_session(**kwargs):
    """
    Set up a default session, passing through any parameters to the session
    constructor. There is no need to call this unless you wish to pass custom
    parameters, because a default session will be created for you.
    """
    global DEFAULT_SESSIONS
    DEFAULT_SESSIONS[threading.get_ident()] = Session(**kwargs)


def set_stream_logger(name="boto3", level=logging.DEBUG, format_string=None):
    """
    Add a stream handler for the given name and level to the logging module.
    By default, this logs all boto3 messages to ``stdout``.

    :type name: string
    :param name: Log name
    :type level: int
    :param level: Logging level, e.g. ``logging.INFO``
    :type format_string: str
    :param format_string: Log message format
    """
    if format_string is None:
        format_string = "%(asctime)s %(name)s [%(levelname)s] %(message)s"

    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def _get_default_session(**kwargs):
    """
    Get the default session, creating one if needed.
    :rtype: :py:class:`~aioboto3.session.Session`
    :return: The default session
    """
    thread_id = threading.get_ident()
    if DEFAULT_SESSIONS.get(thread_id, None) is None:
        setup_default_session(**kwargs)
    _warn_deprecated_python()

    return DEFAULT_SESSIONS[thread_id]


def client(*args, **kwargs):
    """
    Create a low-level service client by name using the default session.
    See :py:meth:`aioboto3.session.Session.client`.
    """
    return _get_default_session().client(*args, **kwargs)


def resource(*args, **kwargs):
    """
    Create a resource service client by name using the default session.
    See :py:meth:`aioboto3.session.Session.resource`.
    """
    return _get_default_session().resource(*args, **kwargs)


# Set up logging to ``/dev/null`` like a library is supposed to.
# http://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
class NullHandler(logging.Handler):
    def emit(self, record):
        pass


logging.getLogger("boto3").addHandler(NullHandler())
