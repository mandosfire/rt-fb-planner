from collections import defaultdict
import pandas as pd

def schedule_feedback(moderators, overheads):
    """
    moderators: list of dicts [{'id': 'M1', 'day': '17/08', 'shift': 'Morning'}]
    overheads: list of dicts [{'id': 'O1', 'day': '17/08', 'shift': 'Morning', 'opt_in': True}]
    """
    # Filter overheads who are available for feedback this week
    available_ohs = [oh for oh in overheads if oh.get('opt_in', True)]
    
    # Organize overheads by day and shift
    oh_by_shift = defaultdict(list)
    for oh in available_ohs:
        key = (oh['day'], oh['shift'])
        oh_by_shift[key].append(oh['id'])
        
    # Group all available shifts for each moderator
    mod_shifts = defaultdict(list)
    for mod in moderators:
        mod_shifts[mod['id']].append(mod)
        
    schedule = []
    
    # Track how many feedbacks each overhead is assigned to balance the load
    oh_load = defaultdict(int)
    
    # Assign exactly one feedback per moderator
    for mod_id, shifts in mod_shifts.items():
        best_oh = None
        best_shift = None
        min_load = float('inf')
        
        # Scan all shifts this moderator works to find the least loaded overhead
        for shift in shifts:
            key = (shift['day'], shift['shift'])
            possible_ohs = oh_by_shift.get(key, [])
            
            for oh_id in possible_ohs:
                if oh_load[oh_id] < min_load:
                    min_load = oh_load[oh_id]
                    best_oh = oh_id
                    best_shift = shift
        
        if best_oh:
            # Assign the moderator to the best found overhead and shift
            oh_load[best_oh] += 1
            schedule.append({
                'Moderator': mod_id, 
                'Overhead': best_oh, 
                'Day': best_shift['day'], 
                'Shift': best_shift['shift']
            })
        else:
            # If no overlapping overhead was found across any of the moderator's shifts
            schedule.append({
                'Moderator': mod_id, 
                'Overhead': 'UNASSIGNED', 
                'Day': 'N/A', 
                'Shift': 'N/A'
            })
            
    return pd.DataFrame(schedule)
