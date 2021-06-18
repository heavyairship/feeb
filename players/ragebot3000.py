import numpy
import math
import matplotlib.pyplot
import dnd
import dnd_stats

MAX_DMG = 1e7

def inf_axe_attack(hit_dc, enemy_ac, indent, advantage=False, verbose=True):

    # Infinity Axe key stats
    die_rank = 12
    num_die = 1
    dmg_mod = 5

    hit_result = dnd.hit_roll(hit_dc, enemy_ac, indent, advantage=advantage, verbose=verbose)

    if not hit_result["crit"]:
        return dnd.dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=verbose, crit=False) if hit_result["hit"] else 0
    
    tot_dmg = dnd.dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=verbose, crit=True)
    crit_threads = 1
    dnd.log(f"{indent}ADDING CRIT THREAD", verbose)
    while crit_threads > 0:
        if tot_dmg > MAX_DMG:
            return tot_dmg
        dnd.log(f"{indent}START CRIT THREAD (PENDING CRIT THREADS: {crit_threads})", verbose)
        crit_threads -= 1
        thread_dmg = 0
        while True:
            hit_result = dnd.hit_roll(hit_dc, enemy_ac, indent + dnd.INDENT, advantage=advantage, verbose=verbose)
            if not hit_result["hit"]:
                break
            if not hit_result["crit"]:
                thread_dmg += dnd.dmg_roll(die_rank, num_die, dmg_mod, indent + dnd.INDENT, verbose=verbose, crit=False)
            else:
                crit_threads += 1
                dnd.log(f"{indent + dnd.INDENT}ADDING CRIT THREAD", verbose)
                thread_dmg += dnd.dmg_roll(die_rank, num_die, dmg_mod, indent + dnd.INDENT, verbose=verbose, crit=True)
        dnd.log(f"{indent}END THREAD: CRIT THREAD DMG: {thread_dmg}", verbose)
        tot_dmg += thread_dmg
    return tot_dmg

def ragebot3000_attack(attacks, hit_dc, enemy_ac, advantage=False, verbose=True):
    tot_dmg = 0
    for _ in range(attacks):
        tot_dmg += inf_axe_attack(hit_dc, enemy_ac, '', advantage=advantage, verbose=verbose)
    dnd.log(f"TOTAL DMG: {tot_dmg}", verbose)
    return tot_dmg

def get_bins():
    out = list(range(0, 101))
    for e in range(2, 10):
        for i in range(1, 11):
            out.append(i*(10**e))
    return sorted(list(set(out)))

def get_log_bins():
    return [x/10 for x in range(100)]

def run_simulations():
    enemy_acs = range(15,22)
    attacks = 2
    hit_dc = 9
    advantage = True
    champion = True
    trials = 100
    verbose = False
    bins = get_bins()
    log_bins = get_log_bins()

    if champion:
        dnd.crit = lambda roll: roll == 19 or roll == 20

    for enemy_ac in enemy_acs:
        data = []
        for _ in range(trials):
            data.append(ragebot3000_attack(attacks, hit_dc, enemy_ac, advantage=advantage, verbose=verbose))
            dnd.log("************", verbose)

        data = sorted(data)
        average = numpy.average(data)
        median = int(numpy.median(data))
        log_data = sorted([math.log(x, 10) if x > 0 else 0 for x in data])

        print(f"ENEMY AC: {enemy_ac}")
        print(f"PLAYER HIT DC: {hit_dc}")
        print(f"AVERAGE DMG (N={trials}): {average}")
        print(f"MEDIAN DMG (N={trials}): {median}")
        print("************")

        # count vs dmg, log scale
        _, ax = matplotlib.pyplot.subplots()
        ax.hist(data, bins=dnd_stats.trim_bins(bins, data), ec="k")
        ax.locator_params(axis="y", integer=True)
        ax.locator_params(axis="x", integer=True)
        ax.set_xscale('log')
        ax.set_ylabel('count')
        ax.set_xlabel('dmg')
        ax.set_title(f"ragebot3000 dmg vs ac={enemy_ac} (med={median}, avg={average})")
        matplotlib.pyplot.savefig(f"./data/bot/ac_{enemy_ac}.png")

        # count vs log(dmg), normal scale
        _, ax = matplotlib.pyplot.subplots()
        ax.hist(log_data, bins=dnd_stats.trim_bins(log_bins, log_data), ec="k")
        ax.locator_params(axis="y", integer=True)
        ax.locator_params(axis="x", integer=True)
        ax.set_ylabel('count')
        ax.set_xlabel('log(dmg)')
        ax.set_title(f"ragebot3000 log(dmg) vs ac={enemy_ac} (med={median}, avg={average})")
        matplotlib.pyplot.savefig(f"./data/bot/ac_{enemy_ac}_log.png")

run_simulations()