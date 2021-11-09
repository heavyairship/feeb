import dnd
import numpy
import matplotlib.pyplot

def hex_attack(indent, verbose=True, crit=False):
    # Hex key stats
    die_rank = 6
    num_die = 1
    dmg_mod = 0
    dnd.log(f"{indent}APPLYING HEX", verbose)
    return dnd.dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=verbose, crit=crit)

def eldritch_blast_attack(hit_dc, enemy_ac, indent, verbose=True, hex=False):
    # Eldritch Blast key stats
    die_rank = 10
    num_die = 1
    dmg_mod = 5

    hit_result = dnd.hit_roll(hit_dc, enemy_ac, indent, verbose=verbose)
    if hit_result["hit"]:
        return dnd.dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=verbose, crit=hit_result["crit"]) + \
            (hex_attack(indent + dnd.INDENT, verbose=verbose, crit=hit_result["crit"]) if hex else 0)
    return 0

def tentacle_attack(hit_dc, enemy_ac, indent, verbose=True, hex=False):
    # Tentacle key stats
    die_rank = 8
    num_die = 2
    dmg_mod = 5

    hit_result = dnd.hit_roll(hit_dc, enemy_ac, indent, verbose=verbose)
    if hit_result["hit"]:
       return dnd.dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=verbose, crit=hit_result["crit"]) + \
            (hex_attack(indent + dnd.INDENT, verbose=verbose, crit=hit_result["crit"]) if hex else 0)
    return 0

def salamandrew_attack(num_eb, hit_dc, enemy_ac, verbose=True, hex=False):
    tot_dmg = 0
    for _ in range(num_eb):
        tot_dmg += eldritch_blast_attack(hit_dc, enemy_ac, '', verbose=verbose, hex=hex)
    tot_dmg += tentacle_attack(hit_dc, enemy_ac, '', verbose=verbose, hex=hex)
    dnd.log(f"TOTAL DMG: {tot_dmg}", verbose)
    return tot_dmg

def run_simulations():
    enemy_acs = range(15, 22)
    rod_dmg = 2
    num_eb = 3
    hit_dc = 10 + rod_dmg
    trials = 1000
    verbose = False
    hex = True
    for enemy_ac in enemy_acs:
        data = []
        for _ in range(trials):
            data.append(salamandrew_attack(num_eb, hit_dc, enemy_ac, verbose=verbose, hex=hex))
            dnd.log("************", verbose)

        data = sorted(data)
        average = numpy.average(data)
        median = int(numpy.median(data))

        print(f"ENEMY AC: {enemy_ac}")
        print(f"PLAYER HIT DC: {hit_dc}")
        print(f"AVERAGE DMG (N={trials}): {average}")
        print(f"MEDIAN DMG (N={trials}): {median}")
        print("************")

        _, ax = matplotlib.pyplot.subplots()
        ax.hist(data, bins=range(0,max(data)), ec="k")
        ax.locator_params(axis="y", integer=True)
        ax.locator_params(axis="x", integer=True)
        ax.set_ylabel('count')
        ax.set_xlabel('dmg')
        ax.set_title(f"salamandrew dmg vs ac={enemy_ac} (med={median}, avg={average})")
        matplotlib.pyplot.savefig(f"./data/sal/ac_{enemy_ac}.png")

if __name__ == "__main__":
    run_simulations()