# Final Project Proposal

**GitHub Repo URL**: https://github.com/CMU-IDS-2022/final-project-solar

A short summary (3-4 paragraphs, about one page) of the data science problem you are addressing and what your solution will address. Feel free to include a figure or sketch to illustrate your project.

Each member of your group should submit the URL pointing to this document on your github repo.


# Summary
In the recent COP26 conference in November 2021, the Glasgow Climate Pact was negotiated with representatives from 197 countries, which included a pact to phase out the use of coal for energy production and consumption [1]. The use of coal to generate energy produces carbon dioxide emissions as a byproduct, which is detrimental to the environment, thus making coal the biggest contributor to climate change [2]. 

In recent years, there has been an increase in the use of renewable energy, such as solar, wind, and geothermal. In particular, California has been recognized as a leader among the US states for promoting renewable energy and policies that support renewable and carbon-free technologies as a solution for reducing greenhouse gas emissions. To balance sustainability and development, California has a diverse renewable energy portfolio. Additionally, the 100 Percent Clean Energy Act of 2018, also known as the Senate Bill 100, sets the goal that by 2045, all retail electricity sold in California and state agency electricity needs to be powered with renewable and zero-carbon resources. Thus, it would be interesting to investigate how the rest of the US compares to California in its initiatives to fully generate and consume clean energy. 

In this final project, we plan to focus on the different US states and understand the changes in renewable energy and nonrenewable energy over time. Our main question to investigate is: **Which state in the US had the largest increase in renewable energy and the largest reduction in the nonrenewable energy over time?** We will be using the 1960-2019 state energy production estimate data published by the U.S. Energy Information Administration (EIA) to create visualisations and extract trends and insights [3]. Additional data displayed in a map visualisation and the tooltip feature will display the renewable energy goals that each states has adopted. This will be based on Renewable Portfolio Standards (RPS) data from the National Conference of State Legislatures (NCSL) [4]. The energy data will be represented as a percentage of the total energy profile. By doing so, we can begin to understand how close each state is to reaching their RPS goals, which is typically stated as a percentage to be met by a certain year. This will help us see which states are more proactive to convert fully into clean energy and see whether the states are working towards their set goals at a reasonable rate. Ultimately, this will help us understand how policies are linked to actions, specially how effective policies are in driving renewable energy.

Another question we can focus on is: **How long would it take for renewable energy to replace fossil fuels?** So with our visualisation, we plan to use SKLearn to predict the energy percentages in the future. We can then use existing data to extrapolate trends about the future to see whether the current rate is reasonable to reach the state-defined RPS goals.


1. https://en.wikipedia.org/wiki/Glasgow_Climate_Pact
2. https://endcoal.org/climate-change/#:~:text=Coal%20is%20the%20single%20biggest,emissions%20from%20the%20electricity%20sector.
3. https://www.eia.gov/state/seds/sep_prod/xls/Prod_dataset.xlsx
4. https://www.ncsl.org/research/energy/renewable-portfolio-standards.aspx


# Sketches and Data Analysis
**Data Processing** 

*Please note that the Summary section has also been updated.


After looking at the Prod_dataset.xlsx dataset, we will do the following data cleanup:
1. For each state, there are 29 rows of data for each type of energy production/consumption. We have identified the following energy type codes to use in our project: BDFDB, BFFDB, CLPRB, NCPRB, NGMPB, PAPRB, WDPRB. In particular, BDFDB, BFFDB, and WDPRB will be combined as one category of "biomass". (Refer Fig. 1)
2. Since the dataset includes energy data for every year between 1960-2019, we will only use and present data at 5-year increments so that it is more handleable. 
3. We will also calculate the total energy and the percentage that each type of energy source makes up for each state at each time point. This will make the profile of the energy sources easily readible for the audience. (Refer Fig. 2)
4. We will have to scrap the renewable portfolio standard data from source #4 listed above. The data will have to also be added to our final dataset. Furtheromre, for each state, we will add a column that identifies the state's current stance on RPS: with RPS, with voluntary RPS or targets, with expired RPS goals, and with no standard/targets.
5. We also plan to calculate the national average to display on the graph.


In general, the data cleanup will be relatively straight forward. We plan to do the cleanup in Python and rewrite a new csv file with only the data that we need for this project.


<em>Fig. 1: Energy codes that are coloured will be used in our project</em>
![alt text](https://raw.githubusercontent.com/CMU-IDS-2022/final-project-solar/main/Dataset%20-%20Energy%20groupings.jpg)

<em>Fig. 2: Full dataset from 1960-2019</em>
![alt text](https://raw.githubusercontent.com/CMU-IDS-2022/final-project-solar/main/Dataset%20-%201960%20to%202019.jpg)



**System Design**

We will display our data using the US map of all the states and charts. On the map, we will colour code each state with its current stance on RPS (Sketch 1). The tooltip feature will also show information, which includes the title of the energy standard, established date, requirement, applicable sectors, cost cap, details, enabling statute/code/order. There will be a filter that allows the audience to select the state of interest to see its energy trends. This will act as filtering instead of showing all states. 

For the first type of chart, we will also provide an option to turn on or off the national average data that can be used for benchmarking (Sketch 2). The tooltip will indicate the specific energy production in units of billion Btus as well as the percentage of the total. For the second type of chart, this is for comparison purposes between the energy productions of the user's selected states of interest (Sketch 3). For this chart, we will simplify the energy sources into renewable and fossil fuel only, which will allow for a cleaner graph.

<em>Sketch 1: Map visualisation</em>
![alt_text](https://raw.githubusercontent.com/CMU-IDS-2022/final-project-solar/main/Sketch1.jpeg)

<em>Sketch 2: First chart visualisation for focus on one state</em>
![alt_text](https://raw.githubusercontent.com/CMU-IDS-2022/final-project-solar/main/Sketch2.jpeg)

<em>Sketch 3: Second chart visualisation for comparison of states</em>
![alt_text](https://raw.githubusercontent.com/CMU-IDS-2022/final-project-solar/main/Sketch3.jpg)
