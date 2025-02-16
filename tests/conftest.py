import sys
import os
import pytest

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../app"))

if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)
