# Agent-Based Model to simulate infectious disease outbreaks

## Summary

A simple model of agents (persons) moving randomly in a small world and getting infected by some disease. All agents start healthy and one of them gets infected at some point in the simulation. Then, the disease is spread. Every step, each agent can move randomly to a neighbor cell. If there is a cell containing healthy persons and infected persons, the healthy persons can be infected with some probability. The simulation and the model were created using [mesa](https://github.com/projectmesa/mesa/), a Python framework for Agent-Based Modeling. For a tutorial on how to use mesa check [this](http://mesa.readthedocs.io/en/latest/intro-tutorial.html).

As the model runs, some statistics about the evolution of the outbreak are collected and plotted (number of infected, number of susceptible, etc. )

## How to Run

To launch the interactive server, as described in the [last section of the tutorial](http://mesa.readthedocs.io/en/latest/intro-tutorial.html#adding-visualization), run:

```
    $ python run.py
```

If your browser doesn't open automatically, point it to [http://127.0.0.1:8521/](http://127.0.0.1:8521/). When the visualization loads, press Reset, then Run.


## Files

* ``model.py``: Final version of the model.
* ``server.py``: Creates and launches interactive visualization.

## Further Reading

The full tutorial describing how to build a model with mesa can be found at:
http://mesa.readthedocs.io/en/latest/intro-tutorial.html

This model is inspired from [this paper](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0208775) where authors analyze the outbreak of a disease in some little towns in England using Agent-Based Model.

 ____
The model is build using Python 3. You will also need the following packages:
* mesa
* matplotlib
* numpy

Required dependencies are listed in the provided `requirements.txt` file which can be installed by running `pip install -r requirements.txt`
