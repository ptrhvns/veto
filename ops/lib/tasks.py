import contextlib
import os
import sys
from pathlib import Path

from git import Repo
from invoke import task
from rich.console import Console
from rich.theme import Theme

theme = Theme({"notify": "cyan", "warn": "yellow", "alert": "bold red"})

console = Console(theme=theme, highlight=False)
econsole = Console(file=sys.stderr, highlight=False, theme=theme)


def notify(message):
    console.print(f"### {message}", style="notify")


def warn(message):
    econsole.print(f"### WARNING: {message}", style="warn")


def alert(message):
    econsole.print(f"### ERROR: {message}", style="alert")


@contextlib.contextmanager
def cd(directory):
    """Temporarily change directory."""
    savedir = os.getcwd()
    os.chdir(os.path.expanduser(directory))
    try:
        yield
    finally:
        os.chdir(savedir)


@task
def release(c):
    """Build and deploy the app to production on Heroku."""
    with cd("client"):
        notify("Building client")
        c.run("npm run build")

    root_directory = str(Path(__file__).resolve().parent.parent.parent)
    repo = Repo(root_directory)

    if repo.is_dirty():
        notify("Adding new client build assets to Git repo")
        c.run("git add client/build")
        result = c.run("git commit -m 'Add new client build assets'")
        if result.failed:
            alert("Git commit of new client build assets returned error")
            sys.exit(1)
    else:
        notify("No change detected in client build assets")

    notify("Pushing Git repo to Heroku")
    c.run("git push heroku main")
