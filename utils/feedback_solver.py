from collections import defaultdict
import pandas as pd

def schedule_feedback(moderators, overheads):
    """
    moderators: list of dicts [{'id': 'M1', 'day': 'Mon', 'shift': 'Morning'}]
    overheads: list of dicts [{'id': 'O1', 'day': 'Mon', 'shift': 'Morning', 'opt_in': True}]
    """
    # Filter overheads who are available for feedback this week
    available_ohs = [oh for oh in overheads if oh.get('opt_in', True)]
    
    # Organize overheads by day and shift
    oh_by_shift = defaultdict(list)
    for oh in available_ohs:
        key = (oh['day'], oh['shift'])
        oh_by_shift[key].append(oh['id'])
        
    schedule = []
    
    # Track how many feedbacks each overhead is assigned to balance the load
    oh_load = defaultdict(int)
    
    # Assign moderators
    for mod in moderators:
        key = (mod['day'], mod['shift'])
        possible_ohs = oh_by_shift.get(key, [])
        
        if not possible_ohs:
            schedule.append({'mod_id': mod['id'], 'oh_id': 'UNASSIGNED', 'day': mod['day'], 'shift': mod['shift']})
            continue
            
        # Sort possible overheads by their current load to ensure equal distribution
        possible_ohs.sort(key=lambda oh_id: oh_load[oh_id])
        
        # Pick the overhead with the lowest load for this shift
        chosen_oh = possible_ohs[0]
        oh_load[chosen_oh] += 1
        
        schedule.append({
            'mod_id': mod['id'], 
            'oh_id': chosen_oh, 
            'day': mod['day'], 
            'shift': mod['shift']
        })
        
    return pd.DataFrame(schedule)
