import pandas as pd
import streamlit as st
import mysql.connector as sql
import plotly.express as px  
from streamlit_option_menu import option_menu



mysql = sql.connect(
    host = "localhost",
    user= "root",
    password = "mysqlroot",
    database ="PhonePe"
  )
cursor = mysql.cursor()



st.set_page_config(page_title = "Phonepe Plusee Data Visualization and Exploration",
                   layout = "wide",
                   initial_sidebar_state = "expanded",
                   menu_items = {'About' : " This project was done by Narmadha Devi B"})


with st.sidebar:
    selected = option_menu(None, ["Home","Top Charts","Explore Data","Questions"],
                    icons = ["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                    menu_icon = "menu-button-wide",
                    default_index = 0,
                    styles = {"nav-link-selected": {"background-color": "#6F36AD"}})
    


if selected == "Home":
    st.header(' :violet[PhonePe Pluse]')
    
    col1, col2 = st.columns(2)

    with col1:
        st.video("https://www.phonepe.com/pulse/videos/pulse-video.mp4?v=1")

    with col2:
        st.markdown("### :black[PhonePe is a popular digital payment app in India, started in December 2015. It lets you to transfer money, pay bills, recharge phones, and shop online easily and securely using the Unified Payments Interface (UPI) system. PhonePe has grown rapidly, becoming one of the most popular payment apps in India due to its ease of use, security features, and wide range of services. The app also offers financial products such as insurance and mutual funds, expanding its portfolio beyond basic payment services.]")
        
    col1, col2 = st.columns(2)

    with col1:
        st.header(' :violet[Conversations]')
        st.subheader(' :violet[Visual stories showcasing the beat of progress]')
        st.markdown("##### :black[Catch Rahul Chari, Co-Founder & CTO, PhonePe in an in-depth conversation with Chandra Srikant, Editor, MoneyControl on how technology will continue to be a game changer for the industry.]")

    with col2:
        st.video("https://www.youtube.com/watch?v=qCOJt31ZXBs&embeds_referring_euri=https%3A%2F%2Fwww.phonepe.com%2F&source_ve_path=Mjg2NjY&feature=emb_logo")


    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("# :violet[SPOTLIGHT]")
        st.markdown("##### :blue[Conversation]")
        st.markdown("###### :black[Know more about Pulse]")
        st.video("https://www.youtube.com/watch?v=Yy03rjSUIB8&embeds_referring_euri=https%3A%2F%2Fwww.phonepe.com%2F&source_ve_path=Mjg2NjY&feature=emb_logo")

    with col2:
        st.markdown("### :blue[Articles]")
        st.image("https://www.phonepe.com/pulsestatic/799/pulse/static/c0d0a53053a4f7bdb5a45c047bdbe97e/6f9b9/spotlight_2.webp")
        url = "https://www.phonepe.com/pulse/articles/innovation_leading_to_accelerated_growth/"
        st.markdown(f"[Innovation Leading to Accelerated Growth]({url})")

    with col3:
        st.markdown("### :blue[Articles]")
        st.image("https://www.phonepe.com/pulsestatic/799/pulse/static/d8d783a2c0d5d913edd31b595277dd89/6365c/spotlight_4.webp")
        url = "https://www.phonepe.com/pulse/articles/changing_landscape_of_financial_services_india/"
        st.markdown(f"[India is steadily progressing towards the vision of becoming a cashless economy]({url})")


if selected == "Top Charts":
    st.header(':violet[PhonePe Pulse Data Visualization and Exploration : A User-Friendly Tool Using Streamlit and Plotly]')

    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))

    if Type == "Transactions":
        col1, col2, col3 = st.columns(3)
        with col1:
            Years = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023', '2024'), key='Years')
        with col2:
            Quarter = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='Quarter')
        with col3:
            Pay_type = st.selectbox('**Select Transaction type**',
                                        ('Recharge & bill payments', 'Peer-to-peer payments',
                                         'Merchant payments', 'Financial Services', 'Others'), key='Pay_type')
            
# Aggregated Transaction Plot 

        if Years in ['2024'] and Quarter in [ '2', '3', '4']:
           st.markdown(''' ### :red[No Data to Display for the above choosen year and quarter.]''')

        else:
            cursor.execute(f"SELECT State, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total  FROM phonepe.aggregated_transaction WHERE Year = '{Years}' AND Quarter = '{Quarter}' AND Transaction_type = '{Pay_type}' GROUP BY State ORDER BY Total DESC LIMIT  12;")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Transaction_amount'])
            fig = px.pie(df, values='Transaction_amount',
                                names='State',  
                                title='Top 10 Aggregated Transaction by State',
                                color_discrete_sequence=px.colors.sequential.Aggrnyl,
                                hover_data=['Transactions_Count'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

# Map Transaction Plot 

        if Years in ['2024'] and Quarter in [ '2', '3', '4']:
           st.markdown(''' ### :red[No Data to Display for the above choosen year and quarter.]''')

        else:
            cursor.execute(f"SELECT District, SUM(Count) AS Total_counts, SUM(Amount) AS Total_amounts FROM phonepe.map_transaction WHERE Year = '{Years}' AND Quarter = '{Quarter}' GROUP BY District ORDER BY Total_amounts DESC LIMIT 10;")
            df = pd.DataFrame(cursor.fetchall(), columns = [ 'District', 'Count', 'Amount'])
            fig = px.pie(df, values = 'Amount',
                            names = 'District',
                            title = 'Top 10 Map Transaction by District',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Count'],
                            labels={'Count':'Count'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

# Top Transaction Plot 

        if Years in ['2024'] and Quarter in [ '2', '3', '4']:
           st.markdown(''' ### :red[No Data to Display for the above choosen year and quarter.]''')
        
        else:    
            cursor.execute(f"select District, sum(Transaction_Count) as Total_Transactions_Count, sum(Transaction_Amount) as Total from phonepe.top_transaction where Year = '{Years}' and Quater = '{Quarter}' group by District order by Total desc limit 10;")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transaction_Count','Transaction_Amount'])
            fig = px.pie(df, values='Transaction_Amount',
                                    names='District',
                                    title='Top 10 Top Transaction by District',
                                    color_discrete_sequence=px.colors.sequential.amp,
                                    hover_data=['Transaction_Count'],
                                    labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


    if Type == "Users":
        col1, col2 = st.columns(2)
        with col1:
            Years = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023', '2024'), key='Years')
        with col2:
            Quarter = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='Quarter')

# Aggregated User

        if (Years in ['2022','2023','2024'] and Quarter in ['2', '3', '4']) or (Years in ['2024'] and Quarter in ['1']):
            st.markdown(''' ### :red[No Data to Display for the above choosen year and quarter.]''')
              
        else:
            cursor.execute(f"SELECT Brands, SUM(Counts) AS Total_Count, AVG(Percentage)*100 AS Avg_Percentage FROM phonepe.aggregated_user WHERE Year = '{Years}' AND Quarter = '{Quarter}' GROUP BY Brands ORDER BY Total_Count DESC LIMIT 10;")
            df = pd.DataFrame(cursor.fetchall(), columns=['Brands', 'Total_Count','Avg_Percentage'])
            df['Total_Count'] = pd.to_numeric(df['Total_Count'], errors='coerce')
            fig = px.scatter(df,
                 title='Top 10 Brands by User Counts and Percentage',
                 x="Total_Count",
                 y="Avg_Percentage",
                 color="Brands",
                 size="Total_Count",
                 hover_name="Brands",
                 color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
    

# Map User

        if Years in ['2024'] and Quarter in ['1', '2', '3', '4']:
            st.markdown(''' ### :red[No Data to Display for the above choosen year and quarter.]''')

        else:
            cursor.execute(f"select District, sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_App_Opens from phonepe.map_user where Year = '{Years}' and Quarter = '{Quarter}' group by District order by Total_Users desc limit 10;")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_App_Opens'])
            fig = px.scatter(df,
                    title='Top 10 District by Total Users and Total App Opens',
                    x="Total_Users",
                    y="Total_App_Opens",
                    color="District",
                    size=df['Total_Users'].astype(float),
                    hover_name="District",
                    color_continuous_scale=px.colors.sequential.algae)
            st.plotly_chart(fig, use_container_width=True)

# Top User

        if Years in ['2024'] and Quarter in ['1', '2', '3', '4']:
            st.markdown(''' ### :red[No Data to Display for the above choosen year and quarter.]''')

        else:
            cursor.execute(f"select District, sum(Registered_Users) as Total_Users from phonepe.top_user where Year = '{Years}' and Quater = '{Quarter}' group by District order by Total_Users desc limit 10;")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users'])
            fig = fig = px.scatter(df,
                    title='Top 10 District by Total Registered Users ',
                    x="Total_Users",
                    y="District",
                    color="District",
                    size=df['Total_Users'].astype(float),
                    hover_name="District",
                    color_continuous_scale=px.colors.sequential.amp)
            st.plotly_chart(fig, use_container_width=True)
        
    
if selected == "Explore Data":
    st.header(':violet[PhonePe Pulse Data Visualization and Exploration : A User-Friendly Tool Using Streamlit and Plotly]')

    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))

    if Type == "Transactions":
        
        Transaction = st.sidebar.selectbox("**Transaction**", ("Amount", "Count"))

        col1, col2 = st.columns(2)
        with col1:
            Years = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023', '2024'), key='Years')
        with col2:
            Quarter = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='Quarter')
        
        #col1, col2 = st.columns(2)

        if Transaction == "Amount":

            st.header(" :violet[ Overall State Transactions Amount]")
            #with col1:

            if Years in ['2024'] and Quarter in [ '2', '3', '4']:
                st.markdown(''' ### :red[No Data to Display for the above choosen year and quarter.]''')
            
            else:
                cursor.execute(f"SELECT State, SUM(Transaction_amount) AS Total_Amount FROM phonepe.aggregated_transaction WHERE Year = {Years} AND Quarter = {Quarter} GROUP BY State ORDER BY State;")
                df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Amount'])
                df2 = pd.read_csv('Agg_tran_path1.csv')
                df3 = df1.merge(df2, on='State')
                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_Amount',
                            color_continuous_scale='Viridis')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
                fig.show()

            #with col2:
        if Transaction == "Count":

            st.header(" :violet[ Overall State Transactions Count]")

            if Years in ['2024'] and Quarter in [ '2', '3', '4']:
                st.markdown(''' ### :red[No Data to Display for the above choosen year and quarter.]''')
            else:
                cursor.execute(f"SELECT State, AVG(Transaction_count) AS Total_Transactions FROM phonepe.aggregated_transaction WHERE Year = {Years} AND Quarter = {Quarter} GROUP BY State ORDER BY State;")
                df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions'])
                df2 = pd.read_csv('Agg_tran_path1.csv')
                df3 = df1.merge(df2, on='State')
                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_Transactions',
                            color_continuous_scale ='Bergeron')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
                fig.show()


    if Type == "Users":
        col1, col2 = st.columns(2)

        with col1:
            Years = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023', '2024'), key='Years')
        with col2:
            Quarter = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='Quarter')    
        
            
        st.markdown("## :violet[Overall State Users App opening frequency]")
        if Years in ['2024'] and Quarter in [ '2', '3', '4']:
                st.markdown(''' ### :red[No Data to Display for the above choosen year and quarter.]''')
        else:
            cursor.execute(f"select State, sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_App_Opens from Phonepe.map_user where Year = {Years} and Quarter = {Quarter} group by State order by State;")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_App_Opens'])
            df2 = pd.read_csv('Map_user_path4.csv')
            df3 = df1.merge(df2, on='State')            
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_App_Opens',
                    color_continuous_scale='Reds')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)


        st.markdown("## :violet[Overall State Registered Users]")
        if Years in ['2024'] and Quarter in [ '2', '3', '4']:
                st.markdown(''' ### :red[No Data to Display for the above choosen year and quarter.]''')
        else:
            cursor.execute(f"select State, sum(Registered_Users) as Total_Users FROM phonepe.top_user where Year = {Years} and Quater = {Quarter} group by State order by State;        ")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users'])
            df2 = pd.read_csv('Top_user_path6.csv')
            df3 = df1.merge(df2, on='State')            
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Users',
                    color_continuous_scale='purd')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)



if selected == "Questions":
    st.markdown(" ## :violet[Questions]")
    #st.markdown(":red[Select any one of the options]")

    Questions = st.selectbox( "Select the Questions",
                           ('1. What is the total transaction amount for each transaction type?',
                           '2. What are the top 10 states by transaction count in the year 2024?',
                           '3. What are the top 10 districts by transaction count?',
                           '4. What are the top 10 districts by total number of registered users and their respective states?',
                           '5. What are the top 10 districts by total app opens and their respective states?',
                           '6. Which quarter had the highest transaction amount for each state in 2023?',
                           '7. what are the total counts of each brand?',
                           '8. What are the top 10 district that has the highest Map transaction amount with its respective state?',
                           '9. Which district has the highest number of registered users by its respective state?',
                           '10. What is the top 10 number of registered users from the Map Users for each district?')) 


    if Questions=="1. What is the total transaction amount for each transaction type?":
        cursor.execute("Select DISTINCT Transaction_type as categorie_Type, SUM(Transaction_amount) as Transaction_Amount FROM phonepe.aggregated_transaction GROUP BY Transaction_type ORDER BY Transaction_Amount DESC;")
        df = pd.DataFrame(cursor.fetchall(), columns = [ 'categorie_Type', 'Transaction_Amount'])
        fig = px.bar(df, 
             x='categorie_Type', 
             y='Transaction_Amount', 
             color='categorie_Type', 
             title='Total Transaction Amount with Highest Transaction_Type ',
             color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig,use_container_width=True)
        st.write(df)

    elif Questions == "2. What are the top 10 states by transaction count in the year 2024?":
        cursor.execute("select State, sum(Transaction_count) as Counts from phonepe.aggregated_transaction where Year = 2024 group by State order by Counts desc limit 10;")
        df = pd.DataFrame(cursor.fetchall(), columns = ['State', 'Counts'])
        fig = px.bar(df,
                     x = 'State',
                     y = 'Counts',
                     color = 'State',
                     title = 'Top 10 Transaction Count in 2024 with its states',
                     color_discrete_sequence=px.colors.qualitative.Antique)
        st.plotly_chart(fig,use_container_width=True)
        st.write(df)
    

    elif Questions == "3. What are the top 10 districts by transaction count?":
        cursor.execute("select District, sum(Count) as Counts from phonepe.map_transaction group by District order by Counts desc limit 10;")
        df = pd.DataFrame(cursor.fetchall(), columns = ['District', 'Counts'])
        fig = px.bar(df, 
                     x = 'District',
                     y = 'Counts',
                     color = 'District',
                     title = 'Total Count from Map transaction with top 10 District',
                     color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig,use_container_width=True)
        st.write(df)
        

    elif Questions == "4. What are the top 10 districts by total number of registered users and their respective states?":
        cursor.execute("select District, State, sum(Registered_Users) as Total_Registered_Users from phonepe.top_user group by District, State order by Total_Registered_Users limit 10;")
        df = pd.DataFrame(cursor.fetchall(), columns = ['District', 'State','Total_Registered_Users'])
        fig = px.bar(df, 
                     x = 'District',
                     y = 'Total_Registered_Users',
                     color = 'District',
                     title = 'Number of Registered Users with their District and State',
                     color_discrete_sequence=px.colors.qualitative.Set1)
        st.plotly_chart(fig,use_container_width=True)
        st.write(df)

    elif Questions == "5. What are the top 10 districts by total app opens and their respective states?":
        cursor.execute("select District, State, sum(App_Opens) as Total_App_Opens from phonepe.map_user group by District, State order by Total_App_Opens limit 10;")
        df = pd.DataFrame(cursor.fetchall(), columns = ['District', 'State','Total_App_Opens'])
        fig = px.bar(df, 
                     x = 'District',
                     y = 'Total_App_Opens',
                     color = 'District',
                     title = 'Top 10 District with its App Opens ',
                     color_discrete_sequence=px.colors.qualitative.G10_r)
        st.plotly_chart(fig,use_container_width=True)
        st.write(df)


    elif Questions == "6. Which quarter had the highest transaction amount for each state in 2023?":
        cursor.execute("SELECT State, Quarter, SUM(Transaction_amount) AS Total_Transaction_Amount FROM phonepe.aggregated_transaction WHERE Year = 2023 GROUP BY State, Quarter ORDER BY Total_Transaction_Amount DESC limit 10;")
        df = pd.DataFrame(cursor.fetchall(), columns = [ 'State', 'Quarter', 'Total_Transaction_Amount'])
        fig = px.bar(df, 
                     x = 'State',
                     y = 'Total_Transaction_Amount',
                     color = 'State',
                     title = 'Highest Transaction with its quarter in 2023',
                     color_discrete_sequence=px.colors.qualitative.Light24)
        st.plotly_chart(fig,use_container_width=True)
        st.write(df)


    elif Questions == "7. what are the total counts of each brand?":
        cursor.execute("SELECT Brands, SUM(Counts) AS Total_Counts FROM phonepe.aggregated_user GROUP BY Brands ORDER BY Total_Counts DESC;")
        df = pd.DataFrame(cursor.fetchall(), columns = [ 'Brands', 'Total_Counts'])
        fig = px.bar(df, 
                     x = 'Brands',
                     y = 'Total_Counts',
                     color = 'Brands',
                     title = 'Total Counts with Mobile Brands',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig,use_container_width=True)
        st.write(df)

    elif Questions == "8. What are the top 10 district that has the highest Map transaction amount with its respective state?":
        cursor.execute("SELECT State, District, SUM(Amount) AS Total_Amount FROM phonepe.map_transaction GROUP BY State, District ORDER BY State, Total_Amount DESC limit 10;")
        df = pd.DataFrame(cursor.fetchall(), columns = [ 'State', 'District', 'Total_Amount'])
        fig = px.bar(df, 
                     x = 'District',
                     y = 'Total_Amount',
                     color = 'District',
                     title = ' Top 10 Map Transaction Amount by its District',
                     color_discrete_sequence=px.colors.qualitative.Plotly)
        st.plotly_chart(fig,use_container_width=True)
        st.write(df)
    
    elif Questions == "9. Which district has the highest number of registered users by its respective state?":
        cursor.execute("SELECT State, District, SUM(Registered_Users) AS Total_Registered_Users FROM  phonepe.map_user GROUP BY State, District ORDER BY State, Total_Registered_Users DESC limit 10;")
        df = pd.DataFrame(cursor.fetchall(), columns = [ 'State', 'District', 'Total_Registered_Users'])
        fig = px.bar(df, 
                     x = 'District',
                     y = 'Total_Registered_Users',
                     color = 'District',
                     title = 'Top 10 Registered Users by District',
                     color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig,use_container_width=True)
        st.write(df)

    elif Questions == "10. What is the top 10 number of registered users from the Map Users for each district?":
        cursor.execute("SELECT District, SUM(Registered_Users) AS Total_Registered_Users FROM phonepe.top_user GROUP BY District ORDER BY Total_Registered_Users DESC limit 10;")
        df = pd.DataFrame(cursor.fetchall(), columns = ['District', 'Total_Registered_Users'])
        fig = px.bar(df, 
                     x = 'District',
                     y = 'Total_Registered_Users',
                     color = 'District',
                     title = 'Top 10 Map Registered Users',
                     color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig,use_container_width=True)
        st.write(df)
