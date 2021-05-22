from flask import Flask, render_template, redirect
from . import SwarmState

app = Flask(__name__)


@app.route('/')
def hello():
    return redirect("/swarm", code=301)


@app.route('/swarm')
def swarm():
    return render_template('swarm.html')


@app.route('/swarm_data')
def swarm_data() -> dict:
    return s.json


if __name__ == "__main__":
    s = SwarmState()
    app.run(host="0.0.0.0", port=50001)
