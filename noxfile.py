import nox


def install_flit_dev_deps(session, with_model=False):
    session.install("flit")
    session.run("flit", "install", "--deps", "develop")
    if with_model:
        session.run("helpner", "download")


@nox.session(reuse_venv=True)
def unit_tests(session):
    session.run("flit", "install", "--deps", "develop")
    session.run("pytest", "tests/unit")


@nox.session(reuse_venv=True)
def integration_tests(session):
    session.run("flit", "install", "--deps", "develop")
    session.run("pytest", "tests/integration")


@nox.session
def coverage(session):
    install_flit_dev_deps(session)
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
def format(session):
    session.run("flit", "install", "--deps", "develop")
    session.run("isort", "cli_help_maker", "examples", "tests")
    session.run("black", "cli_help_maker", "examples", "tests")
