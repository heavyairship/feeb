import random, sys, numpy, math
import matplotlib.pyplot as plt

sys.setrecursionlimit(5000)

INDENT = "  "
CRIT_ROLL = 20
CRIT_MULTIPLIER = 2
MAX_DMG = 500000

def roll(n):
    return int(random.random()*n)+1

def hit_roll(hit_dc, enemy_ac, indent, advantage=False, verbose=True):
    _roll = roll(20)
    tot_roll = _roll+hit_dc
    msg = f"{indent}HIT ROLL: {_roll} + {hit_dc} = {tot_roll}"
    out = {"crit": False, "hit": False}
    if _roll == CRIT_ROLL:
        msg += f" (CRIT)"
        out["crit"] = True
    if (tot_roll >= enemy_ac) or out["crit"]:
        msg += f" (HIT)"
        out["hit"] = True
    else:
        msg += f" (MISS)"
    if verbose:
        print(msg)
    if not out["hit"] and advantage:
        if verbose:
            print(f"{indent}APPLY ADVANTAGE")
        return hit_roll(hit_dc, enemy_ac, indent, advantage=False, verbose=verbose)
    return out

def dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=True, crit=False):
    dmg = 0
    for _ in range(num_die):
        dmg += roll(die_rank)
    tot_dmg = dmg + dmg_mod
    if verbose:
        if crit:
            tot_dmg *= CRIT_MULTIPLIER 
            msg = f"{indent}{INDENT}DMG ROLL: ({dmg} + {dmg_mod}) * {CRIT_MULTIPLIER} = {tot_dmg}"
        else:
            msg = f"{indent}{INDENT}DMG ROLL: {dmg} + {dmg_mod} = {tot_dmg}"
        print(msg)
    return tot_dmg

def _inf_axe_attack(hit_dc, enemy_ac, indent, advantage=False, verbose=True):

    # Infinity Axe key stats
    die_rank = 12
    num_die = 1
    dmg_mod = 5

    hit_result = hit_roll(hit_dc, enemy_ac, indent, advantage=advantage, verbose=verbose)

    if not hit_result["crit"]:
        return dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=verbose, crit=False) if hit_result["hit"] else 0
    
    tot_dmg = dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=verbose, crit=True)
    crit_threads = 1
    if verbose:
        print(f"{indent}ADDING CRIT THREAD")
    while crit_threads > 0:
        if verbose:
            msg = f"{indent}START CRIT THREAD (PENDING CRIT THREADS: {crit_threads})"
            print(msg)
        crit_threads -= 1
        thread_dmg = 0
        while True:
            hit_result = hit_roll(hit_dc, enemy_ac, indent + INDENT, advantage=advantage, verbose=verbose)
            if not hit_result["hit"]:
                break
            if not hit_result["crit"]:
                thread_dmg += dmg_roll(die_rank, num_die, dmg_mod, indent + INDENT, verbose=verbose, crit=False)
            else:
                crit_threads += 1
                if verbose:
                    print(f"{indent + INDENT}ADDING CRIT THREAD")
                thread_dmg += dmg_roll(die_rank, num_die, dmg_mod, indent + INDENT, verbose=verbose, crit=True)
        if verbose:
            msg = f"{indent}END THREAD: CRIT THREAD DMG: {thread_dmg}"
            print(msg)
        tot_dmg += thread_dmg
    return tot_dmg

def inf_axe_attack(hit_dc, enemy_ac, advantage=False, verbose=True):
    tot_dmg = _inf_axe_attack(hit_dc, enemy_ac, '', advantage=advantage, verbose=verbose)
    if verbose:
        print(f"TOTAL DMG: {tot_dmg}")
    return tot_dmg

def get_bins():
    out = list(range(0, 101))
    for e in range(2, 10):
        for i in range(1, 11):
            out.append(i*(10**e))
    return sorted(list(set(out)))

def get_log_bins():
    return [x/10 for x in range(100)]

def trim_bins(bins, data):
    return [x for x in bins if x <= max(data)+1
    ]
enemy_acs = range(15,22)
hit_dc = 9
advantage = True
trials = 1000
verbose = False
bins = get_bins()
log_bins = get_log_bins()

for enemy_ac in enemy_acs:
    data = []
    for i in range(trials):
        data.append(inf_axe_attack(hit_dc, enemy_ac, advantage=advantage, verbose=verbose))
        if verbose:
            print("************")

    average = numpy.average(data)
    median = int(numpy.median(data))
    data = sorted(data)
    log_data = sorted([math.log(x, 10) if x > 0 else 0 for x in data])

    print(f"ENEMY AC: {enemy_ac}")
    print(f"PLAYER HIT DC: {hit_dc}")
    print(f"AVERAGE DMG (N={trials}): {average}")
    print(f"MEDIAN DMG (N={trials}): {median}")
    print("************")

    fig, ax = plt.subplots()
    ax.hist(data, bins=trim_bins(bins, data), ec="k")
    ax.locator_params(axis="y", integer=True)
    ax.locator_params(axis="x", integer=True)
    ax.set_xscale('log')
    ax.set_ylabel('count')
    ax.set_xlabel('log(dmg)')
    ax.set_title(f"infinity axe dmg vs ac={enemy_ac} (median={median})")
    plt.savefig(f"./data/ac_{enemy_ac}.png")

    fig, ax = plt.subplots()
    ax.hist(log_data, bins=trim_bins(log_bins, log_data), ec="k")
    ax.locator_params(axis="y", integer=True)
    ax.locator_params(axis="x", integer=True)
    ax.set_ylabel('count')
    ax.set_xlabel('log(dmg)')
    ax.set_title(f"infinity axe log(dmg) vs ac={enemy_ac} (median={median})")
    plt.savefig(f"./data/ac_{enemy_ac}_log.png")
