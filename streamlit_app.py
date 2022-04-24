import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data
import numpy as np
import matplotlib.pyplot as plt

dataFrameSerialization='legacy'

@st.cache
def load_data():
    production = pd.read_csv("us_prod.csv")
    stateProd = pd.read_csv("state_prod.csv")
    target = pd.read_csv("Prod_dataset.csv")
    return (production, stateProd, target)



# load the data
st.title("Trends and Predictions for Renewable & Non-Renewable Energy Production")
with st.spinner(text="Loading data..."):
    dfProduction, dfStateProd, dfTarget = load_data()
    # dfProduction
    # dfStateProd
    # dfTarget
st.subheader("Jamie Ho & Yi Zhou")
st.text(
"""In the recent COP26 conference in November 2021, the Glasgow Climate Pact was 
negotiated with representatives from 197 countries, which included a pact to phase 
out the use of coal for energy production and consumption. The use of coal to 
generate energy produces carbon dioxide emissions as a byproduct, which is 
detrimental to the environment, thus making coal the biggest contributor to 
climate change.
           
In recent years, there has been an increase in the use of renewable energy, such 
as solar, wind, and geothermal. In particular, California has been recognized as 
a leader among the US states for promoting renewable energy and policies that 
support renewable and carbon-free technologies as a solution for reducing 
greenhouse gas emissions. To balance sustainability and development, California 
has a diverse renewable energy portfolio. Additionally, the 100 Percent Clean 
Energy Act of 2018, also known as the Senate Bill 100, sets the goal that by 
2045, all retail electricity sold in California and state agency electricity 
needs to be powered with renewable and zero-carbon resources. Thus, it would be 
interesting to investigate how the rest of the US compares to California in its 
initiatives to fully generate and consume clean energy.
           
In this final project, we plan to focus on the different US states and understand 
the changes in renewable energy and nonrenewable energy over time. Our main 
question to investigate is: 
\"Which state in the US had the largest increase in renewable energy and the
largest reduction in the nonrenewable energy over time?\"""")
st.text("\n")

# get additional map data to visualise
counties = alt.topo_feature(data.us_10m.url, 'counties')
states = alt.topo_feature(data.us_10m.url, 'states')

dfTarget.columns = ['StateAbbrev', 'State', 'ID', 'Latitude', 'Longtiude', 
                   'Type', 'Title', 'Established', 'Requirement', 
                   'Applicable Sectors', 'Cost Cap', 'Details', 
                   'Enabling Statute, Code, or Order']

### MAP SET-UP ###

st.subheader("Current Targets for Each State")
st.markdown("Click to select one state or Shift-Click to select multiple states")
st.markdown("Click the background to deselect")

# to select multiple states
selection = alt.selection_multi()

# to create choropleth map of state targets
choropleth = (
    alt.Chart(states)
    .mark_geoshape(
        stroke='white'
    ).encode(
        color=alt.Color('Type:N', title='Targets', scale=alt.Scale(
            domain=['None', 'Expired', 'Voluntary', 'Required'],
            range=['black', 'grey', 'lightgreen', 'green'])),
        opacity=alt.condition(selection, alt.value(0.9), alt.value(0.25)),
        tooltip=['State:N', 'Type:N', 'Title:N', 'Established:N', 'Requirement:N', 
                 'Applicable Sectors:N', 'Cost Cap:N', 'Details:N', 
                 'Enabling Statute, Code, or Order:N']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(dfTarget, 'ID', ['Type'])
    ).properties(
        width=700,
        height=500
    ).project(
        'albersUsa'
    ).add_selection(
        selection
    )
)

# to adjust the legend positioning
cLegend = alt.layer(choropleth).configure_legend(
    orient='bottom',
    direction='horizontal'
)

# to display the map with the legend
cLegend


### ENERGY PRODUCTION CHARTS ###
st.subheader("Further Explorations by State(s)")

view_sel = st.selectbox("Would you like to see one or multiple states?",
                        ('Single', 'Multiple'))

# boolean function for data that is in the selected state
@st.cache
def get_state_membership(df, state):
    labels = pd.Series([1] * len(df), index=df.index)
    if state:
        labels &= df['State'].isin(state)
        print(labels)
    return labels


# to create the SINGLE state display
if view_sel == 'Single':
    USstates = dfStateProd['State'].sort_values(ascending=True)
    state_sel = st.selectbox("Please select a state:", USstates.unique())
    st.text(state_sel)
    state_membership = get_state_membership(dfStateProd, [state_sel])
    st.text(state_membership)
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
            tooltip=['State', 'Year:T', 'Total', 'Biomass', 'Coal', 'Renewable Energy', 'Natural Gas', 'Crude Oil']
        ).add_selection(
            selection
        ).properties(
            width=700,
            height=350
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
                width=700,
                height=350
            )
        )
        single_chart + baseline_chart
    else:
        single_chart


# to create the MULTI state display
if view_sel == 'Multiple':
    USstates = dfStateProd['State'].sort_values(ascending=True)
    state_sels = st.multiselect("Please select/deselect some states:", 
                                USstates.unique())
    st.text(state_sels)
    state_membership = get_state_membership(dfStateProd, [state_sels])
    print(state_membership)
    st.text(state_membership)
    multi_chart = (
        alt.Chart(dfStateProd[state_membership]).transform_fold(
            ['T_Renewables', 'T_FossilFuels']
        ).mark_line().encode(
            x='Year:T',
            y=alt.Y('value:Q', 
                    scale=alt.Scale(domain=[0, 100]),
                    title='Percentage of Total Production'),
            color=alt.Color('key:N', title='Production Type', scale=alt.Scale(
                domain=['T_Renewables', 'T_FossilFuels'],
                range=['darkgreen', 'gray'])),
            tooltip=['State', 'Year:T', 'Total', 'T_Renewables', 'T_FossilFuels']
        ).add_selection(
            selection
        ).properties(
            width=700,
            height=350
        )
    )
    multi_chart







    # nearest = alt.selection(type='single', nearest=True, on='mouseover',
    #                         fields=['Year:T'], empty='none')
    # selectors = alt.Chart(dfStateProd).mark_point().encode(
    #     x='Year:T',
    #     opacity=alt.value(0),
    # ).add_selection(
    #     nearest
    # )
    # text = single_chart.mark_text(align='left', dx=5, dy=-5).encode(
    #     text=alt.condition(nearest, 'value:Q', alt.value(' '))
    # )
    # rules = alt.Chart(dfStateProd).mark_rule(color='gray').encode(
    #     x='Year:T',
    # ).transform_filter(
    #     nearest
    # )
    # alt.layer(single_chart, selectors, text, rules)












# '''

# # dfProduction['Renewables'] = data['BDFDB'] + data['BFFDB']+ data['WDPRB']+ data['NCPRB']

# # create a Python list of feature names
# feature_cols = ['BDFDB','BFFDB', 'WDPRB','NCPRB']

# # use the list to select a subset of the original DataFrame
# x = dfProduction[feature_cols]

# y = dfProduction['T_Renewables']
# with st.spinner(text="Loading data..."):
#     x
#     y

# from sklearn.model_selection import train_test_split
# x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)

# # default split is 75% for training and 25% for testing
# print(x_train.shape)
# print(y_train.shape)
# print(x_test.shape)
# print(y_test.shape)

# # import model
# from sklearn.linear_model import LinearRegression

# # instantiate
# linreg = LinearRegression()

# # fit the model to the training data (learn the coefficients)
# linreg.fit(x_train, y_train)

# # pair the feature names with the coefficients
# list(zip(feature_cols, linreg.coef_))

# # make predictions on the testing set
# y_pred = linreg.predict(x_test)

# print(y_pred)
# pred_vals = linreg.predict(x_train)
# residuals = pred_vals - y_train

# d = {'col1': [1, 2], 'col2': [3, 4]}
# df = pd.DataFrame(data=d)
# df

# plt.scatter(pred_vals, residuals)
# plt.hlines(y=0, xmin=3000000, xmax=8000000)
# plt.xlabel('Fitted values')
# plt.ylabel('Residual')
# plt.show()


# ########################### Evaluate the model!
# from sklearn import metrics
# # calculate MAE using scikit-learn
# print(metrics.mean_absolute_error(y_test, y_pred))

# # calculate MSE using scikit-learn
# print(metrics.mean_squared_error(y_test, y_pred))

# # calculate RMSE using scikit-learn
# print(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

# ########################### Regularization
# from sklearn.linear_model import Lasso

# # instantiate
# linreg = Lasso(alpha = 1)

# # fit the model to the training data (learn the coefficients)
# linreg.fit(x_train, y_train)

# y_pred = linreg.predict(x_test)
# print(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

# '''
