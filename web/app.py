from flask import Flask, render_template, send_from_directory, request
from multiprocessing import Process, Queue

from dqc.main import run_on_network

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


def run_script(q, code):
    import qiskit
    full_code = f"{code}" + \
                 "\n" + \
                 "qc = get_circuit()"

    ctx = {}
    exec(full_code, {"__builtins__": None, "qiskit": qiskit}, ctx)

    q.put(ctx['qc'])


def get_qc(code):
    q = Queue()
    p = Process(target=run_script, args=(q, code,))
    p.start()
    res = q.get()
    p.join()
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
