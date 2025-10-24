# Wolt
# Food Delivery Dispatch Simulation Case Study

This is a simulation-based case study for a "Wolt" food delivery dispatch system, built in Python using the `simpy` library. The simulation models the flow of orders from restaurants to customers and analyzes how the number of available drivers impacts system performance.

## Project Overview

The goal of this simulation is to analyze the trade-off between operational cost (number of drivers) and customer satisfaction (wait times). It answers the question: "How many drivers do we need to maintain a good quality of service during a 3-hour dinner rush?"

The simulation tracks three key metrics:
1.  **Pickup Wait Time:** The time food sits "ready for pickup" before a driver collects it (a measure of food quality).
2.  **Total Delivery Time:** The customer's full experience, from placing the order to receiving it.
3.  **Driver Utilization:** The percentage of time drivers are actively busy (a measure of cost efficiency).

## How to Run

### 1. Requirements
* Python 3.12.6
* `simpy`
* `numpy`
* `matplotlib`

### 2. Installation
You can install the required packages using pip:
```bash
pip install simpy numpy matplotlib
