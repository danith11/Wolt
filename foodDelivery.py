# importing Libraries

import simpy
import random
import numpy as np
import matplotlib.pyplot as plt


RANDOM_SEED = 42        # makes sure results are repeatable
SIMULATE_TIME = 180     # Simulations runs for 180 minutes( Rush Hour)
AVG_ARRIVAL_TIME = 3.0  # Average Time Between new orders
MIN_COOK_TIME = 15      # Minimum Cooking Time 
MAX_COOK_TIME = 25      # Maximum Cooking Time 
MIN_DELIVERY_TIME = 5   # Minimum Delivery Time 
MAX_DELIVERY_TIME = 15  # Maximum Delivery Time 

all_scenario_results = []


# Delivery System class
class DeliverySystem:
    def __init__(self, env, num_drivers):
        self.env = env
        # helps manage shared resources (drivers)
        self.drivers = simpy.Resource(env, capacity=num_drivers)

        self.pickup_wait_times = []
        self.total_delivery_time = []
        self.driver_busy_times = []

# Order process

def orderProcess(env, order_name, system):
    # Arrive the order
    order_arrival_time = env.now

    # Cooking time
    cook_time = random.uniform(MIN_COOK_TIME, MAX_COOK_TIME)
    yield env.timeout(cook_time)

    ready_for_pickup_time = env.now

    # Request a driver
    with system.drivers.request() as req:
        yield req  # Wait until a driver is available

        driver_acquired_time = env.now
        pickup_wait = driver_acquired_time - ready_for_pickup_time
        system.pickup_wait_times.append(pickup_wait)

        delivery_time = random.uniform(MIN_DELIVERY_TIME, MAX_DELIVERY_TIME)
        system.driver_busy_times.append(delivery_time)

        yield env.timeout(delivery_time)

        # Record Total Time
        orderd_deliverd_time = env.now

        total_time = orderd_deliverd_time-order_arrival_time
        system.total_delivery_time.append(total_time)


# Keeps generating new orders every few minutes
def setup_orders(env, system):
    order_id = 0

    while True:
        # Time gap between new orders
        arrival_interval = random.expovariate(1.0/AVG_ARRIVAL_TIME)
        yield env.timeout(arrival_interval)

        order_id += 1
        env.process(orderProcess(env, f"Order-{order_id}", system))

# Sets up the environment with a given number of drivers


def run_simulation(num_drivers):
    print(f"\n--- Running Simulation: {num_drivers} Drivers ---")

    random.seed(RANDOM_SEED)

    env = simpy.Environment()

    system = DeliverySystem(env, num_drivers)

    env.process(setup_orders(env, system))

    env.run(until=SIMULATE_TIME)

    # Calculate statistics
    total_driver_busy_time = np.sum(system.driver_busy_times)
    total_driver_available_time = num_drivers * SIMULATE_TIME
    avg_utilization = (total_driver_busy_time /
                       total_driver_available_time) * 100

    avg_pickup_wait = np.mean(system.pickup_wait_times)
    max_pickup_wait = np.max(system.pickup_wait_times)
    avg_total_delivery = np.mean(system.total_delivery_time)

    # Output the results
    print(f"Total Orders Processed: {len(system.pickup_wait_times)}")
    print(f"Average pick up time : {avg_pickup_wait: .2f} minutes")
    print(f"Maximum pick up time : {max_pickup_wait: .2f} minutes")
    print(f"Average total delivery time : {avg_total_delivery:.2f} minutes")
    print(f"Average driver utilization: {avg_utilization:.2f}%")

    return {
        "drivers": num_drivers,
        "avg_pickup_wait": avg_pickup_wait,
        "avg_total_delivery": avg_total_delivery,
        "all_pickup_waits": system.pickup_wait_times,
        "all_total_time": system.total_delivery_time,
        "avg_utilization": avg_utilization
    }


if __name__ == "__main__":
    # Run Multiple Scenarios
    scenarios = [3, 5, 7]
    results = [run_simulation(num) for num in scenarios]

    # Average Pickup Wait bar chart
    driver_counts = [r['drivers'] for r in results]
    avg_waits = [r['avg_pickup_wait'] for r in results]

    plt.figure(figsize=(10, 6))
    plt.bar(driver_counts, avg_waits, color=['#d9534f', '#5cb85c', '#5bc0de'])
    plt.xlabel("Number of Drivers")
    plt.ylabel("Avrage pickup wait time(minutes)")
    plt.title("Food Delivery: Average wait for Driver vs number of drivers")
    plt.xticks(driver_counts)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("avg_pickup_wait_bar_chart.png")
    print("\nGenerated 'avg_pickup_wait_bar_chart.png'")

    # Total Delivery Time Chart
    all_total_time_data = [r['all_total_time'] for r in results]

    plt.figure(figsize=(10, 6))
    plt.boxplot(all_total_time_data, labels=driver_counts)
    plt.xlabel("Number of Drivers")
    plt.ylabel("Total Delivery time for destribution(minutes)")
    plt.title("Food Delivery: Total Customer Delivery Time Distribution")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("total_delivery_time_box_plot.png")
    print("Generated 'total_delivery_time_box_plot.png'")

    # Driver Utilization Chart
    utilizations = [r['avg_utilization'] for r in results]

    plt.figure(figsize=(10, 6))
    plt.bar(driver_counts, utilizations, color=[
            '#d9534f', '#5cb85c', '#5bc0de'])
    plt.xlabel("Number of Drivers")
    plt.ylabel("Average Driver Utilization (%)")
    plt.title("Cost Analysis: Driver Utilization vs. Number of Drivers")
    plt.xticks(driver_counts)
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for i, v in enumerate(utilizations):
        plt.text(driver_counts[i], v + 1,
                 f"{v:.1f}%", ha='center', fontweight='bold')

    plt.savefig("driver_utilization_bar_chart.png")
    print("Generated 'driver_utilization_bar_chart.png'")
