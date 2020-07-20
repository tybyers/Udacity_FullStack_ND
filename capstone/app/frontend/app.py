
@app.route('/')
def index():
  # TODO: Replace this with a render of a more useful index page
  data = get_races().get_json()['race']
  print(data)
  return render_template('pages/index.html', data=data)