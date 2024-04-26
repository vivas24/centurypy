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
        self.century_model = Century(
            Necromasa = input_values['necromasa'], 
            ACTo=input_values['acto'], 
            LENo=input_values['leno'], 
            PASo=input_values['paso'], 
            RESPo= input_values['respo'] , 
            LN= input_values['ln'], 
            FraLA= input_values['frala']
        )

    def __load_genetic_model(self):
        self.genetic_model = Genetic(self.century_model,
                                     self.time_data,
                                     self.training_data)

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

    def __display_chart(self):
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

    def fit_model(self, generations = 500, chart = False):
        self.genetic_model.evolve(generations)
        self.fitted_params = self.genetic_model.solution()
        self.__save_parameters()
        self.__display_parameters()
        if chart:
            self.__display_chart()

    def predict_values(self, day, chart = True):
        time_data = np.linspace(0,day)
        solution = self.century_model.resolve(time_data, self.fitted_params)
        if(chart):
            fig = plt.subplot()
            colors = ['b','r']
            names = ['Active','Respiration']
            for i in [0,1]:
                name = names[i]
                color = colors[i]
                fig.plot(time_data,
                            solution[i],
                            f'{color}-' , 
                            label = f'{name}')
            fig.set(xlabel='Time',ylabel='C(mg)')
            fig.legend()
            plt.show()

