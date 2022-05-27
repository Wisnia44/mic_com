import json

from tabulate import tabulate


def cc(results, composition):
    file = open(f"../metrics/{composition}/cc.json", "r")
    metrics = json.load(file)
    table = []
    max_module_complexity = 0
    total_complexity = 0
    for module in metrics:
        for function in metrics[module]:
            table.append([function["name"], function["complexity"]])
            total_complexity += function["complexity"]
            max_module_complexity = max(function["complexity"], max_module_complexity)
    results.write(tabulate(table))
    results.write(f"\nMax module complexity = {max_module_complexity}\n")
    results.write(f"Total complexity = {total_complexity}\n")


def loc(results, composition):
    file = open(f"../metrics/{composition}/raw.json", "r")
    metrics = json.load(file)
    loc = 0
    for module in metrics:
        loc += metrics[module]["loc"]
    results.write(f"LOC = {loc}\n")


def hal(results, composition):
    file = open(f"../metrics/{composition}/hal.json", "r")
    metrics = json.load(file)
    total_effort = 0
    total_bugs = 0
    for module in metrics:
        module_effort = metrics[module]["total"][9]
        module_bugs = metrics[module]["total"][11]
        total_effort += module_effort
        total_bugs += module_bugs
    results.write(f"Total effort = {total_effort}\n")
    results.write(f"Expected total number of bugs = {total_bugs}\n")


def calculate_metrics(composition):
    results = open(f"../metrics/{composition}/results.txt", "w")
    cc(results, composition)
    loc(results, composition)
    hal(results, composition)
    results.close()


calculate_metrics("choreography")
calculate_metrics("orchestration")
