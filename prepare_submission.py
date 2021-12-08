
import sys
import os
import json
from parse import read_input_file, write_output_file
import pickle as pkl
from solver import truncate_ordering, calculate_profit

def extract(tasks, input_file):
    try:
        ordering, best = pkl.load(open("sols/" + input_file, "rb"))
        return truncate_ordering(ordering, tasks)
    except:
        return [1]

if __name__ == '__main__':

    total_profit = 0
    n_tests = 0
    for size in os.listdir('inputs/'):
        if size not in ['small', 'medium', 'large']:
            continue
        for input_file in os.listdir('inputs/{}/'.format(size)):
            if size not in input_file:
                continue

            input_path = 'inputs/{}/{}'.format(size, input_file)
            output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
            # print(input_path, output_path)
            tasks = read_input_file(input_path)

            output = extract(tasks, input_file)

            # print(calculate_profit(output, tasks))
            total_profit += calculate_profit(output, tasks)
            write_output_file(output_path, output)
            n_tests += 1
    print("Total Profit: ", total_profit)
    print("n_tests: ", n_tests)


    outputs_dir = sys.argv[1]
    submission_name = sys.argv[2]
    submission = {}
    for folder in os.listdir("inputs"):
        if not folder.startswith('.'):
            for input_path in os.listdir("inputs/" + folder):
                graph_name = input_path.split('.')[0]
                output_file = f'{outputs_dir}/{folder}/{graph_name}.out'
                if os.path.exists(output_file):
                    output = open(f'{outputs_dir}/{folder}/{graph_name}.out').read()
                    submission[input_path] = output
    with open(submission_name, 'w') as f:
        f.write(json.dumps(submission))