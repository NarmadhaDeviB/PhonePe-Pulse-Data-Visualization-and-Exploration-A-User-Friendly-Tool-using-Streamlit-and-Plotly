# PhonePe-Pulse-Data-Visualization-and-Exploration-A-User-Friendly-Tool-using-Streamlit-and-Plotly


### Problem Statement
  To Extract the data from the PhonePe Pulse Github respository through scripting and clone it.  And then transform the data and perform the pre-processing steps. After the process insert the data to MySQL database and Create a live geo visualization dashboard using Stremlit and Plotly and fetch the database from the MySQL database to dispaly it. And give atlest 10 different dropdown for the users to select the facts and understand the Data.

### Skills take way
  1. Python
  2. MySQL
  3. Streamlit
  4. Plotly

### Workflow
#### Step 1:
**Inserting the Necessary Library**

  To insert the Necessary library, first import the library, if not the library is imported then just install the library by using below code.
        
        
        !pip install [library name].
        
  Here I have imported the libraries by using the below code.
        
        import os
        import json
        import pandas as pd
        import mysql.connector as sql
        import streamlit as st
        import plotly.express as px

#### Step 2:
**Data Extraction from Github Respository**

  In this project the data has been extracted from the Github respository through scripting and clone the data.

        !git clone [Give the Github clone URL]


#### Step 3:
**Data Transformation**

  In this step, first we will convert the json file from the data into a DataFrame. To perform this step we have used **os**, **json** and **pandas**. And converted the dataframe into CSV file and storing it in the local device.  

        path1 = "json path from the local device"
        Agg_state_list=os.listdir(path1)
        column1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],
            'Transaction_amount': []}
        for state in Agg_state_list:
            new_state = path1 + state + "/"
            Agg_year_list = os. listdir(new_state)
        
            for year in Agg_year_list:
                new_year = new_state + year + '/'
                Agg_js_list = os. listdir(new_year)
        
                for js in Agg_js_list:
                    new_js = new_year + js
                    data = open(new_js, 'r')
                    D = json.load(data)
                    for z in D['data']['transactionData']:
                      Name=z['name']
                      count=z['paymentInstruments'][0]['count']
                      amount=z['paymentInstruments'][0]['amount']
                      column1['Transaction_type'].append(Name)
                      column1['Transaction_count'].append(count)
                      column1['Transaction_amount'].append(amount)
                      column1['State'].append(state)
                      column1['Year'].append(year)
                      column1['Quarter'].append(int(js.strip('.json')))

          Agg_tran=pd.DataFrame(column1)

  
**Converting the DataFrame to CSV file**

        Agg_tran.to_csv('Agg_tran_path1.csv')


#### Step 4:
**Insering the CSV file into the Database**

  After converting the dataframe into a CSV file we are inserting the data into the MySQL database and transforming the data using the SQL query.

        mysql-connector-python

  The above library is used to connect the MySQL database in Python.


#### Step 5:
**Stremlit Dashboard Creation**

  By using Stremlit and plotly library, we create an interactive and visually appealing dashboard. And we also build a geo visualization in the plotly function. 


#### Step 6:
**Data Retrieval**

  The data can be Retried from the MySQL database and fetch the data into a Pandas dataframe and update the dashboard.


### Dataset
**Dataset Link** : [click here to view](https://github.com/PhonePe/pulse#readme)
