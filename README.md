## dash-app
#### Web dashboard application written in Dash and plotly.

Application takes the stock trading operations as input, loads the daily historical prices for the stocks in the portfolio, 
calculates the metrics and shows the respective plots per stock, compares profits and investments of stocks in time, 
shows the metrics in the context of open or closed positions together and separately, and the proportion of the stocks in the portfolio.

*Portal is still in active development phase.*

### Installation:
It is strongly recommended to create a python virtual environment: 
* `python -m venv DashVenv`
Activate virtual environment:
* Mac/Linux: ```source DashVenv/bin/activate```
* Windows: ```DashVenv\Scripts\activate.bat```

### Install the libraries needed for the app:
* ```pip install -r requirements.txt```

### How to run application:
* ```python dash_plotly.py```


#### Known Issues and development under progress:
- Need a refresh of the source data after the user input. Currently, it shows the data correctly only on the next time when server runs.
- Store the state of the user input.
- Moving input functionalities into proper local files, refactor.
- UI input validation
