"""Facility to install the model from GitHub releases. 
It looks through the releases, finds the last one added,
and extracts the wheel from those assets.

TODO:
    - Check for errors on connection, if its not found, and print
        the url where the assets can be installed from.
    - Expose as a subcommand from helpner for
"""

import json
import subprocess
import sys
from urllib.request import urlopen

from packaging.version import parse

url = r"https://github.com/plaguss/helpner-core/releases/download/v0.1.3/en_helpner_core-0.1.3-py3-none-any.whl"

endpoint = r"https://api.github.com/repos/plaguss/helpner-core/releases"


with urlopen(endpoint) as response:
    body = response.read()
    releases = json.loads(body)

# Get the last uploaded release
versions = [parse(r["name"].split("-")[-1]) for r in releases]
last_release = versions.index(max(versions))
assets = releases[last_release]["assets"]
# Find the wheel package
whl = [
    a["browser_download_url"]
    for a in assets
    if a["browser_download_url"].endswith("whl")
][0]
subprocess.run([sys.executable, "-m", "pip", "install", whl], check=True)
