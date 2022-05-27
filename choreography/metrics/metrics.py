import json

from tabulate import tabulate


def cc():
    file = open("metrics/cc.json", "r")
    metrics = json.load(file)
    table = []
    max_module_complexity = 0
    total_complexity = 0
    for module in metrics:
        for function in metrics[module]:
            table.append([function["name"], function["complexity"]])
            total_complexity += function["complexity"]
            max_module_complexity = max(function["complexity"], max_module_complexity)
    print(tabulate(table))
    print(f"Max module complexity = {max_module_complexity}")
    print(f"Total complexity = {total_complexity}")


def loc():
    file = open("metrics/raw.json", "r")
    metrics = json.load(file)
    loc = 0
    for module in metrics:
        loc += metrics[module]["loc"]
    print(f"LOC = {loc}")


def hal():
    file = open("metrics/hal.json", "r")
    metrics = json.load(file)
    total_effort = 0
    total_bugs = 0
    for module in metrics:
        module_effort = metrics[module]["total"][9]
        module_bugs = metrics[module]["total"][11]
        total_effort += module_effort
        total_bugs += module_bugs
    print(f"Total effort = {total_effort}")
    print(f"Expected total number of bugs = {total_bugs}")


cc()
loc()
hal()
