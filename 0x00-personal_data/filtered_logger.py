#!/usr/bin/env python3
"""
This module contains a function to obfuscate sensitive fields in log messages.
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
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
