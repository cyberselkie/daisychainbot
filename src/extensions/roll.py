import arc
import dice

# For more info on plugins & extensions, see: https://arc.hypergonial.com/guides/plugins_extensions/

plugin = arc.GatewayPlugin("roll")


@plugin.include
@arc.slash_command("roll", "Roll hits in Daisy Chainsaw.")
async def roll(
    ctx: arc.GatewayContext,
    primary: arc.Option[int, arc.IntParams("Primary statistic.")],
    secondary: arc.Option[int, arc.IntParams("Secondary statistic.")],
) -> None:
    initial_roll = dice.roll(str(primary) + "d6")
    hits = count_hits(initial_roll, secondary)  # type: ignore
    explode = 0
    rolls = ""
    # count explosions
    for i in initial_roll:
        rolls = rolls + f"`{i}` "
        if i == 1:
            explode += 1
        else:
            pass
    # roll explosions
    if explode > 0:  # noqa: SIM108
        while explode > 0:
            explode_roll = dice.roll("1d6")
            explode -= 1
            for i in explode_roll:
                if i == 1:
                    explode += 1
            for i in explode_roll:
                rolls = rolls + f"`{i}` "
        hits += count_hits(explode_roll, secondary)  # type: ignore

    await ctx.respond(f"{rolls}\n`{hits} hits.`")


def count_hits(num: list, target: int):
    hits = 0
    for i in num:
        if i <= target:
            hits += 1
        else:
            pass
    return hits


@arc.loader
def load(client: arc.GatewayClient) -> None:
    client.add_plugin(plugin)


@arc.unloader
def unload(client: arc.GatewayClient) -> None:
    client.remove_plugin(plugin)
