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
import time as t

iters = 50
def solve(tasks, input_file):
    if os.path.exists("sols/" + input_file):
        ordering, best = pkl.load(open("sols/" + input_file, "rb"))
    else:
        ordering = solve_heuristic(tasks)
        best = calculate_profit(ordering, tasks)
    starting_profit = best

    current_profit = calculate_profit(ordering, tasks)
    for _ in range(iters):
        for i in range(len(tasks)):
            for j in range(i+1, len(tasks)):
                ordering[i], ordering[j] = ordering[j], ordering[i]
                new_profit = calculate_profit(ordering, tasks)
                if new_profit > current_profit or random.random() < 0.0001:
                    current_profit = new_profit
                else:
                    ordering[i], ordering[j] = ordering[j], ordering[i]

        if current_profit > best:
            pkl.dump((ordering, current_profit), open("sols/" + input_file, "wb"))
            best = current_profit

    print("IMPROVEMENT: ", best - starting_profit, "\t", best, "\t", input_file)

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

# @jit
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

from multiprocessing import Process, Pool
    
# Here's an example of how to run your solver.
if __name__ == '__main__':
    total_profit = 0
    n_tests = 0

    pool = Pool(7)
    jobs = []

    for input_file, rank, size in [('large-73.in', 171, 'large'), ('large-263.in', 140, 'large'), ('medium-214.in', 133, 'medium'), ('large-30.in', 133, 'large'), ('large-51.in', 133, 'large'), ('large-292.in', 133, 'large'), ('large-22.in', 132, 'large'), ('medium-97.in', 129, 'medium'), ('large-291.in', 129, 'large'), ('large-38.in', 128, 'large'), ('large-46.in', 128, 'large'), ('large-93.in', 128, 'large'), ('medium-77.in', 127, 'medium'), ('large-39.in', 127, 'large'), ('large-59.in', 127, 'large'), ('large-67.in', 127, 'large'), ('large-98.in', 126, 'large'), ('large-74.in', 125, 'large'), ('large-171.in', 124, 'large'), ('large-238.in', 124, 'large'), ('large-261.in', 124, 'large'), ('large-276.in', 124, 'large'), ('large-26.in', 123, 'large'), ('large-43.in', 123, 'large'), ('large-253.in', 123, 'large'), ('large-287.in', 123, 'large'), ('large-299.in', 123, 'large'), ('large-64.in', 122, 'large'), ('large-68.in', 122, 'large'), ('large-71.in', 122, 'large'), ('large-183.in', 122, 'large'), ('large-41.in', 121, 'large'), ('large-48.in', 121, 'large'), ('large-86.in', 121, 'large'), ('large-36.in', 120, 'large'), ('large-44.in', 120, 'large'), ('large-63.in', 120, 'large'), ('large-87.in', 120, 'large'), ('large-97.in', 120, 'large'), ('large-207.in', 120, 'large'), 
('large-289.in', 120, 'large'), ('small-238.in', 119, 'small'), ('large-92.in', 119, 'large'), ('large-200.in', 119, 'large'), ('large-224.in', 119, 'large'), ('large-298.in', 119, 'large'), ('medium-51.in', 118, 'medium'), ('medium-238.in', 118, 'medium'), ('large-6.in', 118, 'large'), ('large-34.in', 118, 'large'), ('large-66.in', 118, 'large'), ('large-85.in', 118, 'large'), ('large-194.in', 118, 'large'), ('large-50.in', 117, 'large'), ('large-53.in', 117, 'large'), ('large-90.in', 117, 'large'), ('small-263.in', 116, 'small'), ('large-7.in', 116, 'large'), ('large-8.in', 116, 'large'), ('large-223.in', 116, 'large'), 
('large-241.in', 116, 'large'), ('large-269.in', 116, 'large'), ('medium-27.in', 115, 'medium'), ('medium-72.in', 115, 'medium'), ('medium-226.in', 115, 'medium'), ('large-52.in', 115, 'large'), ('large-77.in', 115, 'large'), ('large-81.in', 115, 'large'), ('large-95.in', 115, 'large'), ('large-215.in', 115, 'large'), ('large-232.in', 115, 'large'), ('large-250.in', 115, 'large'), ('large-295.in', 115, 'large'), ('large-296.in', 115, 'large'), ('large-31.in', 114, 'large'), ('large-182.in', 114, 'large'), ('large-234.in', 114, 'large'), ('large-237.in', 114, 'large'), ('large-242.in', 114, 'large'), ('large-283.in', 114, 'large'), ('large-9.in', 113, 'large'), ('large-88.in', 113, 'large'), ('large-91.in', 113, 'large'), ('large-160.in', 113, 'large'), ('large-169.in', 113, 'large'), ('large-225.in', 113, 'large'), ('medium-146.in', 112, 'medium'), ('medium-157.in', 112, 'medium'), ('medium-252.in', 112, 'medium'), ('medium-277.in', 112, 'medium'), ('large-45.in', 112, 'large'), ('large-47.in', 112, 'large'), ('large-61.in', 112, 'large'), ('large-141.in', 112, 'large'), ('large-204.in', 112, 'large'), ('large-264.in', 112, 'large'), ('large-265.in', 112, 'large'), ('large-281.in', 112, 'large'), ('medium-99.in', 111, 'medium'), ('large-20.in', 111, 'large'), ('large-33.in', 111, 'large'), ('large-49.in', 111, 'large'), ('large-58.in', 111, 'large'), ('large-100.in', 111, 'large'), ('small-182.in', 110, 'small'), ('medium-94.in', 110, 'medium'), ('large-3.in', 110, 'large'), ('large-83.in', 110, 'large'), ('large-96.in', 110, 'large'), ('large-161.in', 110, 'large'), ('large-226.in', 110, 'large'), ('medium-91.in', 109, 'medium'), ('medium-108.in', 109, 'medium'), ('large-80.in', 109, 'large'), ('large-173.in', 109, 'large'), ('large-217.in', 109, 'large'), ('large-249.in', 109, 'large'), ('large-251.in', 109, 'large'), ('small-160.in', 108, 'small'), ('large-4.in', 108, 'large'), ('large-37.in', 108, 'large'), ('large-220.in', 108, 'large'), ('large-228.in', 108, 'large'), ('large-236.in', 108, 'large'), ('large-266.in', 108, 'large'), ('large-293.in', 108, 'large'), ('large-297.in', 108, 'large'), ('small-281.in', 107, 'small'), ('medium-59.in', 107, 'medium'), ('medium-169.in', 107, 'medium'), ('medium-205.in', 107, 'medium'), ('large-40.in', 107, 'large'), ('large-60.in', 107, 'large'), ('large-70.in', 107, 'large'), ('large-116.in', 107, 'large'), ('large-125.in', 107, 'large'), ('large-196.in', 107, 'large'), ('small-87.in', 106, 'small'), ('small-88.in', 106, 'small'), ('medium-88.in', 106, 'medium'), ('medium-160.in', 106, 'medium'), ('medium-212.in', 106, 'medium'), ('large-55.in', 106, 'large'), ('large-62.in', 106, 'large'), ('large-94.in', 106, 'large'), ('large-172.in', 106, 'large'), ('large-270.in', 106, 'large'), ('small-66.in', 105, 'small'), ('medium-1.in', 105, 'medium'), ('medium-95.in', 105, 'medium'), ('medium-165.in', 105, 
'medium'), ('large-18.in', 105, 'large'), ('large-24.in', 105, 'large'), ('large-29.in', 105, 'large'), ('large-78.in', 105, 'large'), ('large-84.in', 105, 'large'), ('large-158.in', 105, 'large'), ('large-165.in', 105, 'large'), ('large-186.in', 105, 
'large'), ('large-300.in', 105, 'large'), ('small-151.in', 104, 'small'), ('small-215.in', 104, 'small'), ('medium-17.in', 104, 'medium'), ('medium-56.in', 104, 'medium'), ('medium-82.in', 104, 'medium'), ('medium-92.in', 104, 'medium'), ('medium-260.in', 104, 'medium'), ('large-19.in', 104, 'large'), ('large-32.in', 104, 'large'), ('large-76.in', 104, 'large'), ('large-144.in', 104, 'large'), ('large-231.in', 104, 'large'), ('large-273.in', 104, 'large'), ('large-285.in', 104, 'large'), ('large-286.in', 104, 'large'), ('medium-30.in', 103, 'medium'), ('medium-53.in', 103, 'medium'), ('medium-89.in', 103, 'medium'), ('medium-123.in', 103, 'medium'), ('medium-203.in', 103, 'medium'), ('medium-247.in', 103, 'medium'), ('medium-269.in', 103, 'medium'), ('large-82.in', 103, 'large'), ('large-109.in', 103, 'large'), ('large-170.in', 103, 'large'), ('large-212.in', 103, 'large'), ('large-272.in', 103, 'large'), ('large-294.in', 103, 'large'), ('medium-42.in', 102, 'medium'), ('medium-230.in', 102, 'medium'), ('medium-239.in', 102, 'medium'), ('large-177.in', 102, 'large'), ('large-181.in', 102, 'large'), ('large-205.in', 102, 'large'), ('large-218.in', 102, 'large'), ('large-240.in', 102, 'large'), ('large-274.in', 102, 'large'), ('large-284.in', 102, 'large'), ('small-167.in', 101, 'small'), ('small-231.in', 101, 'small'), ('medium-9.in', 101, 'medium'), ('medium-253.in', 101, 'medium'), ('medium-288.in', 101, 'medium'), ('large-72.in', 101, 'large'), ('large-89.in', 101, 'large'), ('large-153.in', 101, 'large'), ('large-187.in', 101, 'large'), ('large-288.in', 101, 'large'), ('small-8.in', 100, 'small'), ('small-97.in', 100, 'small'), ('small-140.in', 100, 'small'), ('small-216.in', 100, 'small'), ('medium-40.in', 100, 'medium'), ('medium-81.in', 100, 'medium'), ('medium-105.in', 100, 'medium'), ('medium-144.in', 100, 'medium'), ('medium-151.in', 100, 'medium'), ('medium-173.in', 100, 'medium'), ('large-118.in', 100, 'large'), ('large-122.in', 100, 'large'), ('large-128.in', 100, 'large'), ('large-155.in', 100, 'large'), ('large-185.in', 100, 'large'), ('large-209.in', 100, 'large'), ('large-211.in', 100, 'large'), ('large-275.in', 100, 'large'), ('large-279.in', 100, 'large'), ('small-58.in', 99, 'small'), ('small-212.in', 99, 'small'), ('small-260.in', 99, 'small'), ('small-276.in', 99, 'small'), ('medium-4.in', 99, 'medium'), ('medium-11.in', 99, 'medium'), ('medium-80.in', 99, 'medium'), ('medium-86.in', 99, 'medium'), ('medium-125.in', 99, 'medium'), ('medium-141.in', 99, 'medium'), ('medium-150.in', 99, 'medium'), ('medium-196.in', 99, 'medium'), ('medium-204.in', 99, 'medium'), ('medium-231.in', 
99, 'medium'), ('medium-272.in', 99, 'medium'), ('medium-281.in', 99, 'medium'), ('medium-284.in', 99, 'medium'), ('large-13.in', 99, 'large'), ('large-28.in', 99, 'large'), ('large-99.in', 99, 'large'), ('large-145.in', 99, 'large'), ('large-150.in', 
99, 'large'), ('large-154.in', 99, 'large'), ('large-174.in', 99, 'large'), ('large-210.in', 99, 'large'), ('small-78.in', 98, 'small'), ('small-243.in', 98, 'small'), ('small-251.in', 98, 'small'), ('medium-21.in', 98, 'medium'), ('medium-104.in', 98, 'medium'), ('medium-110.in', 98, 'medium'), ('medium-224.in', 98, 'medium'), ('medium-225.in', 98, 'medium'), ('medium-266.in', 98, 'medium'), ('large-11.in', 98, 'large'), ('large-126.in', 98, 'large'), ('large-151.in', 98, 'large'), ('large-162.in', 98, 'large'), ('large-163.in', 98, 'large'), ('large-198.in', 98, 'large'), ('large-239.in', 98, 'large'), ('large-247.in', 98, 'large'), ('large-257.in', 98, 'large'), ('small-37.in', 97, 'small'), ('medium-22.in', 97, 'medium'), ('medium-122.in', 97, 'medium'), ('large-23.in', 97, 'large'), ('large-101.in', 97, 'large'), ('large-127.in', 97, 'large'), ('large-140.in', 97, 
'large'), ('large-206.in', 97, 'large'), ('large-230.in', 97, 'large'), ('large-282.in', 97, 'large'), ('small-53.in', 96, 'small'), ('small-144.in', 96, 'small'), ('small-255.in', 96, 'small'), ('small-272.in', 96, 'small'), ('medium-67.in', 96, 'medium'), ('medium-96.in', 96, 'medium'), ('medium-175.in', 96, 'medium'), ('medium-198.in', 96, 'medium'), ('large-124.in', 96, 'large'), ('large-130.in', 96, 'large'), ('large-147.in', 96, 'large'), ('large-190.in', 96, 'large'), ('large-227.in', 96, 'large'), ('large-246.in', 96, 'large'), ('large-252.in', 96, 'large'), ('small-95.in', 95, 'small'), ('small-113.in', 95, 'small'), ('small-249.in', 95, 'small'), ('medium-10.in', 95, 'medium'), ('medium-74.in', 95, 'medium'), ('medium-168.in', 95, 'medium'), ('medium-176.in', 95, 'medium'), ('medium-191.in', 95, 'medium'), ('medium-206.in', 95, 'medium'), ('medium-227.in', 95, 'medium'), ('medium-229.in', 95, 'medium'), ('medium-270.in', 95, 'medium'), ('medium-271.in', 95, 'medium'), ('large-14.in', 95, 'large'), ('large-25.in', 95, 'large'), ('large-136.in', 95, 'large'), ('large-179.in', 95, 'large'), ('large-258.in', 95, 'large'), ('small-4.in', 94, 'small'), ('small-237.in', 94, 'small'), ('small-286.in', 94, 'small'), ('medium-49.in', 94, 'medium'), ('medium-145.in', 94, 'medium'), ('medium-177.in', 94, 'medium'), ('medium-189.in', 94, 'medium'), ('medium-219.in', 
94, 'medium'), ('medium-223.in', 94, 'medium'), ('medium-279.in', 94, 'medium'), ('medium-299.in', 94, 'medium'), ('medium-300.in', 94, 'medium'), ('large-142.in', 94, 'large'), ('large-189.in', 94, 'large'), ('large-199.in', 94, 'large'), ('large-201.in', 94, 'large'), ('large-202.in', 94, 'large'), ('large-221.in', 94, 'large'), ('large-229.in', 94, 'large'), ('large-244.in', 94, 'large'), ('large-255.in', 94, 'large'), ('large-256.in', 94, 'large'), ('large-268.in', 94, 'large'), ('small-100.in', 93, 'small'), ('small-174.in', 93, 'small'), ('small-278.in', 93, 'small'), ('small-285.in', 93, 'small'), ('small-290.in', 93, 'small'), ('small-291.in', 93, 'small'), ('medium-18.in', 93, 'medium'), ('medium-26.in', 93, 'medium'), ('medium-43.in', 93, 'medium'), ('medium-48.in', 93, 'medium'), ('medium-64.in', 93, 'medium'), ('medium-118.in', 93, 'medium'), ('medium-131.in', 93, 'medium'), ('medium-246.in', 93, 'medium'), ('medium-291.in', 93, 'medium'), ('large-167.in', 93, 'large'), ('large-278.in', 93, 'large'), ('small-9.in', 92, 'small'), ('small-46.in', 92, 'small'), ('small-135.in', 92, 'small'), ('small-225.in', 92, 'small'), ('small-240.in', 92, 'small'), ('small-244.in', 92, 'small'), ('small-274.in', 92, 'small'), ('small-293.in', 92, 'small'), ('medium-20.in', 92, 'medium'), ('medium-28.in', 92, 'medium'), ('medium-36.in', 92, 'medium'), ('medium-41.in', 
92, 'medium'), ('medium-71.in', 92, 'medium'), ('medium-101.in', 92, 'medium'), ('medium-121.in', 92, 'medium'), ('medium-136.in', 92, 'medium'), ('medium-137.in', 92, 'medium'), ('medium-208.in', 92, 'medium'), ('medium-244.in', 92, 'medium'), ('medium-262.in', 92, 'medium'), ('medium-263.in', 92, 'medium'), ('medium-264.in', 92, 'medium'), ('large-15.in', 92, 'large'), ('large-191.in', 92, 'large'), ('large-195.in', 92, 'large'), ('large-197.in', 92, 'large'), ('large-208.in', 92, 'large'), ('large-222.in', 92, 'large'), ('large-233.in', 92, 'large'), ('large-259.in', 92, 'large'), ('small-19.in', 91, 'small'), ('small-44.in', 91, 'small'), ('small-50.in', 91, 'small'), ('small-219.in', 91, 'small'), ('small-230.in', 91, 'small'), ('small-298.in', 91, 'small'), ('medium-8.in', 91, 'medium'), ('medium-39.in', 91, 'medium'), ('medium-44.in', 91, 'medium'), ('medium-107.in', 91, 'medium'), ('medium-138.in', 91, 'medium'), ('medium-140.in', 91, 'medium'), ('medium-186.in', 91, 'medium'), ('medium-241.in', 91, 'medium'), ('medium-258.in', 91, 'medium'), ('medium-289.in', 91, 'medium'), ('large-103.in', 91, 'large'), ('large-106.in', 91, 'large'), ('large-164.in', 91, 'large'), ('large-176.in', 91, 'large'), ('large-193.in', 91, 'large'), ('small-7.in', 90, 'small'), ('small-13.in', 90, 'small'), ('small-86.in', 90, 'small'), ('small-121.in', 90, 'small'), ('small-170.in', 90, 'small'), ('small-204.in', 90, 'small'), ('small-234.in', 90, 'small'), ('small-239.in', 90, 'small'), ('small-284.in', 90, 'small'), ('medium-16.in', 90, 'medium'), ('medium-31.in', 90, 'medium'), ('medium-45.in', 90, 'medium'), ('medium-58.in', 90, 'medium'), ('medium-78.in', 90, 'medium'), ('medium-98.in', 90, 'medium'), ('medium-100.in', 90, 'medium'), ('medium-128.in', 90, 'medium'), ('medium-142.in', 90, 'medium'), ('medium-149.in', 90, 'medium'), ('medium-207.in', 90, 'medium'), ('medium-243.in', 90, 'medium'), ('medium-251.in', 90, 'medium'), ('medium-280.in', 90, 'medium'), ('large-27.in', 90, 'large'), 
('large-149.in', 90, 'large'), ('large-175.in', 90, 'large'), ('large-280.in', 90, 'large'), ('small-6.in', 89, 'small'), ('small-30.in', 89, 'small'), ('small-41.in', 89, 'small'), ('small-47.in', 89, 'small'), ('small-63.in', 89, 'small'), ('small-92.in', 89, 'small'), ('small-132.in', 89, 'small'), ('small-152.in', 89, 'small'), ('small-210.in', 89, 'small'), ('small-228.in', 89, 'small'), ('small-300.in', 89, 'small'), ('medium-15.in', 89, 'medium'), ('medium-25.in', 89, 'medium'), ('medium-50.in', 89, 'medium'), ('medium-87.in', 89, 'medium'), ('medium-119.in', 89, 'medium'), ('medium-143.in', 89, 'medium'), ('medium-159.in', 89, 'medium'), ('medium-187.in', 89, 'medium'), ('medium-294.in', 89, 'medium'), ('large-113.in', 89, 'large'), ('large-148.in', 89, 'large'), ('large-168.in', 89, 'large'), ('large-260.in', 89, 'large'), ('small-173.in', 88, 'small'), ('small-200.in', 88, 'small'), ('small-223.in', 88, 'small'), ('small-226.in', 88, 'small'), ('small-257.in', 88, 'small'), ('small-258.in', 88, 'small'), ('small-259.in', 88, 'small'), ('medium-23.in', 88, 'medium'), ('medium-29.in', 88, 'medium'), ('medium-60.in', 88, 'medium'), ('medium-90.in', 88, 'medium'), ('medium-115.in', 88, 'medium'), ('medium-167.in', 88, 'medium'), ('medium-199.in', 88, 'medium'), ('medium-276.in', 88, 'medium'), ('large-1.in', 88, 'large'), ('large-10.in', 88, 'large'), ('large-104.in', 88, 'large'), ('large-107.in', 88, 'large'), ('large-131.in', 88, 'large'), ('large-235.in', 88, 'large'), ('large-262.in', 88, 'large'), ('small-10.in', 87, 'small'), ('small-84.in', 87, 'small'), ('small-190.in', 87, 'small'), ('small-206.in', 87, 'small'), ('small-264.in', 87, 'small'), ('small-295.in', 87, 'small'), ('medium-52.in', 87, 'medium'), ('medium-66.in', 87, 'medium'), ('medium-70.in', 87, 'medium'), ('medium-76.in', 87, 'medium'), ('medium-120.in', 87, 'medium'), ('medium-216.in', 87, 'medium'), ('medium-236.in', 87, 'medium'), ('medium-274.in', 87, 'medium'), ('medium-278.in', 87, 'medium'), ('large-21.in', 87, 'large'), ('large-114.in', 87, 'large'), ('large-115.in', 87, 'large'), ('large-119.in', 87, 'large'), ('large-123.in', 87, 'large'), ('large-129.in', 87, 'large'), ('small-45.in', 86, 'small'), ('small-49.in', 86, 'small'), ('small-59.in', 86, 'small'), ('small-83.in', 86, 'small'), ('small-104.in', 86, 'small'), ('small-106.in', 86, 'small'), ('small-123.in', 86, 'small'), ('small-149.in', 86, 'small'), ('small-191.in', 86, 'small'), ('medium-6.in', 86, 'medium'), ('medium-7.in', 86, 'medium'), ('medium-38.in', 86, 'medium'), ('medium-61.in', 86, 'medium'), ('medium-152.in', 86, 'medium'), ('medium-215.in', 86, 'medium'), ('medium-222.in', 86, 'medium'), ('medium-234.in', 86, 'medium'), ('medium-250.in', 86, 'medium'), ('medium-297.in', 86, 'medium'), ('small-1.in', 85, 'small'), ('small-93.in', 85, 'small'), ('small-108.in', 85, 'small'), ('small-131.in', 85, 'small'), ('small-183.in', 85, 'small'), ('small-185.in', 85, 'small'), ('small-186.in', 85, 'small'), ('small-218.in', 85, 'small'), ('small-261.in', 85, 'small'), ('small-279.in', 85, 'small'), ('medium-84.in', 85, 'medium'), ('medium-197.in', 85, 'medium'), ('medium-220.in', 85, 'medium'), ('medium-235.in', 85, 'medium'), ('medium-255.in', 85, 'medium'), ('medium-256.in', 85, 'medium'), ('large-17.in', 85, 'large'), ('large-137.in', 85, 'large'), ('large-152.in', 85, 'large'), ('large-157.in', 85, 'large'), ('small-29.in', 84, 'small'), ('small-42.in', 84, 'small'), ('small-136.in', 84, 'small'), ('small-207.in', 84, 'small'), ('small-221.in', 84, 'small'), ('small-292.in', 84, 'small'), ('medium-13.in', 84, 'medium'), ('medium-24.in', 84, 'medium'), ('medium-127.in', 84, 'medium'), ('medium-153.in', 84, 'medium'), ('medium-154.in', 84, 'medium'), ('medium-156.in', 84, 'medium'), ('medium-202.in', 84, 'medium'), ('large-2.in', 84, 'large'), ('large-16.in', 84, 'large'), ('large-156.in', 84, 'large'), ('small-48.in', 83, 'small'), ('small-62.in', 83, 'small'), ('small-70.in', 83, 'small'), ('small-137.in', 83, 'small'), ('small-163.in', 83, 'small'), ('small-202.in', 83, 'small'), ('small-283.in', 83, 'small'), ('medium-113.in', 
83, 'medium'), ('medium-237.in', 83, 'medium'), ('medium-261.in', 83, 'medium'), ('medium-290.in', 83, 'medium'), ('large-135.in', 83, 'large'), ('large-213.in', 83, 'large'), ('small-12.in', 82, 'small'), ('small-68.in', 82, 'small'), ('small-150.in', 82, 'small'), ('small-201.in', 82, 'small'), ('medium-93.in', 82, 'medium'), ('medium-109.in', 82, 'medium'), ('medium-166.in', 82, 'medium'), ('medium-233.in', 82, 'medium'), ('medium-265.in', 82, 'medium'), ('small-3.in', 81, 'small'), ('small-43.in', 81, 'small'), ('small-61.in', 81, 'small'), ('small-188.in', 81, 'small'), ('small-208.in', 81, 'small'), ('small-275.in', 
81, 'small'), ('medium-37.in', 81, 'medium'), ('medium-162.in', 81, 'medium'), ('medium-200.in', 81, 'medium'), ('medium-240.in', 81, 'medium'), ('large-56.in', 81, 'large'), ('large-108.in', 81, 'large'), ('large-134.in', 81, 'large'), ('large-188.in', 81, 'large'), ('large-290.in', 81, 'large'), ('small-115.in', 80, 'small'), ('small-177.in', 80, 'small'), ('small-178.in', 
80, 'small'), ('small-197.in', 80, 'small'), ('small-252.in', 80, 'small'), ('medium-47.in', 80, 'medium'), ('medium-171.in', 
80, 'medium'), ('medium-209.in', 80, 'medium'), ('medium-268.in', 80, 'medium'), ('small-16.in', 79, 'small'), ('small-32.in', 79, 'small'), ('small-71.in', 79, 'small'), ('small-176.in', 79, 'small'), ('small-180.in', 79, 'small'), ('medium-184.in', 79, 'medium'), ('medium-249.in', 79, 'medium'), ('medium-295.in', 79, 'medium'), ('medium-296.in', 79, 'medium'), ('medium-298.in', 79, 'medium'), ('small-14.in', 78, 'small'), ('small-25.in', 78, 'small'), ('small-31.in', 78, 'small'), ('small-76.in', 
78, 'small'), ('small-89.in', 78, 'small'), ('small-109.in', 78, 'small'), ('small-248.in', 78, 'small'), ('medium-63.in', 78, 'medium'), ('medium-126.in', 78, 'medium'), ('medium-148.in', 78, 'medium'), ('medium-172.in', 78, 'medium'), ('medium-228.in', 78, 'medium'), ('large-243.in', 78, 'large'), ('small-125.in', 77, 'small'), ('medium-183.in', 77, 'medium'), ('large-214.in', 77, 'large'), ('small-56.in', 76, 'small'), ('small-82.in', 76, 'small'), ('small-107.in', 76, 'small'), ('small-232.in', 
76, 'small'), ('small-241.in', 76, 'small'), ('medium-46.in', 76, 'medium'), ('medium-114.in', 76, 'medium'), ('small-147.in', 75, 'small'), ('small-282.in', 75, 'small'), ('small-296.in', 75, 'small'), ('large-12.in', 75, 'large'), ('large-121.in', 75, 'large'), ('large-271.in', 75, 'large'), ('large-277.in', 75, 'large'), ('small-20.in', 74, 'small'), ('small-27.in', 74, 'small'), ('small-101.in', 74, 'small'), ('small-130.in', 74, 'small'), ('small-209.in', 74, 'small'), ('small-247.in', 74, 'small'), ('medium-3.in', 74, 'medium'), ('medium-194.in', 74, 'medium'), ('medium-232.in', 74, 'medium'), ('large-120.in', 74, 'large'), ('small-155.in', 73, 'small'), ('small-198.in', 73, 'small'), ('medium-32.in', 73, 'medium'), ('medium-33.in', 73, 'medium'), ('medium-158.in', 73, 'medium'), ('medium-179.in', 73, 'medium'), ('large-35.in', 73, 'large'), ('large-54.in', 73, 'large'), ('small-51.in', 72, 'small'), ('small-220.in', 72, 'small'), ('large-138.in', 72, 'large'), ('small-40.in', 71, 'small'), ('small-90.in', 71, 'small'), ('small-165.in', 71, 'small'), ('small-268.in', 71, 'small'), ('medium-106.in', 71, 'medium'), ('medium-163.in', 71, 'medium'), ('medium-164.in', 71, 'medium'), ('large-143.in', 71, 'large'), ('medium-35.in', 70, 'medium'), ('medium-174.in', 70, 'medium'), ('large-166.in', 70, 'large'), ('medium-19.in', 69, 'medium'), ('medium-170.in', 69, 'medium'), ('medium-210.in', 69, 'medium'), ('small-166.in', 68, 'small'), ('medium-129.in', 68, 'medium'), ('medium-218.in', 68, 'medium'), ('small-39.in', 67, 'small'), ('small-169.in', 67, 'small'), ('medium-130.in', 67, 'medium'), ('medium-193.in', 67, 'medium'), ('small-222.in', 66, 'small'), ('small-229.in', 66, 'small'), ('medium-2.in', 66, 'medium'), ('large-267.in', 66, 'large'), ('small-38.in', 65, 'small'), ('small-52.in', 65, 'small'), ('small-189.in', 65, 'small'), ('small-273.in', 65, 'small'), ('medium-103.in', 65, 'medium'), ('medium-190.in', 65, 'medium'), ('medium-275.in', 65, 'medium'), ('small-158.in', 64, 'small'), ('small-280.in', 64, 'small'), ('medium-147.in', 64, 'medium'), ('medium-201.in', 64, 'medium'), ('large-42.in', 64, 'large'), ('large-105.in', 64, 'large'), ('small-55.in', 63, 'small'), ('small-194.in', 63, 'small'), ('small-2.in', 62, 'small'), ('small-110.in', 62, 'small'), ('small-118.in', 62, 'small'), ('small-129.in', 62, 'small'), ('small-142.in', 62, 'small'), ('small-171.in', 62, 'small'), ('small-246.in', 62, 'small'), ('medium-161.in', 62, 'medium'), ('medium-257.in', 62, 'medium'), ('medium-282.in', 62, 'medium'), ('large-117.in', 62, 'large'), ('large-133.in', 62, 'large'), ('small-116.in', 61, 'small'), ('small-127.in', 61, 'small'), ('small-193.in', 61, 'small'), ('small-299.in', 61, 'small'), ('medium-14.in', 61, 'medium'), ('medium-133.in', 61, 'medium'), ('medium-185.in', 61, 'medium'), ('large-184.in', 61, 'large'), ('large-248.in', 61, 'large'), ('small-143.in', 60, 'small'), ('small-162.in', 60, 'small'), ('small-256.in', 60, 'small'), ('small-265.in', 60, 'small'), ('medium-68.in', 60, 'medium'), ('medium-283.in', 60, 'medium'), ('large-79.in', 60, 'large'), ('small-94.in', 59, 'small'), ('small-146.in', 59, 'small'), ('small-203.in', 59, 'small'), ('medium-34.in', 59, 'medium'), ('medium-242.in', 59, 'medium'), ('small-23.in', 58, 'small'), ('small-34.in', 58, 'small'), ('small-253.in', 58, 'small'), ('small-270.in', 58, 'small'), ('medium-12.in', 58, 'medium'), ('medium-195.in', 58, 'medium'), ('medium-285.in', 58, 'medium'), ('large-203.in', 58, 'large'), ('large-216.in', 58, 'large'), ('small-117.in', 57, 'small'), ('small-120.in', 57, 'small'), ('medium-217.in', 57, 'medium'), ('medium-293.in', 57, 'medium'), ('large-219.in', 57, 'large'), ('small-35.in', 56, 'small'), ('small-91.in', 56, 'small'), ('small-126.in', 56, 'small'), ('small-271.in', 56, 'small'), ('small-288.in', 56, 'small'), ('medium-124.in', 56, 'medium'), ('medium-287.in', 56, 'medium'), ('small-64.in', 55, 'small'), ('small-199.in', 55, 'small'), ('small-294.in', 55, 'small'), ('small-15.in', 54, 'small'), ('small-141.in', 54, 'small'), ('small-159.in', 54, 'small'), ('small-161.in', 54, 'small'), 
('small-277.in', 54, 'small'), ('small-287.in', 54, 'small'), ('medium-55.in', 54, 'medium'), ('small-98.in', 53, 'small'), ('small-122.in', 53, 'small'), ('small-195.in', 53, 'small'), ('medium-62.in', 53, 'medium'), ('medium-116.in', 53, 'medium'), ('medium-188.in', 53, 'medium'), ('small-11.in', 52, 'small'), ('small-103.in', 52, 'small'), ('small-156.in', 52, 'small'), ('small-17.in', 51, 'small'), ('large-102.in', 51, 'large'), ('small-22.in', 50, 'small'), ('medium-135.in', 50, 'medium'), ('medium-221.in', 50, 'medium'), ('small-24.in', 49, 'small'), ('small-196.in', 49, 'small'), ('small-33.in', 48, 'small'), ('small-289.in', 48, 'small'), ('small-105.in', 47, 'small'), ('small-148.in', 47, 'small'), ('small-154.in', 47, 'small'), ('medium-178.in', 47, 'medium'), ('small-80.in', 46, 'small'), ('small-134.in', 46, 'small'), ('small-138.in', 46, 'small'), ('medium-83.in', 46, 'medium'), ('small-18.in', 45, 'small'), ('small-67.in', 45, 'small'), ('small-114.in', 45, 'small'), ('medium-155.in', 45, 'medium'), ('large-65.in', 45, 'large'), ('large-146.in', 45, 'large'), ('small-242.in', 44, 'small'), ('small-269.in', 44, 'small'), ('small-36.in', 43, 'small'), ('small-224.in', 43, 'small'), ('small-236.in', 43, 'small'), ('medium-73.in', 43, 'medium'), ('medium-134.in', 43, 'medium'), ('small-124.in', 42, 'small'), ('small-128.in', 42, 'small'), ('small-205.in', 42, 'small'), ('small-214.in', 42, 'small'), ('small-157.in', 41, 'small'), ('small-235.in', 41, 'small'), ('medium-213.in', 41, 'medium'), ('large-159.in', 41, 'large'), ('small-153.in', 39, 'small'), ('large-110.in', 38, 'large'), ('small-112.in', 
37, 'small'), ('large-112.in', 35, 'large'), ('small-26.in', 34, 'small'), ('medium-117.in', 34, 'medium'), ('large-180.in', 34, 'large'), ('small-60.in', 33, 'small'), ('small-73.in', 33, 'small'), ('small-262.in', 33, 'small'), ('small-72.in', 32, 'small'), ('small-81.in', 32, 'small'), ('medium-248.in', 32, 'medium'), ('medium-273.in', 31, 'medium'), ('small-79.in', 30, 'small'), ('small-145.in', 30, 'small'), ('small-119.in', 29, 'small'), ('small-65.in', 27, 'small'), ('medium-259.in', 26, 'medium'), ('small-175.in', 25, 'small'), ('small-187.in', 25, 'small'), ('large-178.in', 25, 'large'), ('small-69.in', 24, 'small'), ('small-233.in', 22, 'small'), ('medium-112.in', 22, 'medium'), ('medium-211.in', 22, 'medium'), ('medium-65.in', 21, 'medium'), ('small-21.in', 19, 'small'), ('small-213.in', 19, 'small'), ('small-102.in', 18, 'small'), ('small-211.in', 18, 'small'), ('small-133.in', 15, 'small'), ('medium-102.in', 14, 'medium'), ('small-28.in', 13, 'small'), ('medium-54.in', 13, 'medium'), ('medium-286.in', 12, 'medium'), ('medium-180.in', 10, 'medium'), ('small-5.in', 1, 'small'), ('small-54.in', 1, 'small'), ('small-57.in', 1, 'small'), ('small-74.in', 1, 'small'), ('small-75.in', 1, 'small'), ('small-77.in', 1, 'small'), ('small-85.in', 1, 'small'), ('small-96.in', 1, 'small'), ('small-99.in', 1, 'small'), ('small-111.in', 1, 'small'), ('small-139.in', 1, 'small'), ('small-164.in', 1, 'small'), ('small-168.in', 1, 'small'), ('small-172.in', 1, 'small'), ('small-179.in', 1, 'small'), ('small-181.in', 1, 'small'), ('small-192.in', 1, 'small'), ('small-217.in', 1, 'small'), ('small-227.in', 1, 'small'), 
('small-245.in', 1, 'small'), ('small-250.in', 1, 'small'), ('small-254.in', 1, 'small'), ('small-266.in', 1, 'small'), ('small-267.in', 1, 'small'), ('small-297.in', 1, 'small'), ('medium-5.in', 1, 'medium'), ('medium-57.in', 1, 'medium'), ('medium-69.in', 1, 'medium'), ('medium-75.in', 1, 'medium'), ('medium-79.in', 1, 'medium'), ('medium-85.in', 1, 'medium'), ('medium-111.in', 1, 'medium'), ('medium-132.in', 1, 'medium'), ('medium-139.in', 1, 'medium'), ('medium-181.in', 1, 'medium'), ('medium-182.in', 1, 'medium'), ('medium-192.in', 1, 'medium'), ('medium-245.in', 1, 'medium'), ('medium-254.in', 1, 'medium'), ('medium-267.in', 1, 'medium'), ('medium-292.in', 1, 'medium'), ('large-5.in', 1, 'large'), ('large-57.in', 1, 'large'), ('large-69.in', 1, 'large'), ('large-75.in', 1, 'large'), ('large-111.in', 1, 'large'), ('large-132.in', 1, 'large'), ('large-139.in', 1, 'large'), ('large-192.in', 1, 'large'), ('large-245.in', 1, 'large'), ('large-254.in', 1, 'large')]:
        input_path = 'inputs/{}/{}'.format(size, input_file)
        output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
        tasks = read_input_file(input_path)
        print(input_path, output_path)
        # solve(tasks, input_file)
        jobs.append(pool.apply_async(solve, (tasks, input_file)))
        n_tests += 1

    # for size in reversed(os.listdir('inputs/')):
    #     if size not in ['small', 'medium', 'large']:
    #         continue
    #     for input_file in (os.listdir('inputs/{}/'.format(size))):
    #         if size not in input_file:
    #             continue

    #         input_path = 'inputs/{}/{}'.format(size, input_file)
    #         output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
    #         tasks = read_input_file(input_path)
    #         print(input_path, output_path)
    #         # solve(tasks, input_file)
    #         jobs.append(pool.apply_async(solve, (tasks, input_file)))
    #         n_tests += 1

    [job.wait() for job in jobs]
    pool.close()
    pool.join()
    print("Total Profit: ", total_profit)
    print("n_tests: ", n_tests)
