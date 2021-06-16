import random 

INDENT = "  "
CRIT_ROLL = 20
CRIT_MULTIPLIER = 2

def log(msg, verbose):
    if verbose:
        print(msg)

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
    log(msg, verbose)
    if not out["hit"] and advantage:
        log(f"{indent}APPLY ADVANTAGE", verbose)
        return hit_roll(hit_dc, enemy_ac, indent, advantage=False, verbose=verbose)
    return out

def dmg_roll(die_rank, num_die, dmg_mod, indent, verbose=True, crit=False):
    dmg = 0
    for _ in range(num_die):
        dmg += roll(die_rank)
    tot_dmg = dmg + dmg_mod
    if crit:
        tot_dmg *= CRIT_MULTIPLIER 
        log(f"{indent}{INDENT}DMG ROLL: ({dmg} + {dmg_mod}) * {CRIT_MULTIPLIER} = {tot_dmg}", verbose)
    else:
        log(f"{indent}{INDENT}DMG ROLL: {dmg} + {dmg_mod} = {tot_dmg}", verbose)
    return tot_dmg