"""Initialization module for the application"""

import sys

from .functionalities import dbf_controller


def run():
    # Expect receive -r or --reset flag
    if len(sys.argv) > 1:
        if sys.argv[1] == "-r" or sys.argv[1] == "--reset":
            print("Resetting databases...")
            dbf_controller.reset()

    user = {"id": 1, "name": "j4breu", "password": "qwerty"}
    user = dbf_controller.details(user)
    print(user)

    # user = file_controller.de()
    # print(user)

    print("Done!")
