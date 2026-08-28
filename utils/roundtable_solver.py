from ortools.sat.python import cp_model
import pandas as pd
from collections import defaultdict

def generate_roundtable_schedule(moderators, roundtable_configs, days, target_quota):
    model = cp_model.CpModel()
    mod_ids = list(set([m['id'] for m in moderators]))
    num_roundtables = len(roundtable_configs)
    
    # Track which day each moderator is working
    mod_working_days = defaultdict(lambda: defaultdict(bool))
    # Track each moderator's shift
    mod_shift_map = {}
    
    for mod in moderators:
        mod_working_days[mod['id']][mod['day']] = True
        mod_shift_map[mod['id']] = mod['shift']
            
    # Variables
    x = {}
    for m in mod_ids:
        for r in range(num_roundtables):
            x[(m, r)] = model.NewBoolVar(f'x_{m}_{r}')
            
    r_day = {}
    for r in range(num_roundtables):
        for d in days:
            r_day[(r, d)] = model.NewBoolVar(f'r_day_{r}_{d}')
            
    # Constraints per specific roundtable
    for r, config in enumerate(roundtable_configs):
        # Must happen on exactly one day
        model.AddExactlyOne(r_day[(r, d)] for d in days)
        
        # Individual Min/Max sizes
        r_size = sum(x[(m, r)] for m in mod_ids)
        model.Add(r_size >= config['Min Mods'])
        model.Add(r_size <= config['Max Mods'])
        
        # Shift Restrictions
        for m in mod_ids:
            shift = mod_shift_map[m]
            allowed = False
            if shift == "Morning" and config.get('Allow Morning', False): allowed = True
            if shift == "Midday" and config.get('Allow Midday', False): allowed = True
            if shift == "Night" and config.get('Allow Night', False): allowed = True
            
            # If shift is not allowed for this specific RT, force attendance to 0
            if not allowed:
                model.Add(x[(m, r)] == 0)
        
    # Global Moderator Constraints
    for m in mod_ids:
        # Weekly quota
        model.Add(sum(x[(m, r)] for r in range(num_roundtables)) == target_quota)
        
        for d in days:
            mods_rts_today = []
            for r in range(num_roundtables):
                is_in_r_today = model.NewBoolVar(f'm_{m}_in_r_{r}_on_d_{d}')
                model.AddMultiplicationEquality(is_in_r_today, [x[(m, r)], r_day[(r, d)]])
                mods_rts_today.append(is_in_r_today)
                
            # Max 1 roundtable per day
            model.Add(sum(mods_rts_today) <= 1)
            
            # Can't attend if not working that day
            if not mod_working_days[m][d]:
                model.Add(sum(mods_rts_today) == 0)

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        results = []
        for r, config in enumerate(roundtable_configs):
            r_d = [d for d in days if solver.Value(r_day[(r, d)]) == 1][0]
            r_mods = [m for m in mod_ids if solver.Value(x[(m, r)]) == 1]
            
            results.append({
                'Roundtable': config['RT Name'],
                'Day': r_d,
                'Total_Count': len(r_mods),
                'Moderators': ", ".join(r_mods)
            })
        return pd.DataFrame(results)
    else:
        return None
