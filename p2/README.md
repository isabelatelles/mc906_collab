## Files

### create_dataset.py
Execution:
    python3 create_dataset.py

It creates a dataset based on the internal variables "n_children" and "n_gift_type". To change the size of the dataset, these variables must be modified at the base code.

### genetic_algorithm.py
Execution:
    python3 genetic_algorithm.py
    
It runs the algorithm based on the internal variables "population_size", "max_generation" and "mutation_rate", besides "n_children" and "n_gift_type". To change the dataset, these variables must be modified at the base code. Also, the dataset needs to exist and be at dataset/ folder.

### fitness_function.py
It holds a class that calculates the fitness function of the problem.

### modeling.py
It contains the modeling of the problem, including the crossover and mutation methods.

### plot.py
It plots a graph based on the best, worst and average individual of each generation of the algorithm.

### results folders
Each folder "cN_gM" represents the results of the algorithm when it was run with the configuration of N children and M gift types.

The result files are the following:
* best_ind: a .txt file with the representation of the best individual reached
* output: a .txt file with the output generated while the algorithm was running, with the number of the generation and the score of its best individual.
* graph: a .png file with the graph of scores x generation