#!/usr/bin/env python3
"""0.Regex-ing"""


import re


def filter_datum(fields, redaction, message, separator):
    """todo"""
    regex = '|'.join([f'({field}=[^;]*)' for field in fields])
    return re.sub(regex, f'{redaction}', message)
