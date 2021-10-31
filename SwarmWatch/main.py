"""
Copyright (C) 2021 https://github.com/binaryhabitat.

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from flask import Flask, redirect, render_template

from . import SwarmState

app = Flask(__name__)


@app.route("/")
def hello():
    return redirect("/swarm", code=301)


@app.route("/swarm")
def swarm():
    return render_template("swarm.html")


@app.route("/swarm_data")
def swarm_data() -> dict:
    return s.json


if __name__ == "__main__":
    s = SwarmState()
    app.run(host="0.0.0.0", port=50001)
