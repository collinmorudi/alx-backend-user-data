#!/usr/bin/env python3
"""0.Regex-ing"""


import re
import logging


def filter_datum(fields, redaction, message, separator):
    """todo"""
    regex = '|'.join([f'({field}=[^;]*)' for field in fields])
    return re.sub(regex, f'{redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = record.getMessage()
        return super().format(record)._style._fmt % self.filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)

    @staticmethod
    def filter_datum(fields, redaction, message, separator):
        regex = '|'.join([f'({field}=[^;]*)' for field in fields])
        return re.sub(regex, f'{redaction}', message)


PII_FIELDS = ("email", "ssn", "password", "date_of_birth", "name")


def get_logger():
    """todo"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
