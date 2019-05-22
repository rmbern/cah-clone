import cah

import os
import tempfile

import pytest

app = cah.create_app()
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
