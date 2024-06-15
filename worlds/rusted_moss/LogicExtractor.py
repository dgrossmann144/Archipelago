from dataclasses import asdict
import os
import csv
import pkgutil
import typing

from .Locations import location_list

def extract_logic():
    # Rooms
    regions: set[str] = set()
    # Room: ["Room[transition number]", "Room[transition number]"]
    exits: dict[str, set[str]] = {}
    # From transition: to transition
    connectors: dict[str, str] = {}
    # Location: Room TODO maybe unneeded?
    location_to_region: dict[str, str] = {}
    # Event names
    events: set = set()
    # Location/Region: access rule logic
    rules: dict[str, str] = {}

    logicLines = pkgutil.get_data(__name__, "RustedMossLogic.csv").decode().splitlines()

    for logicLine in logicLines:
        lineData = logicLine.split(",")
        line = {
            "from": lineData[0],
            "to": lineData[1],
            "requires": lineData[2],
            "notes": lineData[3],
        }
        if line["from"] == "rm_test_4_alt_2[100383]":
            print(line)
        if line["from"] == "from":
            continue

        fromRoom = line["from"].split("[")[0]
        if line["to"].find("[") != -1:
            toRoom = line["to"].split("[")[0]
            
            # add room to regions and transition to exits
            regions.add(fromRoom)
            regions.add(toRoom)
            if exits.get(fromRoom) is None:
                exits[fromRoom] = set()
                exits.get(fromRoom).add(line["from"])
            else:
                exits.get(fromRoom).add(line["from"])
            if exits.get(toRoom) is None:
                exits[toRoom] = set()
                exits.get(toRoom).add(line["to"])
            else:
                exits.get(toRoom).add(line["to"])
            
            if fromRoom != toRoom:
                # if from and to are in different then it is a connector
                if connectors.get(line["from"]) is None:
                    connectors[line["from"]] = line["to"]
                elif connectors[line["from"]] != line["to"]:
                    print("mismatched connector!")
                    print("existing entry from " + line["from"] + " to " + connectors[line["from"]])
                    print("new entry from " + line["from"] + " to " + line["to"])
                if connectors.get(line["to"]) is None:
                    connectors[line["to"]] = line["from"]
                elif connectors[line["to"]] != line["from"]:
                    print("mismatched connector!")
                    print("existing entry from " + line["to"] + " to " + connectors[line["to"]])
                    print("new entry from " + line["to"] + " to " + line["from"])
                    
        elif line["to"] in location_list:
            regions.add(fromRoom)
            location_to_region[line["to"]] = fromRoom
        elif line["to"].startswith("e_"):
            events.add(line["to"])

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

        requires = ""
        if line["requires"] != "":
            requires = " + (" + line["requires"] + ")"
        if line["to"].find("[") != -1:
            # transition to transition rule
            if line["to"] not in rules:
                rules[line["to"]] = line["to"] + " | (" + line["from"] + requires + ")"
            else:
                rules[line["to"]] = rules[line["to"]] + " | (" + line["from"] + requires + ")"

            fromRoom = line["from"].split("[")[0]
            toRoom = line["to"].split("[")[0]
            # Only do reverse transition if rooms are different
            if fromRoom != toRoom:
                if line["from"] not in rules:
                    rules[line["from"]] = line["from"] + " | (" + line["to"] + requires + ")"
                else:
                    rules[line["from"]] = rules[line["from"]] + " | (" + line["to"] + requires + ")"
        elif line["to"] in location_list:
            # transition to location rule
            if line["to"] not in rules:
                rules[line["to"]] = "(" + line["from"] + requires + ")"
            else:
                rules[line["to"]] = rules[line["to"]] + " | (" + line["from"] + requires + ")"
        elif line["to"].startswith("e_"):
            # transition to event rule
            if line["to"] not in rules:
                rules[line["to"]] = line["to"] + " | (" + line["from"] + requires + ")"
            else:
                rules[line["to"]] = rules[line["to"]] + " | (" + line["from"] + requires + ")"
        
    # for location, rule in rules.items():
    #     print(location + ": " + rule)
    print(rules["rm_test_4_alt_2[100383]"])

    return (regions, exits, connectors, location_to_region, events, rules)
