from dataclasses import asdict
import os
import csv
import pkgutil
import typing

from .Locations import location_list
from .Options import Character


def extract_logic():
    # Event names
    events: set = set()
    # Location/Region: access rule logic
    rules: dict[tuple[str, str, int], str] = {}

    # Extracts logic for each character
    for character, logic_file in enumerate([
        "RustedMossLogic.csv",
        None, # TODO Maya logic
        None, # TODO Ameli logic
        "RustedMossLogic_Gimmick.csv",
    ]):
        if logic_file:
            extract_logic_file(rules, events, logic_file, character)
    
    return (events, rules)


def extract_logic_file(rules: dict[tuple[str, str, int], str], events: set, logic_file: str, character: int):
    def add_rule(parent: str, spot: str, rule: str):
        """
        Joins a new rule + parent with potential existing rules
        assumes rule is either an empty string (for logicless)
        or a logic string with wrapper ` + (logic)`
        """
        prev = rules.get((parent, spot, character))
        if prev and prev != "":
            new = f"{prev} | ({rule})"
        elif prev == "":
            assert False, f"tried to add rule {rule} to existing connection {parent} -> {spot}"
            return
        else:
            new = f"({rule})" if rule != "" else ""
        rules[(parent, spot, character)] = new

    logicLines = pkgutil.get_data(__name__, logic_file).decode().splitlines()

    for logicLine in logicLines:
        lineData = logicLine.split(",")
        line = {
            "from": lineData[0],
            "to": lineData[1],
            "requires": lineData[2],
            "notes": lineData[3],
        }
        # simple check for extra parenthesis
        assert line["requires"].count("(") == line["requires"].count(")"), f"Rule {line["from"]} -> {line["to"]} has extra parenthesis: {line["requires"]}"

        if line["from"] == "from":
            continue
        assert line["from"] != line["to"], f"self-referential: {line['from']}"
        if line["to"].startswith("e_"):
            events.add(line["to"])

        requires = line["requires"]
        if character == Character.option_gimmick:
            requires = expand_gimmick_logic(requires)

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


# from itertools import combinations
# upgrades: list[str] = [
#     "Grappling_Hook",
#     "Shotgun",
#     "Rocket_Launcher",
#     "Grappling_Hook_Upgrade",
# ]
# for i in range(1,5):  
#   all_combs = list(combinations(upgrades, i))
#   logic_ar = [" + ".join(x) for x in all_combs]
#   logic_str = "((" + ") | (".join(logic_ar) + "))"
#   print(f'jump_{i}: str = "{logic_str}"')


jump_1: str = "((Grappling_Hook) | (Shotgun) | (Rocket_Launcher) | (Grappling_Hook_Upgrade))"
jump_2: str = "((Grappling_Hook + Shotgun) | (Grappling_Hook + Rocket_Launcher) | (Grappling_Hook + Grappling_Hook_Upgrade) | (Shotgun + Rocket_Launcher) | (Shotgun + Grappling_Hook_Upgrade) | (Rocket_Launcher + Grappling_Hook_Upgrade))"
jump_3: str = "((Grappling_Hook + Shotgun + Rocket_Launcher) | (Grappling_Hook + Shotgun + Grappling_Hook_Upgrade) | (Grappling_Hook + Rocket_Launcher + Grappling_Hook_Upgrade) | (Shotgun + Rocket_Launcher + Grappling_Hook_Upgrade))"
jump_4: str = "((Grappling_Hook + Shotgun + Rocket_Launcher + Grappling_Hook_Upgrade))"
flying: str = "(Heavy_Ammo + bunny_hopping)"

def expand_gimmick_logic(rule: str):
    rule = rule.replace("Jump{1}", jump_1)
    rule = rule.replace("Jump{2}", jump_2)
    rule = rule.replace("Jump{3}", jump_3)
    rule = rule.replace("Jump{4}", jump_4)
    rule = rule.replace("Flying", flying)
    print(rule)
    return rule
