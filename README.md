# CenturyPy

CenturyPy is a Python library for training and running the Century (Soil Organic Matter) model. For mor information about Century, take a look at this [link](https://www2.nrel.colostate.edu/projects/irc/public/Documents/Software/Century5/Reference/html/Century/cent5-overview.htm).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install centurypy.

```bash
pip install centurypy
```

## Usage

```python
from centurypy import CenturyPy

# define model
model = CenturyPy('./data.csv',{
    "necromasa": 2140,
    "acto": 50.04,
    "leno": 2250,
    "paso": 19150,
    "respo": 0,
    "ln": 0.33,
    "frala": 0.33,
})

# begin training
model.fit_model()

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## Author

This library was developed by Gerardo Vivas. Any questions about it have no doubt in contact me by email <vivas.fermin24@gmail.com>

## License

[MIT](https://choosealicense.com/licenses/mit/)