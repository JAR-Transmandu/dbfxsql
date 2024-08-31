"""Initialization module for the application"""

import click


@click.group()
def run():
    # Expect receive -r or --reset flag

    print("Done!")
