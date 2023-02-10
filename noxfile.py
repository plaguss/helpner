import nox


def install_flit_dev_deps(session, with_model=False):
    session.install("flit")
    session.run("flit", "install", "--deps", "develop")
    if with_model:
        session.run("helpner", "download")


@nox.session
def tests(session):
    install_flit_dev_deps(session, with_model=True)
    session.run("pytest", "tests")


@nox.session
def coverage(session):
    install_flit_dev_deps(session, with_model=True)
    session.run(
        "python",
        "-m",
        "pytest",
        "-s",
        "tests",
        "--cov=helpner",
        "--cov-report=term-missing",
        "--cov-config=pyproject.toml",
    )


@nox.session
def lint(session):
    session.install("black", "ruff")
    session.run("ruff", "helpner")
    session.run("black", "--check", "helpner")


@nox.session
def typecheck(session):
    session.install("mypy")
    install_flit_dev_deps(session)
    session.run("mypy", "-p", "helpner", "--no-incremental")


@nox.session
def format(session):
    session.install("black", "ruff")
    session.run("ruff", "helpner", "--fix")
    session.run("black", "helpner")
