#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import os
import sys
from enum import Enum

""" <config> """
# SERVICE INFO
PORT = 8084

# DEBUG -- logs to stderr, TRACE -- verbose log
DEBUG = os.getenv("DEBUG", False)
TRACE = os.getenv("TRACE", False)
""" </config> """


def check(host):
    die(ExitStatus.CHECKER_ERROR, "Not implemented")


def put(host, flag_id, flag, vuln):
    die(ExitStatus.CHECKER_ERROR, "Not implemented")


def get(host, flag_id, flag, vuln):
    die(ExitStatus.CHECKER_ERROR, "Not implemented")


""" <common> """


class ExitStatus(Enum):
    OK = 101
    CORRUPT = 102
    MUMBLE = 103
    DOWN = 104
    CHECKER_ERROR = 110


def _log(obj):
    if DEBUG and obj:
        caller = inspect.stack()[1].function
        print(f"[{caller}] {obj}", file=sys.stderr, flush=True)
    return obj


def die(code: ExitStatus, msg: str):
    if msg:
        print(msg, file=sys.stderr, flush=True)
    exit(code.value)


def _main():
    action, *args = sys.argv[1:]

    try:
        if action == "check":
            host, = args
            check(host)
        elif action == "put":
            host, flag_id, flag, vuln = args
            put(host, flag_id, flag, vuln)
        elif action == "get":
            host, flag_id, flag, vuln = args
            get(host, flag_id, flag, vuln)
        else:
            raise IndexError
    except ValueError:
        die(
            ExitStatus.CHECKER_ERROR,
            f"Usage: {sys.argv[0]} check|put|get IP FLAGID FLAG",
        )
    except Exception as e:
        die(
            ExitStatus.CHECKER_ERROR,
            f"Exception: {e}. Stack:\n {inspect.stack()}",
        )


""" </common> """

if __name__ == "__main__":
    _main()
