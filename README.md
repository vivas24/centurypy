# CenturyPy

CenturyPy is a Python library for training and running the Century (Soil Organic Matter) model. For more information about Century, take a look at this [link](https://www2.nrel.colostate.edu/projects/irc/public/Documents/Software/Century5/Reference/html/Century/cent5-overview.htm).

This is the first version of the library and only simulates the dynamic for the carbon. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install centurypy.

```bash
pip install centurypy
```

## Usage

```python
from centurypy import CenturyPy

# define the model, the first parameter is the file with the samples's data.
# the second parameter is a dictionary containing the initial conditions 
# from where the samples were taken
model = CenturyPy('./data.csv',{
    "necromasa": 2140,  # Necromass
    "acto": 50.04,      # Initial value for the Active container
    "leno": 2250,       # Initial value for the Slow container
    "paso": 19150,      # initial value for the Pasive container
    "respo": 0,         # initial value for the Respiration
    "ln": 0.33,         # Lignin
    "frala": 0.33,      # Fine soil fraction
})


# begin training, default 500 generations
model.fit_model()

# in case you want more precission, you can define 
# the number of generations using an integer
model.fit_model(1000)

# or using the parameter's name
model.fit_model(generations = 1000)

# by default, the library draws a chart containing the result of the training, in case you 
# don't want to show that chart, you can disable it using the second parameter as follows
model.fit_model(generations = 500, chart = False)

```

The supported intput's file format is colon separated CSV (,). The content of that file must be the sample's data without the headers.
It must have only three columns, the first one represents the time when the sample was taken, the second one represents the value for the active container and the last one represents the value for the
respiration. 

An example is shown bellow: 

```
     1, 243, 118.52
     2, 192, 512.245
     3, 240, 840.725
     4, 235, 1396.19
     5, 314, 1895.14625
     8, 241, 2195.29625
    11, 213, 2509.59625
    18, 185, 2892.02125
    25, 177, 3147.39625
    30, 114, 3203.66125

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## Author

This library was developed by Gerardo Vivas. Any questions about it have no doubt in contact me by email <vivas.fermin24@gmail.com>

## License

[MIT](https://choosealicense.com/licenses/mit/)