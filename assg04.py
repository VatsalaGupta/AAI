import sys
import math
from z3 import *

# Function to read the automatically generated input file
def load_data(file_name):
    ports_count = 0
    prices = []
    vehicles = []
    
    try:
        with open(file_name, 'r') as f:
            for line in f:
                # Ignore comments and empty lines
                if line.startswith('%') or not line.strip():
                    continue
                
                parts = line.split()
                # Reading K (number of ports)
                if parts[0] == 'K':
                    ports_count = int(parts[1])
                # Reading P (price list)
                elif parts[0] == 'P':
                    prices = [int(p) for p in parts[1:]]
                # Reading V (vehicle data)
                elif parts[0] == 'V':
                    # data: id, arrival, departure, work
                    vehicles.append([int(x) for x in parts[1:]])
        return ports_count, prices, vehicles
    except FileNotFoundError:
        print("Input file not found. Please run the generator script first.")
        sys.exit()

def run_scheduler():
    # 1. Load the data from input.txt
    K, P, vehicle_list = load_data('input.txt')
    
    # 2. Setup the Optimization Solver
    solver = Optimize()
    results = []
    
    # Define variables for each vehicle
    for v in vehicle_list:
        v_id, arr, dep, work = v
        
        # We need to decide which port and what start time
        port_choice = Int(f'port_{v_id}')
        start_time = Int(f'start_{v_id}')
        duration = Int(f'dur_{v_id}')
        cost = Int(f'cost_{v_id}')
        
        # Constraints: Port must be within range 1 to K
        solver.add(port_choice >= 1, port_choice <= K)
        
        # Constraints: Must start at or after arrival
        solver.add(start_time >= arr)
        
        # Duration logic: The duration is ceil(work / port_number)
        # In Z3, we can write this as: duration * port >= work 
        # AND (duration - 1) * port < work
        solver.add(duration * port_choice >= work)
        solver.add((duration - 1) * port_choice < work)
        
        # Must finish before or at departure
        solver.add(start_time + duration <= dep)
        
        # Cost logic: duration * price of the chosen port
        # We use If-Else chain to pick the right price from the list P
        chosen_price = P[0]
        for i in range(1, K):
            chosen_price = If(port_choice == i + 1, P[i], chosen_price)
            
        solver.add(cost == duration * chosen_price)
        
        results.append({
            'id': v_id, 'p': port_choice, 's': start_time, 
            'd': duration, 'c': cost, 'work': work
        })

    # 3. Prevent Overlapping (The most important part)
    # If two vehicles share the same port, they must not occupy it at the same time
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            v1 = results[i]
            v2 = results[j]
            
            # Condition: Are they on the same port?
            same_port = (v1['p'] == v2['p'])
            
            # Condition: Do their times stay apart?
            # (V1 ends before V2 starts) OR (V2 ends before V1 starts)
            apart = Or(v1['s'] + v1['d'] <= v2['s'], 
                       v2['s'] + v2['d'] <= v1['s'])
            
            # If same_port is true, then apart must be true
            solver.add(Implies(same_port, apart))

    # 4. Set the goal: Minimize the total cost of all vehicles
    total_bill = Sum([r['c'] for r in results])
    solver.minimize(total_bill)

    # 5. Check and print the output
    if solver.check() == sat:
        ans = solver.model()
        print(f"--- Optimization Successful ---")
        print(f"Minimum Total Cost: {ans[total_bill]}")
        print("-" * 30)
        
        for r in results:
            p_val = ans[r['p']].as_long()
            s_val = ans[r['s']].as_long()
            d_val = ans[r['d']].as_long()
            c_val = ans[r['c']].as_long()
            print(f"Vehicle {r['id']}: Port {p_val} | Time {s_val} to {s_val+d_val} | Cost {c_val}")
    else:
        print("No possible schedule fits these constraints.")

if __name__ == "__main__":
    run_scheduler()