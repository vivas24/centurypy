import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os.path
from centurypy.century import Century
from centurypy.genetic import Genetic

class  CenturyPy:

    def __init__(self, input_file,  input_values):
        if not self.__check_input_file(input_file):
           raise Exception("Input file not found")
        if not self.__check_input_values(input_values):
           raise Exception("Wrong input values format")
        self.params_name = ['Kmet', 'Kest', 'Kminl', 'Khumac', 'Kminp', 'ResEL', 
                            'ResEA', 'ResMet', 'ResLA', 'ResPA', 'PartEst', 'PartLen','PartAct']
        self.fitted_params = []
        self.training_data = []
        self.time_data = []
        self.century_model = None
        self.genetic_model = None
        self.__load_input_file(input_file)
        self.__load_century_model(input_values)
        self.__load_genetic_model()
        
    def __check_input_file(self, input_file):
        return os.path.isfile(input_file)

    def __check_input_values(self, input):
        if not type(input) is dict: 
            return False
        if input.get('necromasa') == None:
            return False
        if input.get('ln') == None:
            return False
        if input.get('frala') == None:
            return False
        if input.get('leno') == None:
            return False
        if input.get('paso') == None:
            return False
        if input.get('acto') == None:
            return False
        if input.get('respo') == None:
            return False
        return True

    def __load_input_file(self, input_file):
        df = pd.read_csv(input_file,header=None)
        array = df.to_numpy()
        self.training_data = (array[:,1][:],array[:,2][:])
        self.time_data = array[:,0][:]

    def __load_century_model(self,input_values):
        self.century_model = Century([
            input_values['necromasa'],
            input_values['ln'],
            input_values['frala'],
            input_values['leno'],
            input_values['paso'],
            input_values['acto'],
            input_values['respo'],
        ])

    def __load_genetic_model(self):
        self.genetic_model = Genetic(self.century_model,
                                     self.time_data,
                                     self.training_data)

    def fit_model(self, generations = 500, chart = False):
        self.genetic_model.evolve(generations)
        self.fitted_params = self.genetic_model.solution()
        self.__save_parameters()
        self.__display_parameters()
        if chart:
            self.__display_fitted_chart()

    def __save_parameters(self):
        f = open("parameters.txt","w")
        for i in range(len(self.fitted_params)):
            f.write(f'{self.params_name[i]}: {self.fitted_params[i]}\n')
        f.close()

    def __display_parameters(self):
        print('+++++++++++++++++++++++++++++++++++++++++++++++')
        print('+++++++++++++++ PARAMETERS ++++++++++++++++++++')
        for i in range(len(self.fitted_params)):
            param_name = self.params_name[i]
            print(f'{param_name.rjust(10," ")}: {self.fitted_params[i]}')
        print('+++++++++++++++++++++++++++++++++++++++++++++++')

    def __display_fitted_chart(self):
        generations, error = zip(*self.genetic_model.milestones)
        solution = self.century_model.resolve(self.time_data, self.fitted_params )
        fig, axes = plt.subplots(2,1)
        colors = ['b','r']
        names = ['Active','Respiration']
        for i in [0,1]:
            name = names[i]
            color = colors[i]
            axes[0].plot(self.time_data,
                         self.training_data[i],
                         f'{color}.' , 
                         label = f'{name} (Original)')
            axes[0].plot(self.time_data,
                         solution[i],
                         f'{color}-' , 
                         label = f'{name} (Solution)')
        axes[0].set(xlabel='Time',ylabel='C(mg)')
        axes[0].legend()
        axes[1].plot(generations,error,'b.-')
        axes[1].set(xlabel='Generations',ylabel='Error (MSE)')
        plt.show()

    def predict_values(self, day, chart = True):
        if int(day) < 0:
           raise Exception("Day must be a positive number")
        time_data = np.linspace(0,day,dtype=int)
        solution_data = self.century_model.resolve(time_data, self.fitted_params)      
        if(chart):
            self.__display_prediction_chart(time_data, solution_data)
        else:
            self.__display_prediction_values(time_data,solution_data)

    def __display_prediction_chart(self,time,data):
        fig = plt.subplot()
        colors = ['b','r']
        names = ['Active','Respiration']
        for i in [0,1]:
            name = names[i]
            color = colors[i]
            fig.plot(time,
                        data[i],
                        f'{color}.')
            fig.plot(time,
                        data[i],
                        f'{color}-' , 
                        label = f'{name}')
        fig.set(xlabel='Time',ylabel='C(mg)')
        fig.legend()
        plt.show()

    def __display_prediction_values(self,time,data):
        print('+++++++++++++++++++++++++++++++++++++++++++++++')
        print('++++++++++++++++ SOLUTION +++++++++++++++++++++')
        rows = zip(time,data[0],data[1])
        active_label = 'Active'
        respiration_label = 'Respiration'
        for row in rows:
            print(f'Day {row[0]}:')
            print(f'{active_label.rjust(15," ")}: {"{:.2f}".format(row[1])}')
            print(f'{respiration_label.rjust(15," ")}: {"{:.2f}".format(row[2])}')
            print()
        print('+++++++++++++++++++++++++++++++++++++++++++++++')

        
