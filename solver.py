from typing import NewType
from parse import read_input_file, write_output_file
import os
import copy
from math import exp, log
from tqdm import tqdm
"""
Args:
    tasks: list[Task], list of igloos to polish
Returns:
    output: list of igloos in order of polishing  
"""

# decay is a constant factor for each timestep
# should priotize stuff that hasn't started decaying yet

def solve_heuristic(tasks):
    # sort by profit/time ratio, decreasing
    def value(t):
        earliest_finish_time = t.duration
        best_possible_benefit = t.perfect_benefit
        if earliest_finish_time > t.deadline:
            best_possible_benefit *= exp(-0.017 * (earliest_finish_time - t.deadline))

        ratio = best_possible_benefit / t.duration
        deadline_weight = 0.0000025 * t.deadline
        return ratio - deadline_weight

    tasks = sorted(tasks, key=lambda t: -value(t))
    # print(*tasks, sep="\n")
    def value(t):
        earliest_finish_time = time + t.duration
        best_possible_benefit = t.perfect_benefit
        if earliest_finish_time > t.deadline:
            best_possible_benefit *= exp(-0.017 * (earliest_finish_time - t.deadline))

        ratio = best_possible_benefit / t.duration
        deadline_weight = 0.0005 * t.deadline
        return ratio - deadline_weight


    sol = []
    unused = []
    time = 0
    while tasks:
        if time + tasks[0].duration > 1440:
            unused.append(tasks[0].task_id)
            del tasks[0]
            continue
        sol.append(tasks[0].task_id)
        time += tasks[0].duration
        del tasks[0]
        
        tasks = sorted(tasks, key=lambda t: -value(t))
    
    for x in unused:
        sol.append(x)

    return sol

# import heapq
# def solve(tasks):
#     sol = []
#     tasks = copy.deepcopy(tasks)
#     tasks = sorted(tasks, key=lambda t: -t.deadline)
#     q = []
#     for i in range(1, len(tasks)):
#         heapq.heappush(q, (tasks[i].duration, tasks[i]))
#         gap = tasks[i].deadline - tasks[i-1].deadline

#         while q:
#             next = heapq.heappop(q)[1]
#             if gap >= next.duration:
#                 sol.append(next.id)
#                 gap -= next.duration
#             else:
#                 next.duration -= gap
#                 heapq.heappush(q, (next.duration, next))
#                 break
#     return sol


# def solve_greedy_deadline(tasks):
#     tasks = sorted(tasks, key=lambda t: t.deadline)
#     sol = []
#     time = 0
#     while tasks:
#         if time + tasks[0].duration > 1440:
#             del tasks[0]
#             continue
#         sol.append(tasks[0].task_id)
#         time += tasks[0].duration
#         del tasks[0]
#     return sol

# def solve_greedy_profit(tasks):
#     tasks = sorted(tasks, key=lambda t: - t.perfect_benefit)
#     sol = []
#     time = 0
#     while tasks:
#         if time + tasks[0].duration > 1440:
#             del tasks[0]
#             continue
#         sol.append(tasks[0].task_id)
#         time += tasks[0].duration
#         del tasks[0]
#     return sol

# def solve_greedy_ratio(tasks):
#     tasks = sorted(tasks, key=lambda t: -t.perfect_benefit/t.duration + 0.001*t.duration)
#     sol = []
#     time = 0
#     while tasks:
#         if time + tasks[0].duration > 1440:
#             del tasks[0]
#             continue
#         sol.append(tasks[0].task_id)
#         time += tasks[0].duration
#         del tasks[0]
#     return sol


import pickle as pkl
import random

iters = 100
def solve(tasks, input_file):
    if os.path.exists("sols/" + input_file):
        ordering, best = pkl.load(open("sols/" + input_file, "rb"))
    else:
        ordering = solve_heuristic(tasks)
        best = calculate_profit(ordering, tasks)

    current_profit = calculate_profit(ordering, tasks)
    for x in range(iters):
        for i in range(len(tasks)):
            for j in range(i+1, len(tasks)):
                ordering[i], ordering[j] = ordering[j], ordering[i]
                new_profit = calculate_profit(ordering, tasks)
                # print(new_profit, " ", end='')
                if new_profit > current_profit or random.random() < 0.0005:
                    current_profit = new_profit
                else:
                    ordering[i], ordering[j] = ordering[j], ordering[i]

        # if current_profit == last_profit:
        #     pkl.dump(ordering, open("sols/" + input_file, "wb"))
        #     return truncate_ordering(ordering, tasks)
        if current_profit > best:
            pkl.dump((ordering, current_profit), open("sols/" + input_file, "wb"))
            best = current_profit
        print(current_profit, "\t", best, "\t", x)

    return truncate_ordering(ordering, tasks)

def extract(tasks, input_file):
    ordering, best = pkl.load(open("sols/" + input_file, "rb"))
    return truncate_ordering(ordering, tasks)

def truncate_ordering(ordering, tasks):
    time = 0
    for i in range(len(ordering)):
        if time + tasks[ordering[i] - 1].duration > 1440:
            return ordering[:i]
        time += tasks[ordering[i] - 1].duration
    return ordering

def calculate_profit(output, tasks):
    time = 0
    profit = 0
    for id in output:
        task = tasks[id - 1]
        finish = time + task.duration
        if finish <= task.deadline:
            profit += task.perfect_benefit
        else:
            profit += task.perfect_benefit * exp(-0.017 * (finish - task.deadline))
        time += task.duration

        if time > 1440:
            break
    return profit

# Here's an example of how to run your solver.
if __name__ == '__main__':
    total_profit = 0
    n_tests = 0

    for size in os.listdir('inputs/'):
        if size not in ['small', 'medium', 'large']:
            continue
        for input_file in tqdm(os.listdir('inputs/{}/'.format(size))):
            if size not in input_file:
                continue

            # if not (input_file == 'large-300.in'):
            #     continue

            input_path = 'inputs/{}/{}'.format(size, input_file)
            output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
            print(input_path, output_path)
            tasks = read_input_file(input_path)

            output = solve(tasks, input_file)
            # output = extract(tasks, input_file)
            #  output = solve_heuristic(tasks)

            # print(output)

            # print(calculate_profit(output, tasks))
            total_profit += calculate_profit(output, tasks)

            write_output_file(output_path, output)
            n_tests += 1

    print("Total Profit: ", total_profit)
    print("n_tests: ", n_tests)
