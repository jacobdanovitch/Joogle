from flask import Flask, render_template, request, redirect, url_for
import os


from vsm import VSM
from brm import BRM


app = Flask(__name__, static_folder=os.path.abspath('templates/static'))

vsm_model = VSM()
brm_model = BRM()
 
@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/<string:query>&<string:model>", methods=["POST"])
def api(query, model):
  m = brm_model if model == "brm" else vsm_model
  return m.query(query)


@app.route("/search/vsm", methods=["GET"])
def search_vsm():
  if request.method != "GET":
    return f"Invalid method: {request.method}"
  
  query = request.args.get('q', type = str) or request.form.get('q')
  if not query:
    print(f"Empty query. Request data: {list(request.args.items())}")
    return redirect(url_for("index"))
  
  correction = vsm_model.check_spelling(query)
  
  (_, title), (_, body), (_, confidence) = vsm_model.query(query).to_dict().items()
  results = dict(zip(title.values(), body.items()))

  return render_template("results.html", query=query, correction=correction, results=results)
  

@app.route("/search/brm")
def search_brm():
  query = request.args.get('q', type = str)
  
  try:
    (_, title), (_, body) = brm_model.query(query).to_dict().items() # why is there confidence here??
  except:
    return "Unable to parse boolean expression."
  
  correction = brm_model.check_spelling(query)
  results = dict(zip(title.values(), body.items()))

  return render_template("results.html", query=query, correction=correction, results=results)
 
if __name__ == "__main__":
  app.run(debug=True)