from dataclasses import asdict
import os
import csv
import pkgutil
import typing

from .Locations import location_list


def extract_logic():
    # Event names
    events: set = set()
    # Location/Region: access rule logic
    rules: dict[tuple[str, str], str] = {}

    logicLines = pkgutil.get_data(__name__, "RustedMossLogic.csv").decode().splitlines()

    def add_rule(parent: str, spot: str, rule: str):
        """
        Joins a new rule + parent with potential existing rules
        assumes rule is either an empty string (for logicless)
        or a logic string with wrapper ` + (logic)`
        """
        prev = rules.get((parent, spot))
        if prev and prev != "":
            new = f"{prev} | ({rule})"
        elif prev == "":
            assert False, f"tried to add rule {rule} to existing connection {parent} -> {spot}"
            return
        else:
            new = f"({rule})" if rule != "" else ""
        rules[(parent, spot)] = new

    for logicLine in logicLines:
        lineData = logicLine.split(",")
        line = {
            "from": lineData[0],
            "to": lineData[1],
            "requires": lineData[2],
            "notes": lineData[3],
        }
        if line["from"] == "from":
            continue
        assert line["from"] != line["to"], f"self-referential: {line['from']}"
        if line["to"].startswith("e_"):
            events.add(line["to"])

        requires = line["requires"]
        if line["to"].find("[") != -1:
            # transition to transition rule
            add_rule(line["from"], line["to"], requires)

            fromRoom = line["from"].split("[")[0]
            toRoom = line["to"].split("[")[0]
            # Only do reverse transition if rooms are different
            if fromRoom != toRoom:
                add_rule(line["to"], line["from"], requires)
        elif line["to"] in location_list:
            # transition to location rule
            add_rule(line["from"], line["to"], requires)
        elif line["to"].startswith("e_"):
            # transition to event rule
            add_rule(line["from"], line["to"], requires)
    return (events, rules)
