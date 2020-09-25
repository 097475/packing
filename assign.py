from timeit import default_timer as timer
import math
from collections import deque


class Assign:

    def __init__(self, debug, estimator):
        self.debug = debug
        self.estimator = estimator
        return

    def assign(self, cars, gates, capacity, time):
        """
        Determines the gate number to dispatch the item in car[0].
        :param cars: List with weight of items.
        :param gates: List with weight of boxes at gates.
        :param capacity: Box capacity
        :param timer: Maximum time (in seconds) allowed for allocation; if 0, then there are no time-limits.
        :return: The gate number to assign item in car[0]
        """

        def time_is_up(start, time):
            if time == 0:
                return False
            return timer() - start >= time

        def do_assign(w, g):
            filled = False
            giveaway = 0
            gates[g] += w
            if gates[g] >= capacity:
                giveaway = gates[g] - capacity
                gates[g] = 0
                filled = True
            return (filled, giveaway)

        def undo_assign(w, g, info):
            filled, giveaway = info
            if filled:
                gates[g] = (capacity + giveaway) - w
            else:
                gates[g] -= w
            return

        # IMPLEMENT THIS ROUTINE
        # Suggestion: Use an iterative-deepening version of DFBnB.
        # Call 'self.estimator.get_giveaway(gates)' for the heuristic estimate of future giveaway.
        lowest_giveaway = math.inf  # giveaway weight of best solution found so far
        best_solution = None
        stack = deque([[None] * len(cars)])  # stack (to ensure LIFO order) initialized with an initial solution
        # a solution is a list which assigns a gate to each car
        # initially all cars have no assigned gate
        while stack:
            current_solution = stack.popleft() #get the current solution
            if None in current_solution: #not a full assignment
                next_unassigned_var = current_solution.index(None)  # get the first unassigned variable
                for g in range(len(gates)):
                    new_solution = current_solution.copy()
                    new_solution[next_unassigned_var] = g
                    for i in range(len(new_solution)):
                        if new_solution[i]:
                            do_assign(cars[i], new_solution[i])
                    current_giveaway = self.estimator.get_giveaway(gates)  # get new giveaway using heuristic
                    if current_giveaway < lowest_giveaway:
                        stack.appendleft(new_solution)
            else: # a full assignment
                for i in range(len(current_solution)):
                    do_assign(cars[i], current_solution[i])
                current_giveaway = self.estimator.get_giveaway(gates) #get new giveaway using heuristic
                if current_giveaway < lowest_giveaway:
                    lowest_giveaway = current_giveaway
                    best_solution = current_solution

        return best_solution[0]  # Return the gate to dispatch the item in the first car (car[0]).
