import startup
from startup import client

def test_good_login(client):
  # Input: Valid login request
  # Output: Lobby page with new player
  res = client.post('/login',
                    data = {"username":"not a real person"},
                    follow_redirects = True)
  
  # Check that the given username was correctly rendered
  # and sent to the client.
  # Not particularly thorough, but good enough.
  assert b'not a real person' in res.data

  # TODO: Directly check database?
    
def test_blank_login(client):
  # Input: Request with empty string for login.
  #        (Cannot be done through frontend web pages,
  #         could potentially be stimulated via curl, etc.

  # Output: Login request with error message.
  res = client.post('/login',
                    data = {"username":""},
                    follow_redirects = True)

  assert b'try again using' in res.data
  
def test_invalid_login(client):
  # Input: Request with invalid chars for login.

  # Output: Login request with error message.
  res = client.post('/login',
                    data = {"username":"aeflkja*&fe56"},
                    follow_redirects = True)

  assert b'try again using' in res.data

def test_duplicate_login(client):
  with startup.get_app().test_request_context():
    res = client.post('/login',
                      data = {"username":"duplicate"},
                      follow_redirects = True)
  
  with startup.get_app().test_request_context():
    res = client.post('/login',
                      data = {"username":"duplicate"},
                      follow_redirects = True)

  assert b'already in use' in res.data

