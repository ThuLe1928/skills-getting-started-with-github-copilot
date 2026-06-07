from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

# Add the src directory to the Python path so tests can import the app directly.
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from app import app  # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)
