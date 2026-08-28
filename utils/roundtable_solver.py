from ortools.sat.python import cp_model
import pandas as pd

def generate_roundtable_schedule(moderators, num_roundtables, days, settings):
    """
    moderators: list of dicts [{'id': 'M1', 'day': 'Mon', 'shift': 'Morning'}]
    settings: dict containing min_mods, max_mods, allowed_shifts, target_quota
    """
    model = cp_model.CpModel()
    
    # Pre-process moderator availability 
    # mod_days[m][d] is True if moderator m works on day d in an allowed shift
    mod_days = defaultdict(lambda: defaultdict(bool))
    for mod in moderators:
        if mod['shift'] in settings['allowed_shifts']:
            mod_days[mod['id']][mod['day']] = True
            
    mod_ids = list(set([m['id'] for m in moderators]))
    
    # 1. Variables: x[m, r] = 1 if moderator m is in roundtable r
    x = {}
    for m in mod_ids:
        for r in range(num_roundtables):
            x[(m, r)] = model.NewBoolVar(f'x_{m}_{r}')
            
    # Also assign each roundtable to a specific day: r_day[r, d] = 1
    r_day = {}
    for r in range(num_roundtables):
        for d in days:
            r_day[(r, d)] = model.NewBoolVar(f'r_day_{r}_{d}')
            
    # 2. Constraints
    for r in range(num_roundtables):
        # A roundtable must happen on exactly one day
        model.AddExactlyOne(r_day[(r, d)] for d in days)
        
        # Roundtable size constraints
        r_size = sum(x[(m, r)] for m in mod_ids)
        model.Add(r_size >= settings['min_mods'])
        model.Add(r_size <= settings['max_mods'])
        
    for m in mod_ids:
        # Weekly quota per moderator
        model.Add(sum(x[(m, r)] for r in range(num_roundtables)) == settings['target_quota'])
        
        for d in days:
            # Max 1 roundtable per day per moderator
            # If moderator is in a roundtable on day d, they must actually be working that day
            mods_rts_today = []
            for r in range(num_roundtables):
                # We use a boolean trick: if x[m,r] and r_day[r,d] are both true, mod is busy today
                is_in_r_today = model.NewBoolVar(f'm_{m}_in_r_{r}_on_d_{d}')
                model.AddMultiplicationEquality(is_in_r_today, [x[(m, r)], r_day[(r, d)]])
                mods_rts_today.append(is_in_r_today)
                
            model.Add(sum(mods_rts_today) <= 1)
            
            # If mod doesn't work this day (or wrong shift), they can't attend roundtables today
            if not mod_days[m][d]:
                model.Add(sum(mods_rts_today) == 0)

    # 3. Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        results = []
        for r in range(num_roundtables):
            # Find the day for this roundtable
            r_d = [d for d in days if solver.Value(r_day[(r, d)]) == 1][0]
            # Find the moderators
            r_mods = [m for m in mod_ids if solver.Value(x[(m, r)]) == 1]
            
            results.append({
                'Roundtable_ID': r,
                'Day': r_d,
                'Moderators': ", ".join(r_mods),
                'Total_Count': len(r_mods)
            })
        return pd.DataFrame(results)
    else:
        return None # No feasible schedule found with given constraints
