from flask import Flask
from data_loading.load_data import load_latest_temperature

app = Flask(__name__)


@app.route('/')
def hello_world():
    time, cpu_temperature = load_latest_temperature()
    return """Hello World!
              <br><br>
              Latest CPU temperature logged: <strong>{}°C</strong> <br>
              Logged on <strong>{:%Y-%m-%d}</strong>, at <strong>{:%H:%M}</strong>""".format(cpu_temperature, time, time)


if __name__ == '__main__':
    app.run('0.0.0.0')
