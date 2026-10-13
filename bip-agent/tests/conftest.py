import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bip_agent.catalog import Catalog  # noqa: E402


@pytest.fixture(scope="session")
def catalog():
    return Catalog.load()


@pytest.fixture(scope="session")
def example_specs():
    import json

    return {p.stem: json.loads(p.read_text()) for p in sorted((ROOT / "examples" / "specs").glob("*.json"))}
