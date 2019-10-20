import asyncio

from flask import Flask, render_template, send_from_directory, request
from multiprocessing import Process

from web.dqc.main import run_on_network

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('templates/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('templates/css', path)


@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('templates/fonts', path)


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('templates/images', path)


@app.route('/inc/<path:path>')
def send_inc(path):
    return send_from_directory('templates/inc', path)


@app.route('/vendor/<path:path>')
def send_vendor(path):
    return send_from_directory('templates/vendor', path)


@app.route('/mirror/<path:path>')
def send_codemirror(path):
    return send_from_directory('templates/mirror', path)


def get_qc(code):
    with open("tmp.py", "w") as f:
        f.write(code)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    from tmp import get_circuit

    # res = exec(code + "\nget_circuit()")

    res = get_circuit()
    return res


@app.route('/api/run', methods=['POST'])
def run_code():
    code = request.json["code"]

    qc = get_qc(code)
    res = run_on_network(qc, ["Alice", "Bob"])
    print(res)

    return {
        "status": "ok",
        "results": res
    }


if __name__ == '__main__':
    app.run()
