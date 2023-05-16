"""Logging processors for structlog."""

import logging
from typing import Any, Dict

import structlog

gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_error_logger.setLevel(logging.INFO)
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.setLevel(logging.INFO)


def edit_event_name(_, __, event_dict: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Edit the event dict to change the event name, so we don't clobber elastic indices.

    Args:
        _: Unused
        __: Unused
        event_dict: The logging event dictionary

    Returns:
        The modified logging event dictionary
    """
    event = event_dict.pop("event")
    event_dict["event_content"] = event
    return event_dict


STD_LIB_PROCESSORS = [
    # Add these bits of information to the event_dict if the log entry
    # is not from structlog.
    # change the event name to message
    edit_event_name,
    # Add the name of the logger to event dict.
    structlog.stdlib.add_logger_name,
    # Add log level to event dict.
    structlog.stdlib.add_log_level,
    # Add a timestamp in ISO 8601 format.
    structlog.processors.TimeStamper(fmt="iso"),
]


STRUCTLOG_PROCESSORS = [
    # If log level is too low, abort pipeline and throw away log entry.
    structlog.stdlib.filter_by_level,
    # change the event name to message
    edit_event_name,
    # Add the name of the logger to event dict.
    structlog.stdlib.add_logger_name,
    # Add log level to event dict.
    structlog.stdlib.add_log_level,
    # Perform %-style formatting.
    structlog.stdlib.PositionalArgumentsFormatter(),
    # Add a timestamp in ISO 8601 format.
    structlog.processors.TimeStamper(fmt="iso"),
    # If the "stack_info" key in the event dict is true, remove it and
    # render the current stack trace in the "stack" key.
    structlog.processors.StackInfoRenderer(),
    # Sets "exc_info" key if the method name is "exception" and exc_info not set
    structlog.dev.set_exc_info,
    # If the "exc_info" key in the event dict is either true or a
    # sys.exc_info() tuple, remove "exc_info" and render the exception
    # with traceback into the "exception" key.
    structlog.processors.format_exc_info,
    # If some value is in bytes, decode it to a unicode str.
    structlog.processors.UnicodeDecoder(),
    # Wrap logger, name, and event_dict.
    # The result is later unpacked by ProcessorFormatter when formatting log entries.
    structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
]
