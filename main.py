import os
from flask import Flask, render_template, request, redirect, url_for, session
from utils import load_script, get_character_lines, get_script_characters, get_character_traits, get_character_back_story, get_script_summary

# session.clear()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))


@app.route('/')
def index():
  return render_template('home.html')


@app.route('/process_form', methods=['POST'])
def process_form():
  option = request.form['option']
  file = request.files['file']
  path = r'static/files/' + file.filename
  file.save(path)
  script = load_script(path)

  print(f"GET SCRIPT CHARACTERS")
  characters = get_script_characters(script)

  print(f"GET CHARACTER LINES")
  character_lines = get_character_lines(script, characters)

  print(f"GET CHARACTER TRAITS")
  traits = get_character_traits(character_lines, characters)
  print(type(traits))
  
  print(f"GET CHARACTER BACKSTORY")
  backstory = get_character_back_story(character_lines, characters)
  print(type(backstory))
  
  print(f"GET SCRIPT SUMMARY")
  script_sum = get_script_summary(script)
  print(type(script_sum))

  session['traits'] = traits
  print(type(session["traits"]))
  session['backstory'] = backstory
  print(type(backstory))
  session['script_sum'] = script_sum

  if option == '1':

    return redirect(url_for('summary'))

  elif option == '2':

    return redirect(url_for('traits'))

  elif option == '3':

    return redirect(url_for('backstory'))


@app.route('/traits')
def traits():
  data = session.get("traits")
  #print(type(data))
  return render_template('character.html', character_stories=data)


@app.route('/backstory')
def backstory():
  data = session.get("backstory")
  #print(type(data))
  return render_template('character.html', character_stories=data)


@app.route('/summary')
def summary():
  data = session.get("script_sum")
  #print(type(data))
  return render_template('summary.html', summary=data)


app.run(host='0.0.0.0', port=81)
