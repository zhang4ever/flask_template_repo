import sys
import os

_root_project = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(_root_project))

from main import create_app

app = create_app()
