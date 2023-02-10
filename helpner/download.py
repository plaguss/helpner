"""Facility to install the model from GitHub releases. 
It looks through the releases, finds the last one added,
and extracts the wheel from those assets.
"""

import json
import subprocess
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from packaging.version import parse

RELEASES_URL = r"https://github.com/plaguss/helpner-core/releases"
RELEASES_ENDPOINT = r"https://api.github.com/repos/plaguss/helpner-core/releases"


def _get_wheel(releases: Any) -> str:
    """Parses the response from github api to obtain
    the most updated wheel.
    """
    # Get the last uploaded release
    versions = [parse(r["name"].split("-")[-1]) for r in releases]
    last_release = versions.index(max(versions))
    assets = releases[last_release]["assets"]
    # Find the wheel package instead of the sdist.
    whl = [
        a["browser_download_url"]
        for a in assets
        if a["browser_download_url"].endswith("whl")
    ][0]
    return whl


def download_model() -> None:  # pragma: no cover
    """Downloads the lastest model from `helpner-core` releases.

    Raises:
        HTTPError: Raised if calling urlopen fails.
            If that occurs, a url pointing to the models would appear.
    """
    try:
        with urlopen(RELEASES_ENDPOINT) as response:
            body = response.read()
    except (URLError, HTTPError) as e:
        raise URLError(
            f"Something failed, the model should be installed from: {RELEASES_URL}"
        ) from e
    else:
        releases = json.loads(body)

    whl = _get_wheel(releases)
    # An example browser_download_url path would be:
    # https://github.com/plaguss/helpner-core/releases/download/v0.1.3/en_helpner_core-0.1.3-py3-none-any.whl
    subprocess.run([sys.executable, "-m", "pip", "install", whl], check=True)


if __name__ == "__main__":
    download_model()  # pragma: no cover
