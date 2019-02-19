from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/about")
def about():
  return render_template("about.html")


@app.route("/search/vsm", methods=["GET"])
def search_vsm():
  if request.method != "GET":
    return f"Invalid method: {request.method}"
  
  query = request.args.get('q', type = str) or request.form.get('q')
  if not query:
    df = pd.DataFrame(columns=["title", "body", "confidence"])
    (_, title), (_, body), (_, confidence) = df.to_dict().items()
    results = dict(zip(title.values(), body.items()))
    return render_template("results.html", query="", correction=None, results=results, error_msg="Empty query.")
  
  correction = vsm_model.check_spelling(query)
  
  df = vsm_model.query(query)
  if df is None:
    df = pd.DataFrame(columns=["title", "body", "confidence"])

  (_, title), (_, body), (_, confidence) = df.to_dict().items()

  results = dict(zip(title.values(), body.items()))
  return render_template("results.html", query=query, correction=correction, results=results)
  

@app.route("/search/brm")
def search_brm():
  query = request.args.get('q', type = str)
  correction = None
  err_msg = None
  
  try:
    correction = brm_model.check_spelling(query)
    (_, title), (_, body) = brm_model.query(query).to_dict().items()
  except:
    df = pd.DataFrame(columns=["title", "body"])
    (_, title), (_, body) = df.to_dict().items()
    print("err")
    err_msg = "Unable to parse boolean query. Please try again."

  results = dict(zip(title.values(), body.items()))
  return render_template("results.html", query=query, correction=correction, results=results, error_msg=err_msg)
 
if __name__ == "__main__":
  app.run(port=4999, debug=True)
