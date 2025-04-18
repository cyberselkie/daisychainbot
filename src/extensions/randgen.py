import json
import random
from collections import Counter

import arc

# For more info on plugins & extensions, see: https://arc.hypergonial.com/guides/plugins_extensions/

plugin = arc.GatewayPlugin("randgen")


@plugin.include
@arc.slash_command("gen", "Generate a random PL1 character.")
async def gen(ctx: arc.GatewayContext) -> None:
    w1 = select_weapon()
    w2 = select_weapon()
    stats, primary, secondary = assign_stats(w1, w2)
    format_weapons = f"`Main: {w1} [{primary}]`\n`Offhand: {w2} [{secondary}]`"

    charm = stats["Charm"]
    focus = stats["Focus"]
    heart = stats["Heart"]
    power = stats["Power"]
    format_stats = f"`Charm   Focus   Heart   Power`\n`  {charm}       {focus}       {heart}       {power}  `"

    health, speed, spells = calculate_secondary_stats(stats, primary)
    format_secondary_stats = f"`Health       Speed     Spells`\n`  {health}            {speed}          {spells}  `"

    abilities = select_abilities(w1, w2)
    format_abilities = f"`Abilities:` `{abilities[0]}` `{abilities[1]}`"

    if spells > 0:
        spells_list = select_spells(spells)
        format_spells = "`Spells:` "
        for i in spells_list:
            format_spells = format_spells + f"`{i}` "
        await ctx.respond(
            f"{format_weapons}\n{format_stats}\n{format_secondary_stats}\n{format_abilities}\n{format_spells}"
        )
    else:
        await ctx.respond(f"{format_weapons}\n{format_stats}\n{format_secondary_stats}\n{format_abilities}")


def open_json(filename: str):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


def select_weapon():
    weapons = [
        "Baseball Bat",
        "Brass Knuckles",
        "Chainsaw",
        "Gun",
        "Hat",
        "Knives",
        "Katana",
        "Microphone",
        "Roller Skates",
        "Whip",
    ]
    w = random.choice(weapons)
    return w


def assign_stats(w1: str, w2: str):
    data = open_json("src/data/weapons.json")
    stats = ["Charm", "Focus", "Heart", "Power"]
    weights = []

    picks = Counter()

    # Get primary statistic
    primary = data["Weapons"][w1]["primary"]
    secondary = data["Weapons"][w2]["primary"]
    if primary == secondary:
        secondary = data["Weapons"][w2]["secondary"]

    # weight statistics
    for x in stats:
        if x == primary or x == secondary:
            weight = 0.35
        else:
            weight = 0.15
        weights.append(weight)

    # assign statistics
    for i in range(6):
        pick = random.choices(stats, weights=weights)
        pick = pick[0]
        picks[pick] += 1

    # everything starts at 1, so add 1 to everything
    for n in stats:
        picks[n] += 1

    return picks, primary, secondary


def calculate_secondary_stats(stats, primary: str):
    health = stats["Heart"] * 3
    speed = stats["Focus"] + stats[primary]
    spells = stats["Charm"] - 1
    return health, speed, spells


def select_abilities(w1: str, w2: str):
    data = open_json("src/data/abilities.json")
    choices = [w1, w2]
    abilities = []
    for i in range(2):
        choice = random.choice(choices)
        ability_list = data[choice]["t1"]
        random_index = random.randint(0, len(ability_list) - 1)
        abilities.append(ability_list[random_index]["name"])
    while abilities[0] == abilities[1]:
        abilities.remove(abilities[1])
        choice = random.choice(choices)
        ability_list = data[choice]["t1"]
        random_index = random.randint(0, len(ability_list) - 1)
        abilities.append(ability_list[random_index]["name"])

    return abilities


def select_spells(spells: int):
    data = open_json("src/data/spells.json")
    spells_list = []
    for i in range(spells):
        ability_list = data["t1"]
        random_index = random.randint(0, len(ability_list) - 1)
        spells_list.append(ability_list[random_index]["name"])
    return spells_list


@arc.loader
def load(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)


@arc.unloader
def unload(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
