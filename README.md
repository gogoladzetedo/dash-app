## Financial Stokcs Portfolio Analytics

##### Application lets users to upload the stock market transactions and calculates the metrics accordingly. 

Web dashboard application written in Dash and plotly.

Application takes the stock trading operations as input, loads the daily historical prices for the stocks in the portfolio, 
calculates the metrics and shows the respective plots per stock, compares profits and investments of stocks in time, 
shows the metrics in the context of open or closed positions together and separately, and the proportion of the stocks in the portfolio.
Upload of the transactions can be done either, by manually entering each stock market operation - sell or buy, or by uploading a .csv file that holds these transactions.

[The Application](https://portfolio-dash.azurewebsites.net/) is deployed on Azure web apps.



*Portal is still in active development phase.*

### Installation using docker
If you already have docker installed on your machine, dockerfile needed for the build and run for the application is included in the repository. 
Build the application by running the commands from the dash-app folder:
``` docker build -t portfolio-app-dash . ```
``` docker run -dp 80:80 portfolio-app-dash ```
And browse the application at the localhost:80 address.


### Installation:
It is strongly recommended to create a python virtual environment: 
* ```python -m venv DashVenv```

Activate virtual environment:
* Mac/Linux: ```source DashVenv/bin/activate```
* Windows: ```DashVenv\Scripts\activate.bat```

### Install the libraries needed for the app:
* ```pip install -r requirements.txt```

### How to run application:
* ```python app.py```
Application will run on local machine port 80.

#### Screenshots from the dashboard:
![image 1](/images/image1.png)
![image 2](/images/image2.png)
![image 3](/images/image3.png)
![image 4](/images/image4.png)
![image 5](/images/image5.png)


#### Known Issues and development under progress:
- Improve input data refresh functionality.
- Change the metric tabs to one tab with all the metrics as the option within.
- Store the state of the user input.
- UI input validation
