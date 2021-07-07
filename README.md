# Quantum Futures Hackathon 2019

We implemented a web interface from which you could submit 
a qiskit circuit and the system would divide the circuit between
simulated devices connected through a simulated quantum network and 
it would run the circuit and print back the results.

In the web interface user can type any python code for generating the circuit.

This is a demonstration of a distributed quantum computer operating on a quantum network.

This project was implemented during the [Quantum Futures Hackathon at CERN](https://indico.cern.ch/event/838035/).

# Running the app

Interface is implemented as a Flask web application.

To run the application you can create a virtual environment, install requirements 
and then run the following:

```
export FLASK_APP=app.py
python -m flask run
```

Please note that this is meant for only demonstration purposes and it should not
be exposed to public internet.


## Simulaqron

We used SimulaQron to simulate the quantum network.

You can see SimulaQron documentation here: https://softwarequtech.github.io/SimulaQron/html/GettingStarted.html

Also you can clone these two repos for examples and for reference:

`git clone https://github.com/SoftwareQuTech/CQC-Python`
`https://github.com/SoftwareQuTech/SimulaQron`
