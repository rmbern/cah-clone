from flask import Blueprint, request, current_app, redirect, render_template
from cah.db import get_db

bp = Blueprint('login', __name__)

@bp.route('/')
def reroute(): # redirect already owned by Flask
               # aren't naming coliisions exciting!?!?!?!?!?!?!?!?
  return redirect('/login')

@bp.route('/login', methods=['GET'])
def login():
  return render_template('login.html')

@bp.route('/login', methods=['POST'])
def register_player():
  player_name = request.form['username']
  if not player_name:
    # TODO: handle this "error"!
    flash("Username must be specified!!")
  
  # TODO: Handle when playername is already taken!!
  db = get_db()
  db.execute(
    'INSERT INTO players'
    ' VALUES (?,0,0)', (player_name,)
  )
  db.commit()
  
  # TODO: error handling
  res_string = "You have been added to the db!!"
  for i in db.execute('SELECT * FROM players').fetchall():
    # have to be careful with a lot of special chars that
    # flask seems to disallow
    res_string +="|"+ i['name']+"|"
    print(res_string)
  return res_string
