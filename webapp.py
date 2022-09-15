from flask import Flask, render_template
from turbo_flask import Turbo
import datetime
import threading
import resource_manager
import time

app = Flask(__name__)
# Bootstrap4(app)
turbo = Turbo(app)

hw_res = resource_manager.HwResources()


def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S"), now.strftime("%Y")


@app.route("/")
def index():
    return render_template("index_test.html")


@app.context_processor
def inject_load():
    hw_res.update()
    return {"time": get_current_time()[0],
            "year": get_current_time()[1],
            "cpu_act": hw_res.figures["cpu_act"],
            "cpu_history": hw_res.figures["cpu_history"],
            "ram_act": hw_res.figures["ram_act"],
            "ram_history": hw_res.figures["ram_history"],
            "hdd_usage": hw_res.figures["hdd_usage"],
            "hdd_history": hw_res.figures["hdd_history"],
            "net_history": hw_res.figures["net_history"]
            }


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


def update_load():
    with app.app_context():
        while True:
            time.sleep(4)
            turbo.push(turbo.replace(render_template("wallboard.html"), "wb"))


if __name__ == "__main__":
    app.run(debug=True)
