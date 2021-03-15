#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import uuid
import requests
import os
import sys
from enum import Enum

""" <config> """
# SERVICE INFO
PORT = 8080

# DEBUG -- logs to stderr, TRACE -- verbose log
DEBUG = os.getenv("DEBUG", True)
TRACE = os.getenv("TRACE", False)
""" </config> """


def check(host):
    try:
        r = requests.get(f'http://{host}:8080/')
    except:
        die(ExitStatus.DOWN,"DOWN")
    #print("************ r = ", r)
    t = r.status_code
    _log(t)
    if t == 200:
        die(ExitStatus.OK, "OK")
    else:
        die(ExitStatus.MUMBLE, "MUMBLE")


def put(host, flag_id, flag, vuln):
    login = uuid.uuid4()
    password = "12345"
    s = requests.Session()
    r = s.post(f'http://{host}:8080/signup', {
     'username': login,
     'password': password,
})
    _log(r.text)
    r = s.post(f'http://{host}:8080/auth', {
     'username': login,
     'password': password,
})
    _log(r.text)
    r = s.post(f'http://{host}:8080/addRecipe', {
    'recipe': flag,
    })
    _log(r.text)
    if flag not in r.text:
        die(ExitStatus.MUMBLE, "MUMBLE: Не нашел флаг после сохранения")
    print(f'{login}:{password}')
    die(ExitStatus.OK, "OK")


def get(host, flag_id, flag, vuln):
    s = requests.Session()
    username, password = flag_id.split(":")
    r = s.post(f'http://{host}:8080/auth', {
     'username': username,
     'password': password,
})
    _log(r.text)
    r = s.get(f'http://{host}:8080/recipes')
    _log(r.text)
    if flag not in r.text:
        die(ExitStatus.CORRUPT, "CORRUPT: Нет флага в рецептах")
    else:
        die(ExitStatus.OK, "OK")

#""" <common> """


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
