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


def die(message):
    alert(message)
    sys.exit(1)


def run(ctx, cmd, **kwargs):
    result = ctx.run(cmd, warn=True, **kwargs)
    if result.failed:
        die(f"Command failed: {cmd}")


@task(name="test:client")
def test_client(ctx):
    """Run client tests"""
    notify("Running client tests")
    with ctx.cd("client"):
        run(ctx, "CI=true npm test", pty=True)


@task(name="test:client:coverage")
def test_client_coverage(ctx):
    """Run client tests"""
    notify("Running client tests with coverage")
    with ctx.cd("client"):
        run(ctx, "CI=true npm test -- --coverage", pty=True)


@task(name="test:server")
def test_server(ctx):
    """Run server tests"""
    notify("Running server tests")
    with ctx.cd("server"):
        run(ctx, "pytest --exitfirst", pty=True)


@task(name="test:server:coverage")
def test_server_coverage(ctx):
    """Create server test coverage report"""
    notify("Running server tests with coverage and generating report")
    with ctx.cd("server"):
        run(
            ctx, "pytest --cov-branch --cov=veto --exitfirst --no-cov-on-fail", pty=True
        )
        run(ctx, "coverage html --directory coverage", pty=True)


@task(test_client, test_server, name="test:all")
def test_all(ctx):
    """Run all tests (client and server)"""
    notify("All tests run")


@task(test_all)
def release(ctx):
    """Build and release the app to production"""
    root_directory = str(Path(__file__).resolve().parent.parent.parent)
    repo = Repo(root_directory)

    if repo.is_dirty():
        die("Git repo is dirty")

    notify("Building client")
    with ctx.cd("client"):
        run(ctx, "npm run build")

    if repo.is_dirty():
        notify("Adding new client build assets to Git repo")
        run(ctx, "git add client/build")
        run(ctx, "git commit -m 'Add new client build assets'")
    else:
        notify("No change detected in client build assets")

    notify("Pushing Git repo to origin remote")
    run(ctx, "git push origin main")

    notify("Pushing Git repo to heroku remote")
    run(ctx, "git push heroku main")
