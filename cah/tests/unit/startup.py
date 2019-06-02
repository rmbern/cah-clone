import cah

import os
import tempfile

import pytest

app = cah.create_app()

def run_db_script(filename):
  with app.open_resource("tests/unit/"+filename) as f:
    with app.app_context():
      cah.db.get_db().executescript(f.read().decode('utf-8'))

@pytest.fixture
def client():
  fd, app.config['DATABASE'] = tempfile.mkstemp()
  app.config['TESTING'] = True
  client = app.test_client()

  with app.app_context():
    cah.db.init_db()

  yield client

  os.close(fd)
  os.unlink(app.config['DATABASE'])

def get_app(): return app
