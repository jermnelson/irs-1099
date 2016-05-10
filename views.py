from __init__ import app
from flask import render_template, request
from forms import MISC1099Form
from record import FIREFile

@app.route("/generate", methods=["POST"])
def generate():
    form = MISC1099Form()
    if request.method.startswith("POST") and form.validate():
        fire_file = FIREFile(form)
        return fire_file.save()
    return "Generate 1099-MISC {} {}".format(form.validate(), form.errors)

@app.route("/")
def index():
    return render_template(
        "index.html", 
        form=MISC1099Form())
