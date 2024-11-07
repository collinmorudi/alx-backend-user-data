#!/usr/bin/env python3
"""
This module contains functions and classes to obfuscate sensitive
fields in log messages.
"""


import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates sensitive information in a log message by replacing specified
    field values with a redaction string.

    Args:
        fields (List[str]): List of fields to obfuscate.
        redaction (str): The string used to replace sensitive field values.
        message (str): The log line containing the data.
        separator (str): The character separating fields in the log line.

    Returns:
        str: The log message with sensitive fields obfuscated.
    """
    pattern = f"({'|'.join(fields)})=([^ {separator}]+)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class to filter sensitive information
    in log records. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the formatter with specific fields to redact.

        Args:
            fields (List[str]): List of fields to be redacted in the
            log message.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record, applying redaction to specified fields.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted and redacted log message.
        """
        record.msg = (
          filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        )
        return super().format(record)
