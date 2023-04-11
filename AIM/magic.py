import argparse
import random
import time


def evaluate(x, n, M):
    obj = 0
    for i in range(n):
        row_sum = 0
        col_sum = 0
        for j in range(n):
            row_sum += x[i*n+j]
            col_sum += x[j*n+i]
        obj += abs(row_sum - M) + abs(col_sum - M)
    diag_sum1 = 0
    diag_sum2 = 0
    for i in range(n):
        diag_sum1 += x[i*n+i]
        diag_sum2 += x[i*n+(n-i-1)]
    obj += abs(diag_sum1 - M) + abs(diag_sum2 - M)
    return obj


def generate_initial_solution(N, n):
    x = [-1] * (n*n)
    for i in range(n):
        for j in range(n):
            while True:
                value = random.choice(N)
                if N.count(value) == 1:
                    x[i*n+j] = value
                    N.remove(value)
                    break
    return x


def generate_neighbourhood(x, n, k):
    neighbours = []
    for i in range(k):
        for j in range(i+1, k):
            x_new = x.copy()
            x_new[i], x_new[j] = x_new[j], x_new[i]
            neighbours.append(x_new)
    return neighbours



def variable_neighborhood_search(n, M, N, max_time):
    best_x = None
    best_obj = float('inf')
    start_time = time.time()
    current_time = start_time
    
    # generate initial solution
    x = generate_initial_solution(N, n)
    current_obj = evaluate(x, n, M)
    best_x = x
    best_obj = current_obj
    
    # loop until reaching the maximum time limit
    while current_time - start_time < max_time:
        for k in range(2, n+1):
            neighbourhood = generate_neighbourhood(x, n, k)
            for x_new in neighbourhood:
                obj_new = evaluate(x_new, n, M)
                if obj_new < current_obj:
                    x = x_new
                    current_obj = obj_new
                    if current_obj < best_obj:
                        best_x = x_new
                        best_obj = current_obj
        current_time = time.time()
    
     # check if the current best solution is different from the previous best solution
        if prev_best_x is None or best_x != prev_best_x:
            f.write(str(best_obj) + "\n")
            f.write(" ".join(map(str, best_x)) + "\n")
            prev_best_x = best_x
        
    return best_x, best_obj


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', required=True, help='Input file')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    parser.add_argument('-t', '--time', required=True, type=int, help='Maximum running time in seconds')
    args = parser.parse_args()

    # read input file
    with open(args.source) as f:
        # read the total number of problems
        num_problems = int(f.readline())
        
        # read each problem one by one
        problems = []
        for i in range(num_problems):
            line = f.readline().split()
            n = int(line[0])
            M = int(line[1])
            N = list(map(int, f.readline().split()))
            problems.append((n, M, N))

# solve each problem and write results to file
    with open(args.output, "w") as f:
        f.write(str(num_problems) + "\n")
        for i, problem in enumerate(problems):
            n, M, N = problem
            start_time = time.time()
            x = generate_initial_solution(N, n)
            current_obj = evaluate(x, n, M)
            best_x = x
            best_obj = current_obj
            last_best_obj = None
            f.write(str(best_obj) + "\n")
            f.write(" ".join(map(str, best_x)) + "\n")
            while time.time() - start_time < 100:
                for k in range(2, n+1):
                    neighbourhood = generate_neighbourhood(x, n, k)
                    for x_new in neighbourhood:
                        obj_new = evaluate(x_new, n, M)
                        if obj_new < current_obj:
                            x = x_new
                            current_obj = obj_new
                            if current_obj < best_obj:
                                best_x = x_new
                                best_obj = current_obj
                                # check if the new best objective value is different from the previous one
                                if last_best_obj != best_obj:
                                    f.write(str(best_obj) + "\n")
                                    f.write(" ".join(map(str, best_x)) + "\n")
                                last_best_obj = best_obj
            print(f"Problem {i+1} done. Best objective value found: {best_obj}.")
            
print("All problems solved.")
