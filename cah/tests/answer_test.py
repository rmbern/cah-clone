import cah
import startup
from startup import client, run_db_script

def test_get_answers(client):
  # TODO: Should /get-answers really be dependent on a session?
  run_db_script("test_get_answers.sql")

  with client.session_transaction() as test_session:
    test_session['username'] = "player 1"

  res = client.get('/get-answers')
  
  # TODO: Right now, get-answers doesn't give the answer
  #       for the player within the current session.
  #       This would go away with the removal of session
  #       dependence.
  # assert b'PLAYER 1 ANSWER' in res.data
  assert b'PLAYER 2 ANSWER' in res.data

def test_all_answered(client):
  run_db_script("test_all_answered.sql")

  with client.session_transaction() as test_session:
    test_session['username'] = "player 1"
  res = client.get('/all-answered')

  assert b'ALL ANSWERED' in res.data

  with startup.get_app().app_context():
    cah.db.get_db().execute(
      "UPDATE players"
      " SET answer = NULL"
    " WHERE name = 'player 3'"
    )
    cah.db.get_db().commit()

  res = client.get('/all-answered')

  assert b'NOT ALL ANSWERED' in res.data

# Going to break this one unit test into two functions
# So we can get a teardown before testing it with everyone
# answering.
def test_submit_answer_not_all_answered(client):
  # Borrowing from the first test. It sets up
  # three players, one of which hasn't answered.
  # This is exactly what we need for this test too.
  run_db_script("test_get_answers.sql")
  with client.session_transaction() as test_session:
    test_session['username'] = "player 2"
  
  res = client.post('/submit-answer',
                    data = {"answer":"THIS IS A TEST"},
                    follow_redirects = True) 
  
  with startup.get_app().app_context():
    recs = cah.db.get_db().execute(
      "SELECT name, answer FROM players"
    ).fetchall()
  
  # Check in both the db and the response data
  # since we don't render from db information
  [ player_2_answer ] = [ x['answer'] for x in recs \
                          if x['name'] == "player 2"]

  assert "A TEST" in player_2_answer
  assert b"A TEST" in res.data

  # Check that we didn't modify db in an incorrect manner
  [ player_3_rec ] = [ x['answer'] for x in recs  \
                       if x['name'] == "player 3" ]

  assert None == player_3_rec

# TODO: This is INSANELY complicated for a unit test.
#       Refactor!!!
def test_submit_answer_all_answered(client):
  # Borrowing from the second test. It sets up
  # three players, all of which have answered.
  # This is exactly what we need for this test too.
  run_db_script("test_all_answered.sql")
  
  # Get all information before our post switches to
  # a new round, which involves a lot of changes to
  # the database.
  initial_judge = ""
  initial_question = ""
  inital_player_recs = []
  with startup.get_app().app_context():

    initial_judge = cah.db.get_db().execute(
      'SELECT name FROM players'
      ' WHERE judge = 1'
    ).fetchone()['name']

    initial_question = cah.db.get_db().execute(
      'SELECT question FROM current_question'
    ).fetchone()['question']

    # Check that all answers have been cleared
    initial_player_recs = cah.db.get_db().execute(
      "SELECT name, answer FROM players"
    ).fetchall()


    with client.session_transaction() as test_session:
      test_session['username'] = "player 2"
    
    res = client.post('/submit-answer',
                      data = {"answer":"THIS IS A TEST"},
                      follow_redirects = True)

    new_player_recs = cah.db.get_db().execute(
        "SELECT name, answer FROM players"
      ).fetchall()

  [ player_2_answer ] = [ x['answer'] for x in new_player_recs \
                          if x['name'] == "player 2"]

  # Check in both the db and the response data
  # since we don't render from db information
  assert "A TEST" in player_2_answer
  assert b"A TEST" in res.data

  # Next, check that we correctly modified db
  with startup.get_app().app_context():

    # Check that the question has changed.
    new_question = cah.db.get_db().execute(
      "SELECT question FROM current_question"
    ).fetchone()['question']

    assert new_question != initial_question
  
    # Check that the judge has changed.
    new_judge = cah.db.get_db().execute(
      "SELECT name FROM players"
      " WHERE judge = 1"
    ).fetchone()['name']

    assert new_judge != initial_judge

# TODO: PUT CHECK FOR DB CLEAR WHERE IT BELONGS
#    # Check that all answers have been cleared
#    player_recs = cah.db.get_db().execute(
#      "SELECT name, answer FROM players"
#    ).fetchall()
#    
#    # Since initial sql script has three players,
#    # We want to check that we have thre player
#    # records with None for an answer.
#    assert len([ x for x in player_recs if x['answer'] == None]) == 3
