import numpy as np
import time
import sys
import os

class Genetic:
    
    
    def __init__(self, century_model, time_data, training_data):
        self.century_model = century_model
        self.time_data = time_data
        self.training_data = training_data
        self.population_size = 200
        self.selection_rate = 0.3
        self.mutation_rate  = 0.01
        self.gen_len = 3
        self.n_params = 13
        self.generation = 0
        self.error = sys.maxsize
        self.start_time = time.time()
        self.population = []
        self.milestones = []
        self.fitness = []
        self.generate_population()


    def mse(self, parameters):
        model_data = self.century_model.resolve(self.time_data, parameters)
        max_value = 0
        for i in [0,1]:
            values_model = model_data[i]
            values_training = self.training_data[i]
            sum = 0
            for j in range(len(values_model)):
                sum += (values_model[j] - values_training[j]) ** 2
            avg = (sum / len(values_model))
            if(avg > max_value):
                max_value = avg
        return round(max_value)

    def generate_population(self):
        for i in range(self.population_size):
            child = list(np.random.rand(self.n_params))
            self.population.append(child)

    def mutate(self):
        for i in range(len(self.population)):
            child = self.population[i]
            if np.random.random() < self.mutation_rate:
                gen = list(np.random.rand(self.gen_len))
                index = np.random.randint(len(child) - self.gen_len + 1)
                child = child[0:index] + gen + child[index + self.gen_len:]
            self.population[i] = child

    def evaluate_population(self):
        fitness_tmp = []
        for child in self.population:
            y = self.mse(child)
            fitness_tmp += [y]
        self.fitness = np.array(fitness_tmp)

    def update_error(self):
        fitness_sorted = sorted(self.fitness)
        error = fitness_sorted[0]
        if(error < self.error and error >= 0):
            self.error = error
            self.milestones.append([self.generation, self.error])

    def choose_parents(self):
        fitness_tmp = []
        population_tmp = []
        for i in range(int(self.population_size * self.selection_rate)):
            index = np.random.choice(self.population_size)
            fitness_tmp.append(self.fitness[index])
            population_tmp.append(self.population[index])
        parents = [x for _,x in sorted(zip(fitness_tmp,population_tmp))]
        return (parents[0],parents[1])

    def select_offspring(self):
        offspring = []
        for i in range(self.population_size//2):
            parents =  self.choose_parents()
            cross_point = np.random.randint(self.n_params)
            offspring += [ parents[0][:cross_point] + parents[1][cross_point:] ]
            offspring += [ parents[1][:cross_point] + parents[0][cross_point:] ]
        return offspring


    def evolve(self, generations):
        for _ in range(generations):
            self.evaluate_population()
            self.update_error()
            self.population = self.select_offspring()
            self.mutate()
            self.print_status()
            self.generation += 1
        self.print_status(True)

    def format_time(self, seconds):
        hh = int(seconds // 3600)
        mm = int((seconds - (hh * 3600)) // 60)
        ss = int((seconds - (hh * 3600) - (mm * 60)))
        return f'{ "0" if hh < 10 else "" }{hh}:{"0" if mm < 10 else ""}{mm}:{"0" if ss < 10 else ""}{ss}'

    def print_status(self,done = False):
        time_formatted = self.format_time(time.time() - self.start_time)
        error_str = '{}'.format(self.error).rjust(10," ")
        if done: 
            print(f'DONE! => time: {time_formatted}, generation: {self.generation}, error: {error_str}')     
        else:
            print(f'time: {time_formatted}, generation: {self.generation}, error: {error_str}', end='\r') 


    def solution(self):
        index = -1
        min_value = sys.maxsize
        for i in range(len(self.population)):
            child = self.population[i]
            value = self.mse(child)
            if value < min_value:
                min_value = value
                index = i
        return self.population[index]
