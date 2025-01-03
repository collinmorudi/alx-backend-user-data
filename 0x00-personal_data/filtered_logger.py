#!/usr/bin/env python3
"""
This module contains functions and classes to handle logging with sensitive
field redaction, as well as database connection setup.
"""


import logging
import re
import os
from typing import List, Tuple
import mysql.connector


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for user data with sensitive information
    redaction.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to a MySQL database using credentials from
    environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main():
    """
    Main function that retrieves and logs user data from the database, with
    sensitive information redacted.
    """
    db = get_db()
    cursor = db.cursor()

    # Retrieve all rows in the users table
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    # Get column names to properly format each row
    columns = [column[0] for column in cursor.description]

    logger = get_logger()

    # Format each row as a message with redacted fields
    for row in rows:
        row_data = "; ".join(f"{col}={val}" for col, val in zip(columns, row))
        logger.info(row_data)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
