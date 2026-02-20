import random
import math

# This function creates a random test case for the EV charging problem
def create_random_input(filename="input.txt"):
    # Randomly decide number of ports (e.g., between 3 and 6)
    total_ports = random.randint(3, 6)
    
    # Generate prices that increase as the port gets faster
    current_price = random.randint(5, 10)
    prices = []
    for i in range(total_ports):
        prices.append(current_price)
        current_price += random.randint(4, 10) # Price goes up for faster ports
        
    # Decide how many vehicles are in the system
    total_vehicles = random.randint(5, 10)
    
    # Write everything to the file in the required format
    with open(filename, 'w') as my_file:
        my_file.write(f"% total number of ports\n")
        my_file.write(f"K {total_ports}\n")
        
        my_file.write(f"% prices for each port\n")
        price_string = " ".join(map(str, prices))
        my_file.write(f"P {price_string}\n")
        
        my_file.write(f"% id arrival departure work\n")
        for i in range(1, total_vehicles + 1):
            arrival = random.randint(0, 50)
            work = random.randint(10, 30)
            
            # The departure must be late enough to allow charging at some port
            # Even at the fastest port, duration is ceil(work/total_ports)
            min_duration = math.ceil(work / total_ports)
            extra_time = random.randint(min_duration, work + 5)
            departure = arrival + extra_time
            
            my_file.write(f"V {i} {arrival} {departure} {work}\n")

    print(f"File '{filename}' has been generated successfully!")

if __name__ == "__main__":
    create_random_input()