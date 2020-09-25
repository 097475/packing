from timeit import default_timer as timer
import math

class Assign:

    def __init__(self, debug, estimator):
        self.debug = debug
        self.estimator = estimator
        return

    def get_estimator(self):
        return self.estimator

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

        def do_assign( w, g ):
            filled = False
            giveaway = 0
            gates[g] += w
            if gates[g] >= capacity:
                giveaway = gates[g] - capacity
                gates[g] = 0
                filled = True
            return (filled, giveaway)

        def undo_assign( w, g, info ):
            filled, giveaway = info
            if filled:
                gates[g] = (capacity + giveaway) - w
            else:
                gates[g] -= w
            return

        # IMPLEMENT THIS ROUTINE
        # Suggestion: Use an iterative-deepening version of DFBnB.
        # Call 'self.estimator.get_giveaway(gates)' for the heuristic estimate of future giveaway.
        def iterative_deepening_bnb():
            start = timer()
            solution = None

            def bnb(current_solution, upper_bound, best_solution, limit, depth, giveaway):
                if time_is_up(start, time):
                    return upper_bound, best_solution
                next_unassigned_var = current_solution.index(None)  # get the first unassigned variable
                for g in range(len(gates)):
                    new_solution = current_solution.copy()  # generate new solution
                    new_solution[next_unassigned_var] = g  # assign a gate to the unassigned variable
                    info = do_assign(cars[next_unassigned_var], g)  # update the weight of the gate
                    giveaway += info[1]
                    if depth < limit:
                        if giveaway < upper_bound:
                            upper_bound, best_solution = bnb(new_solution, upper_bound, best_solution, limit, depth + 1,
                                                             giveaway)
                        else:
                            pass
                            # print("pruned")
                    else:
                        estimate = self.estimator.get_giveaway(gates) + giveaway
                        if estimate < upper_bound:
                            upper_bound, best_solution = estimate, new_solution
                        else:
                            pass
                            # print("pruned")

                    undo_assign(cars[next_unassigned_var], g, info)
                    giveaway -= info[1]

                return upper_bound, best_solution

            for limit in range(len(cars)):
                if time_is_up(start, time):
                    return solution or [0]
                else:
                    bound, tentative_solution = bnb([None] * len(cars), math.inf, None, limit, 0, 0)
                    if tentative_solution:
                        solution = tentative_solution
                    print("solution for depth:", limit+1, ":", solution)
            return solution

        selected_solution = iterative_deepening_bnb()

        print(selected_solution[0])
        print("---------")

        return selected_solution[0]  # Return the gate to dispatch the item in the first car (car[0]).
