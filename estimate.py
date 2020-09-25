import math
from numpy import random


class Estimator:

    def __init__(self, num_gates, capacity, avg, std):
        assert (num_gates > 0)
        self.num_gates = num_gates
        self.capacity = capacity
        self.avg = avg
        self.std = std

    def get_giveaway(self, gates):
        # Estimate the future giveaway for the partially filled boxes at the gates.
        return 0


class InformedEstimator(Estimator):

    def __init__(self, num_gates, capacity, avg, std):
        Estimator.__init__(self, num_gates, capacity, avg, std)
        self.compute()
        return

    def compute(self):
        # You implement this (optional) in case you want to do some onetime pre-computations.
        return

    def get_giveaway(self, gates):
        giveaway = 0

        # giveaway = self.simple_heuristic(gates)

        giveaway = self.largest_sample_to_largest_box(gates)

        # giveaway = self.overall_capacity(gates)

        return giveaway

    # Iterate through the gates and fill them with the samples taken from the normal distribution
    def simple_heuristic(self, gates):
        giveaway = 0

        for i in range(self.num_gates):
            current_gate_weight = gates[i]

            while current_gate_weight < self.capacity:
                next_weight = random.normal(self.avg, self.std)
                current_gate_weight += next_weight

            giveaway += current_gate_weight - self.capacity

        return giveaway

    # Sample for each remaining gate and fit the largest samples into the most empty boxes.
    # Repeat until all boxes are full.
    def largest_sample_to_largest_box(self, gates):
        giveaway = 0

        open_gates = self.num_gates
        sorted_gates = sorted(gates)

        while open_gates > 0:
            next_weight_samples = random.normal(self.avg, self.std, open_gates)
            sorted_samples = sorted(next_weight_samples, reverse=True)

            for i in range(len(sorted_gates)):
                sorted_gates[i] += sorted_samples[i]
                if sorted_gates[i] >= self.capacity:
                    giveaway += sorted_gates[i] - self.capacity

            sorted_gates = [gate for gate in sorted_gates if gate < self.capacity]
            sorted_gates = sorted(sorted_gates)
            open_gates = len(sorted_gates)

        return giveaway

    # Just look at the overall remaining capacity and not at the distribution between different boxes.
    def overall_capacity(self, gates):
        max_capacity = self.num_gates * self.capacity
        used_capacity = sum(gates)

        while used_capacity < max_capacity:
            next_weight = random.normal(self.avg, self.std)
            used_capacity += next_weight

        giveaway = used_capacity - max_capacity

        return giveaway
