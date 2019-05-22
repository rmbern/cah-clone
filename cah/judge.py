from flask import Blueprint, request, session, current_app, redirect
from cah.db import get_db
from . import answer

bp = Blueprint('judge', __name__)

@bp.route('/select-winner', methods=['POST'])
def select_winner():
  # Look up score of player(s) submitting winning answer,
  # and increment it.

  # In what should be a rare case of two players submitting
  # the same answer, and one of those answers being chosen,
  # we will increment the score of both players.
  db = get_db()
  
  # The judge should have a blank answer whereas all players
  # should have populated answers at this point, but we
  # explicity make sure we are not updating a judge's score
  # for defensive purposes.
  current_app.logger.info("Request form:" + str(request.form.__dict__))
  db.execute(
    'UPDATE players'
    ' SET score = score + 1'
    ' WHERE answer = ?' 
    ' AND judge = 0', (request.form['answer-button'],))

  # After setting the players' scores, set the judge's answer
  # to whatever they selected from the other players. Now we
  # know in other functions what the judge answered.
  change_diff = db.total_changes
  db.execute(
    'UPDATE players'
    ' SET answer = ?'
    ' WHERE judge = 1'
    ' AND name = ?', (request.form['answer-button'], session['username']))
  # TODO: My gut said to check that an update actually occured
  #       for this one sql statement, but maybe it belongs to
  #       most of them? I can't think of a situation in this
  #       enviornment where an execute shouldn't make a change.
  change_diff = db.total_changes - change_diff

  if change_diff == 0:
    current_app.logger.warning("Judge's answer was not updated!")

  db.commit()

  return redirect('/scoreboard')

@bp.route('/judge-answered', methods=['GET'])
def judge_answered():
  db = get_db()
  
  record = db.execute(
               'SELECT answer FROM players'
               ' WHERE judge = 1').fetchone()

  if record['answer'] == None:
    return "JUDGE DID NOT ANSWER"
  else: 
    return "JUDGE ANSWERED"
