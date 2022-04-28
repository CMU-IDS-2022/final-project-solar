import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data
import numpy as np
import matplotlib.pyplot as plt
from TableData import TABLENONE, TABLEREQUIRED, TABLEVOLUNTARY, TABLEEXPIRED
import folium
import branca
# import branca.colormap as cm
import leafmap.foliumap as leafmap
import requests
import time  # to simulate a real time data, time loop
import plotly.express as px  # interactive charts

dataFrameSerialization='legacy'

st.set_page_config(
    page_title="Renewable & Non-Renewable Energy Production Dashboard",
    page_icon="✅",
    layout="wide",
)

@st.cache
def load_data():
    production = pd.read_csv("us_prod.csv")
    stateProd = pd.read_csv("state_prod.csv")
    target = pd.read_csv("Prod_dataset.csv")
    return (production, stateProd, target)



# load the data
colT1,colT2 = st.columns([1,10])
with colT2:
    st.title("Trends and Predictions for Renewable & Non-Renewable Energy Production in the U.S.")
with st.spinner(text="Loading data..."):
    dfProduction, dfStateProd, dfTarget = load_data()
    # dfProduction
    # dfStateProd
    # dfTarget
colT3,colT4 = st.columns([5,8])
with colT4:
    st.subheader("Jamie Ho & Yi Zhou")

### show the image
from PIL import Image
image = Image.open('energy_source.jpg')
col1,col2 = st.columns([1,7])
with col2:
    st.image(image, caption='Renewable energy vs Fossil Fuel')


### Project Description
st.markdown("""In the recent COP26 conference in November 2021, [the Glasgow Climate Pact](https://en.wikipedia.org/wiki/Glasgow_Climate_Pact) was negotiated with representatives from 197 countries, which included a pact to phase out the use of coal for energy production and consumption. The use of coal to generate energy produces carbon dioxide emissions as a byproduct, which is detrimental to the environment, thus making coal the biggest contributor to climate change.
           
In recent years, there has been an increase in the use of renewable energy, such as solar, wind, and geothermal. In particular, California has been recognized as a leader among the US states for promoting renewable energy and policies that support renewable and carbon-free technologies as a solution for reducing greenhouse gas emissions. To balance sustainability and development, California has a diverse renewable energy portfolio. Additionally, the 100 Percent Clean Energy Act of 2018, also known as the Senate Bill 100, sets the goal that by 2045, all retail electricity sold in California and state agency electricity needs to be powered with renewable and zero-carbon resources. Thus, it would be interesting to investigate how the rest of the US compares to California in its initiatives to fully generate and consume clean energy.

We use the [1960-2019 state energy production estimate data published by the U.S. Energy Information Administration (EIA)](https://www.eia.gov/state/seds/sep_prod/xls/Prod_dataset.xlsx) and [Renewable Portfolio Standards (RPS) data from the National Conference of State Legislatures (NCSL)](https://www.ncsl.org/research/energy/renewable-portfolio-standards.aspx).

In this final project, we plan to focus on the different US states and understand the changes in renewable energy and nonrenewable energy over time. Our main question to investigate is: 
\"Which state in the US had the largest increase in renewable energy and the largest reduction in the nonrenewable energy over time?\"""", unsafe_allow_html=True)

st.text("\n")

# get additional map data to visualise
counties = alt.topo_feature(data.us_10m.url, 'counties')
states = alt.topo_feature(data.us_10m.url, 'states')

dfTarget.columns = ['State', 'Name', 'TypeID', 'ID', 'Type', 'Title', 'Established',
                    'Target', 'Date', 'Requirement', 'Applicable Sectors', 
                    'Cost Cap', 'Details', 'Enabling Statute, Code, or Order']

# Functions
# boolean function for data that is in the selected state
@st.cache
def get_state_membership(df, state):
    labels = pd.Series([1] * len(df), index=df.index)
    if state:
        labels &= df['State'].isin(state)
    return labels


### Folium map(we tried but gave up) ###
# m = leafmap.Map(center=(38, -98), zoom=4)
# polygons = 'us_states.json'
# m.add_geojson(polygons, layer_name="State")

# geojson_url = 'https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_states.json'
# response = requests.get(geojson_url)
# geojson = response.json()


# m = folium.Map(location=[38, -98], zoom_start=4)
# folium.Choropleth(
#     geo_data=geojson,
#     data=dfTarget,
#     columns=['State', 'TypeID'],
#     key_on='feature.id',
#     fill_color='Greens',
#     fill_opacity=0.75,
#     line_opacity=0.25
# ).add_to(m)
# m

### MAP SET-UP ###
st.text("\n")
st.subheader("Current Targets for Each State")

selectionbox = st.selectbox("I want to see the targets for:", ('all states','states with No Renewable Energy Targets',
'states with Expired Renewable Energy Targets','states with Voluntary Renewable Energy Targets',
'states with Required Renewable Energy Targets'))

# store the selection as index list 
if selectionbox==('states with No Renewable Energy Targets'):
    list=dfTarget.index[dfTarget['Type'] == 'None'].tolist()
if selectionbox==('states with Expired Renewable Energy Targets'):
    list=dfTarget.index[dfTarget['Type'] == 'Expired'].tolist()
if selectionbox==('states with Voluntary Renewable Energy Targets'):
    list=dfTarget.index[dfTarget['Type'] == 'Voluntary'].tolist()
if selectionbox==('states with Required Renewable Energy Targets'):
    list=dfTarget.index[dfTarget['Type'] == 'Required'].tolist()

# to create choropleth map of state targets dependent on selection 
if selectionbox =='all states':
    selection = alt.selection_multi()
    choropleth = (
        alt.Chart(states)
        .mark_geoshape(
            stroke='white'
        ).encode(
            tooltip=['State:N', 'Type:N', 'Title:N'],
            opacity=alt.condition(selection, alt.value(0.9), alt.value(0.25)),
            color=alt.Color('Type:N', title='Targets', scale=alt.Scale(
                domain=['None', 'Expired', 'Voluntary', 'Required'],
                range=['black', 'grey', 'lightgreen', 'green'])),
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(dfTarget, 'ID', ['Type','State','Title'])
        ).properties(
            width=1000,
            height=800
        ).project(
            'albersUsa'
        ).add_selection(
            selection
        )
    )
else:
    selection = alt.selection_multi()
    choropleth = (
        alt.Chart(states)
        .mark_geoshape(
            stroke='lightgrey'
        ).encode(
            tooltip=['State:N', 'Type:N', 'Title:N'],
            opacity=alt.condition(selection, alt.value(0.9), alt.value(0.25)),
            color=alt.Color('Type:N', title='Targets', scale=alt.Scale(
                domain=['None', 'Expired', 'Voluntary', 'Required'],
                range=['black', 'grey', 'lightgreen', 'green'])),
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(dfTarget.iloc[list], 'ID', ['Type','State','Title'])
        ).properties(
            width=1000,
            height=800
        ).project(
            'albersUsa'
        ).add_selection(
            selection
        )
    )


# to display the map with the legend

# use_container_width = False
# if st.checkbox('Use container width', True):
#     use_container_width=True

# cht_expander = st.expander('expander', expanded=False)

# cht_expander.altair_chart(choropleth, use_container_width=use_container_width)

# to adjust the legend positioning
cLegend = alt.layer(choropleth).configure_legend(
    orient='bottom',
    direction='horizontal'
)

col1, col2, col3 = st.columns([2,6,2])
with col1:
    st.write("")
with col2:
    cLegend
with col3:
    st.write("")


st.markdown("\n")
if selectionbox != 'all states':
    st.markdown('**Detailed Breakdown of Each State\'s Target**')
if selectionbox==('states with No Renewable Energy Targets'):
    with st.expander('States with No Renewable Energy Targets'):
        st.write(TABLENONE)
if selectionbox==('states with Expired Renewable Energy Targets'):
    with st.expander('States with Expired Renewable Energy Targets'):
        st.write(TABLEEXPIRED)
if selectionbox==('states with Voluntary Renewable Energy Targets'):
    with st.expander('States with Voluntary Renewable Energy Targets'):
        st.write(TABLEVOLUNTARY)
if selectionbox==('states with Required Renewable Energy Targets'):
    with st.expander('States with Required Renewable Energy Targets'):
        st.write(TABLEREQUIRED)


### ENERGY PRODUCTION CHARTS ###
st.subheader("\n")
st.subheader("Further Explorations by State(s)")
st.markdown('''In this section, you can explore the energy data for each state or compare between a maximum of three states.
\nPlease note that the Single State Exploration shows a detailed breakdown of different energy production types, whereas the Multiple State Exploration shows a general energy production profile (renewables VS non-renewables)''')


# show raw data section
st.write('\n')
rawdata = st.checkbox('Show raw data')
if rawdata:
    st.dataframe(dfProduction)

view_sel = st.selectbox("Would you like to see a single state or multiple states?",
                        ('Single', 'Multiple'))

# to create the SINGLE state display
if view_sel == 'Single':
    USstates = dfStateProd['State'].sort_values(ascending=True)
    state_sel = st.selectbox("Please select a state:", USstates.unique())
    state_membership = get_state_membership(dfStateProd, [state_sel])
    single_chart = (
        alt.Chart(dfStateProd[state_membership]).transform_fold(
            ['Biomass', 'Coal', 'Renewable Energy', 'Natural Gas', 'Crude Oil']
        ).mark_line().encode(
            x='Year:T',
            y=alt.Y('value:Q', 
                    scale=alt.Scale(domain=[0, 100]),
                    title='Percentage of Total Production'),
            color=alt.Color('key:N', title='Production Type', scale=alt.Scale(
                domain=['Biomass', 'Coal', 'Renewable Energy', 'Natural Gas', 'Crude Oil'],
                range=['darkgreen', 'black', 'lightgreen', 'lightgray', 'gray'])),
            tooltip=['State', 'Year:T', 'Total', 'Biomass', 'Coal', 
                     'Renewable Energy', 'Natural Gas', 'Crude Oil']
        ).properties(
            width=1000,
            height=500
        )
    )
    benchmark = st.checkbox('Show US baseline')
    if benchmark:
        baseline_sel = st.selectbox('Which production type for the US baseline do you want to see?',
                            ('Biomass', 'Coal', 'Renewable Energy', 'Natural Gas', 'Crude Oil'))
        baseline_chart = (
            alt.Chart(dfProduction).transform_fold(
                [baseline_sel]
            ).mark_line(
                strokeDash=[5, 5],
                strokeWidth=1.5
            ).encode(
                x='Year:T',
                y=alt.Y('value:Q', 
                        scale=alt.Scale(domain=[0, 100]),
                        title='Percentage of Total Production'),
                color=alt.Color('key:N', title='Production Type', scale=alt.Scale(
                    domain=['Biomass', 'Coal', 'Renewable Energy', 'Natural Gas', 'Crude Oil'],
                    range=['darkgreen', 'black', 'lightgreen', 'lightgray', 'gray'])),
                tooltip=['Year:T', 'Total', baseline_sel]
            ).properties(
                width=1000,
                height=500
            )
        )
        st.markdown("\n")
        st.markdown("\n")
        st.markdown('**Comparing the Different Energy Sources in Two States with the US Baseline**')
        #lay out the chart
        col_4, col_5, col_6 = st.columns([1,2,1])
        with col_4:
            st.write("")
        with col_5:
            single_chart + baseline_chart
        with col_6:
            st.write("")        
    else:
        st.markdown("\n")
        st.markdown("\n")
        st.markdown('**Comparing the Different Energy Sources in Three States**')
        #lay out the chart
        col_4, col_5, col_6 = st.columns([1,2,1])
        with col_4:
            st.write("")
        with col_5:
            single_chart 
        with col_6:
            st.write("")

def createChart(df, selState, energy, s):
    c = (
        alt.Chart(df[selState]).transform_fold(
            [energy]
        ).mark_line().encode(
            x='Year:T',
            y=alt.Y('value:Q', 
                    scale=alt.Scale(domain=[0, 100]),
                    title='Percentage of Total Production'),
            color=alt.Color('key:N', title='Production Type', scale=alt.Scale(
                range=['gray', 'darkgreen'])),
            tooltip=['State', 'Year:T', 'Renewables', 'FossilFuel']
        ).properties(
            width=1000,
            height=500
        )
    )
    l = createLabel(df, selState, energy, s)
    return c, l

def createLabel(df, selState, energy, s):
    l = (
        alt.Chart(df[selState]).transform_fold(
            [energy]
        ).mark_text(
            align='left', dx=3
        ).encode(
            x='max(Year):T',
            y=alt.Y('value:Q', aggregate={'argmax': 'Year'}),
            text='State:N',
            color=alt.Color('key:N', title='Production Type', scale=alt.Scale(
                range=['gray', 'darkgreen']))
        )
    )
    return l

# to create the MULTI state display
if view_sel == 'Multiple':
    USstates = dfStateProd['State'].sort_values(ascending=True)
    state_sels = st.multiselect("Please select up to 3 states:", 
                                USstates.unique(), default=['AK', 'AZ'])
    charts = 0
    if len(state_sels) > 3:
        st.markdown('_**ERROR:** You have selected more than 3 states._')
    else:
        counter = 0
        for s in state_sels:
            state_membership = get_state_membership(dfStateProd, [s])
            if counter == 0:
                cr1, lr1 = createChart(dfStateProd, state_membership, 'Renewables', s)
                cf1, lf1 = createChart(dfStateProd, state_membership, 'FossilFuel', s)
                counter += 1
            elif counter == 1:
                cr2, lr2 = createChart(dfStateProd, state_membership, 'Renewables', s)
                cf2, lf2 = createChart(dfStateProd, state_membership, 'FossilFuel', s)
                counter += 1
            elif counter == 2:
                cr3, lr3 = createChart(dfStateProd, state_membership, 'Renewables', s)
                cf3, lf3 = createChart(dfStateProd, state_membership, 'FossilFuel', s)
                counter += 1
        st.markdown("\n")
        st.markdown("\n")
        st.markdown('**Comparing the Energy Profiles Between Different States**')
        st.markdown('_Hover over the lines to see more information_')
        if len(state_sels) == 1:
            st.markdown('_**Note: Please select more than one state. If you want to view only one state, please use the Single State option.**_')
        elif len(state_sels) == 2:
            #lay out the chart
            col_4, col_5, col_6 = st.columns([1,2,1])
            with col_4:
                st.write("")
            with col_5:
                lr1+lf1+lr2+lf2 + cr1+cr2+cf1+cf2
            with col_6:
                st.write("")
        elif len(state_sels) == 3:            
            #lay out the chart
            col_4, col_5, col_6 = st.columns([1,2,1])
            with col_4:
                st.write("")
            with col_5:
                lr1+lf1+lr2+lf2+lr3+lf3 + cr1+cr2+cr3+cf1+cf2+cf3
            with col_6:
                st.write("")
            


### PREDICTION ON A SINGLE STATE ###
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.ForecasterAutoregCustom import ForecasterAutoregCustom
from skforecast.ForecasterAutoregMultiOutput import ForecasterAutoregMultiOutput
from skforecast.model_selection import grid_search_forecaster
from skforecast.model_selection import backtesting_forecaster
from joblib import dump, load

# Warnings configuration
# ==============================================================================
import warnings

st.markdown("\n")
st.markdown("\n")
st.subheader("Predictions on Renewables and Non-Renewable Energy Use")

# predict on the renewables and non-renewables for a single state
Prodstate_sel = st.selectbox("Please select a state:", USstates.unique(), key = 'T_Renewables')

Prodstate_membership = get_state_membership(dfStateProd, [Prodstate_sel])
stateIndex = dfTarget.index[dfTarget['State']==Prodstate_sel].tolist()
num = stateIndex[0]
stateTargetTable=dfTarget.iloc[stateIndex]

### create a dashboard for the values 
# creating a single-element container
placeholder = st.empty()

Type = stateTargetTable['Type']
newType=''
for i1 in Type:
    newType+=i1    

date=str(stateTargetTable['Date'][num])
if len(date) == 6:
    v = date[:4]
else:
    v = str(stateTargetTable['Date'][num])

with placeholder.container():
    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Target Type",
        value=newType
    )
    kpi2.metric(
        label="Target Date",
        value=v
    )
    kpi3.metric(
        label="Requirements for the Target",
        value=str(stateTargetTable['Target'][num])
    )


# Here is the prediction part: data preparation
data = dfStateProd[Prodstate_membership]
data['number']= range(0, 60)
st.text("\n")

# Split data into train-test
# ==============================================================================
steps = 10
data_train = data[:-steps]
data_test  = data[-steps:]

print(f"Train dates : {data_train.index.min()} --- {data_train.index.max()}  (n={len(data_train)})")
print(f"Test dates  : {data_test.index.min()} --- {data_test.index.max()}  (n={len(data_test)})")

# Create and train forecaster with the best hyperparameters
# ==============================================================================
# for renewables
regressor = RandomForestRegressor(max_depth=300, n_estimators=400, random_state=123)
forecaster = ForecasterAutoreg(
                regressor = regressor,
                lags = 20
                )

# for fossil fuel
regressor_fossil = RandomForestRegressor(max_depth=300, n_estimators=400, random_state=123)
forecaster_fossil = ForecasterAutoreg(
                regressor = regressor_fossil,
                lags = 15
                )

# Hyparameter tuning part 
# =============================================================================
# from lightgbm import LGBMRegressor
# forecaster = ForecasterAutoreg(
#                 regressor = LGBMRegressor(max_depth=100, n_estimators=400, random_state=123),
#                 lags = 5
#             )
# forecaster

### default settings for forecaster 
# forecaster = ForecasterAutoreg(
#                 regressor = RandomForestRegressor(random_state=123),
#                 lags = 15
#                 )

forecaster.fit(y=data_train['Renewables'])
forecaster_fossil.fit(y=data_train['FossilFuel'])

# Predictions based on existing times
# ==============================================================================
predictions = forecaster.predict(steps=steps)
predictions_fossil = forecaster_fossil.predict(steps=steps)


# Test error
# ==============================================================================
error_mse = mean_squared_error(
                y_true = data_test['Renewables'],
                y_pred = predictions
            )

error_mse_fossil = mean_squared_error(
                y_true = data_test['FossilFuel'],
                y_pred = predictions_fossil
            )

print(f"Test error (mse): {error_mse}, {error_mse_fossil}")
print(predictions,data_test['Renewables'])

# Predictions into the future till 2050
# ==============================================================================
futureSteps = 21
futurePredictions = forecaster.predict(steps=futureSteps)
futurePredictions_fossil = forecaster_fossil.predict(steps=futureSteps)

# Backtest with prediction intervals
# ==============================================================================
n_backtesting = 10*3 # The first 30 years are separated for backtesting
steps = 10

# for renewables
forecaster = ForecasterAutoreg(
                regressor = LinearRegression(),
                lags      = 15
             )

metric, predictions = backtesting_forecaster(
                            forecaster         = forecaster,
                            y                  = data['Renewables'],
                            initial_train_size = len(data) - n_backtesting,
                            fixed_train_size   = False,
                            steps              = steps,
                            metric             = 'mean_squared_error',
                            refit              = True,
                            interval           = [1, 99],
                            n_boot             = 100,
                            verbose            = True
                      )

print(f"Test error (mse): {error_mse}")

# for fossil fuel
forecaster_fossil = ForecasterAutoreg(
                regressor = LinearRegression(),
                lags      = 15
             )

metric, predictions_fossil = backtesting_forecaster(
                            forecaster         = forecaster_fossil,
                            y                  = data['FossilFuel'],
                            initial_train_size = len(data) - n_backtesting,
                            fixed_train_size   = False,
                            steps              = steps,
                            metric             = 'mean_squared_error',
                            refit              = True,
                            interval           = [1, 99],
                            n_boot             = 100,
                            verbose            = True
                      )

print(f"Test error (mse): {error_mse_fossil}")

# Combine prediction data to the true value
# ==============================================================================
# for renewables
dfFuturePredictions = pd.DataFrame(data=futurePredictions, columns=['pred'])
dfFuturePredictions['Year']= range(2010, 2031)


# join the prediction to the original data
mergeFuture = pd.merge_ordered(dfFuturePredictions,data[:-steps+1])
# mergeFuture = pd.merge(dfFuturePredictions,data_train,on='Year')
# joinFuture = data_train.join(dfFuturePredictions.set_index('Year'), on='Year')


# for fossil fuels
dfFuturePredictions_fossil = pd.DataFrame(data=futurePredictions_fossil, columns=['pred'])
dfFuturePredictions_fossil['Year']= range(2010, 2031)
# data['number']= range(1960, 2501)

# join the prediction to the original data
mergeFuture_fossil = pd.merge_ordered(dfFuturePredictions_fossil,data[:-steps+1])


################predict on the renewables and non-renewables for a single state
# =============================================================================
predict_chart2 = (
    alt.Chart(mergeFuture).transform_fold(
        ['Renewables', 'FossilFuel']
    ).mark_line().encode(
        x='Year:T',
        y=alt.Y('value:Q', 
                scale=alt.Scale(domain=[0, 100]),
                title='Percentage of Total Production'),
        color=alt.Color('key:N', title='Production Type', scale=alt.Scale(
            domain=['Renewables', 'FossilFuel'],
            range=['darkgreen', 'black'])),
        tooltip=['State', 'Year:T', 'Total', 'Renewables', 'FossilFuel']
    ).properties(
        width=1000,
        height=500
    )
)

futureLine = alt.Chart(mergeFuture).mark_line(
                strokeDash=[5, 5],
                strokeWidth=1.5
            ).encode(
    x='Year:T',
    y='pred',
    color=alt.value('darkgreen'),
    tooltip=['State', 'Year:T', 'pred']
)

futureLine_fossil = alt.Chart(mergeFuture_fossil).mark_line(
                strokeDash=[5, 5],
                strokeWidth=1.5
            ).encode(
    x='Year:T',
    y='pred',
    color=alt.value('black'),
    tooltip=['State', 'Year:T', 'pred']
)

xrule = (
    alt.Chart(pd.DataFrame({'Year':[2010]}))
    .mark_rule(color="darkgrey", strokeWidth=2)
    .encode(x='Year:T')
)

yrule = (
    alt.Chart(mergeFuture).mark_rule(color="darkgrey",size=0.5).encode(y=alt.datum(50))
)

text1 = alt.Chart(mergeFuture).mark_text(
    align='left', dx=3
).encode(
    x='max(Year):T',
    y=alt.datum(50),
    text=alt.value(' Renewables = Fossil Fuel')
)

# to lay out the chart
col4, col5, col6 = st.columns([3,6,2])

with col4:
    st.write("")
with col5:
    predict_chart2 + futureLine + futureLine_fossil + yrule + xrule + text1
with col6:
    st.write("")


st.markdown("""The diagram above shows the trends of renewables and fossil fuel and 
how our predictions forecast to the future year 2030. """)
st.markdown("""*Note that the energy consumption is calculated as percentage; the vertical 
bar stands for the splitting time for ground truth existing data and prediction; 
the horizontal grey rule stands for the datum where renewables and fossil fuel 
production are equal, and will possibly moving towards the trend where renewables 
production exceeds fossil fuel production """)



# Here is the part visualizing the uncetainty of our predictions
# =============================================================================
st.text("\n")
st.subheader("How reliable is the prediction?")
st.text("\n")
st.markdown("""Here we backtest the data with prediction intervals and 20 years prior to 2010 
are separated for backtesting. predictions for the renewables and the fossil fuel 
are separately visualized in which the orange prediction lines with bands shows 
the amount of uncertainty (although might not be obvious for some states) """)
# join the prediction to the true value 
# for renewables
predictions['number']= range(30, 60)
joinRenewables= data.join(predictions.set_index('number'), on='number')
# st.text(joinRenewables)

line = (
    alt.Chart(joinRenewables).transform_fold(
        ['Renewables', 'pred']
    ).mark_line().encode(
        x='Year:T',
        y=alt.Y('value:Q', 
                # scale=alt.Scale(domain=[0, 100]),
                title='Percentage of Total Production'),
            color=alt.Color('key:N', title='Predictions vs True value', scale=alt.Scale(
            domain=['Renewables', 'pred'],
            range=['darkgreen', 'orange'])),
        tooltip=['State', 'Year:T', 'Total', 'Renewables', 'FossilFuel']
    ).properties(
        width=800,
        height=400
    )
)

band = alt.Chart(joinRenewables).mark_area(opacity=0.5
).encode(
    x='Year:T',
    y='lower_bound', 
    y2='upper_bound',     
    color=alt.value('orange'), 
    tooltip=['State', 'Year:T', 'Total', 'Renewables']
).properties(
    width=800,
    height=400
)

# for fossil fuel
predictions_fossil['number']= range(30, 60)
joinFossil= data.join(predictions_fossil.set_index('number'), on='number')
# st.text(joinRenewables)

line_fossil = (
    alt.Chart(joinFossil).transform_fold(
        ['FossilFuel', 'pred']
    ).mark_line().encode(
        x='Year:T',
        y=alt.Y('value:Q', 
                # scale=alt.Scale(domain=[0, 100]),
                title='Percentage of Total Production'),
            color=alt.Color('key:N', title='Predictions vs True value', scale=alt.Scale(
            domain=['FossilFuel', 'pred'],
            range=['black', 'orange'])),
        tooltip=['State', 'Year:T', 'Total', 'FossilFuel']
    ).properties(
        width=800,
        height=400
    )
)

band_fossil = alt.Chart(joinFossil).mark_area(opacity=0.5
).encode(
    x='Year:T',
    y='lower_bound', 
    y2='upper_bound',     
    color=alt.value('orange'),    
    tooltip=['State', 'Year:T', 'Total', 'FossilFuel']
).properties(
    width=800,
    height=400
)

# to lay out the chart
col7, col8 = st.columns([1,1])

with col7:
    line + band + xrule    
with col8:
    line_fossil + band_fossil + xrule
    
# creating a single-element container
placeholder2 = st.empty()

with placeholder2.container():
    # create twp columns
    kpi4, kpi5 = st.columns(2)

    # fill in those three columns with respective metrics or KPIs
    kpi4.metric(
        label="MSE for renewable prediction is:",
        value=error_mse
    )
    kpi5.metric(
        label="MSE for fossil fuel prediction is:",
        value=error_mse_fossil
    )


#Reference: 
#1. https://www.cienciadedatos.net/documentos/py27-time-series-forecasting-python-scikitlearn.html
#2. https://www.cienciadedatos.net/documentos/py29-forecasting-electricity-power-demand-python.html
