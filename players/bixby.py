import dnd
import numpy
import matplotlib.pyplot

def divine_smite(indent, verbose=True, crit=False):
    # Divine smite stats (assuming lvl 1 spell slot)
    die_rank = 8
    num_die = 2
    dmg_mod = 0
    return dnd.dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=verbose, crit=crit)

def flail_attack(hit_dc, enemy_ac, indent, verbose=True):
    # Flail key stats
    die_rank = 8
    num_die = 1
    dmg_mod = 6

    hit_result = dnd.hit_roll(hit_dc, enemy_ac, indent, verbose=verbose)
    if hit_result["hit"]:
        return divine_smite(indent, verbose=verbose, crit=hit_result["crit"]) + dnd.dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=verbose, crit=hit_result["crit"])
    return 0

def bixby_attack(attacks, hit_dc, enemy_ac, verbose=True):
    tot_dmg = 0
    for _ in range(attacks):
        tot_dmg += flail_attack(hit_dc, enemy_ac, '', verbose=verbose)
    dnd.log(f"TOTAL DMG: {tot_dmg}", verbose)
    return tot_dmg

def run_simulations():
    enemy_acs = range(15, 22)
    attacks = 2
    hit_dc = 8
    trials = 1000
    verbose = False
    for enemy_ac in enemy_acs:
        data = []
        for _ in range(trials):
            data.append(bixby_attack(attacks, hit_dc, enemy_ac, verbose=verbose))
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
        ax.set_title(f"bixby dmg vs ac={enemy_ac} (med={median}, avg={average})")
        matplotlib.pyplot.savefig(f"./data/bix/ac_{enemy_ac}.png")

run_simulations()