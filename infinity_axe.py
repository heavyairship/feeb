import random, sys

sys.setrecursionlimit(5000)

INDENT = "  "
CRIT_ROLL = 20
CRIT_MULTIPLIER = 2

def roll(n):
    return int(random.random()*n)+1

def hit_roll(hit_dc, enemy_ac, indent, verbose=True):
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
    return out

def dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=True, crit=False):
    dmg = 0
    for i in range(num_die):
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

def new_crit_thread(hit_dc, enemy_ac, indent, verbose=True):
    total_dmg = 0
    dmg = 0
    if verbose:
        msg = f"{indent}START THREAD"
        print(msg)
    while True:
        dmg = _inf_axe_attack(hit_dc, enemy_ac, indent + INDENT, verbose=verbose)
        if dmg == 0:
            break
        total_dmg += dmg
    if verbose:
        msg = f"{indent}END THREAD: TOTAL CRIT THREAD DMG: {total_dmg}"
        print(msg)
    return total_dmg

def _inf_axe_attack(hit_dc, enemy_ac, indent, verbose=True):

    # Infinity Axe key stats
    die_rank = 12
    num_die = 1
    dmg_mod = 5

    hit_result = hit_roll(hit_dc, enemy_ac, indent, verbose=verbose)

    if not hit_result["crit"]:
        return dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=verbose, crit=False) if hit_result["hit"] else 0
    else:
        return dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=verbose, crit=True) + new_crit_thread(hit_dc, enemy_ac, indent + INDENT, verbose=verbose)

def inf_axe_attack(hit_dc, enemy_ac, verbose=True):
    tot_dmg = _inf_axe_attack(hit_dc, enemy_ac, '', verbose=verbose)
    if verbose:
        print(f"TOTAL DMG: {tot_dmg}")
    return tot_dmg

def average(results):
    s = 0
    for r in results:
        s += r
    return s/len(results)

def median(results):
    _sorted = sorted(results)
    middle = int(len(results)/2)
    if len(results) % 2 == 0:
        return average([_sorted[middle],_sorted[middle-1]]) 
    return _sorted[middle]

enemy_acs = [11, 12, 13, 14, 15]
hit_dc = 9
trials = int(1e4)
verbose = False

for enemy_ac in enemy_acs:
    results = []
    for i in range(trials):
        try:
            results.append(inf_axe_attack(hit_dc, enemy_ac, verbose=verbose))
        except RecursionError as e:
            print(e)
        if verbose:
            print("************")
    print(f"ENEMY AC: {enemy_ac}")
    print(f"PLAYER HIT DC: {hit_dc}")
    print(f"AVERAGE DMG (N={trials}): {average(results)}")
    print(f"MEDIAN DMG (N={trials}): {median(results)}")
    print("************")
