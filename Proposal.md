# Final Project Proposal

**GitHub Repo URL**: https://github.com/CMU-IDS-2022/final-project-solar

A short summary (3-4 paragraphs, about one page) of the data science problem you are addressing and what your solution will address. Feel free to include a figure or sketch to illustrate your project.

Each member of your group should submit the URL pointing to this document on your github repo.


# Summary
In the recent COP26 conference in November 2021, the Glasgow Climate Pact was negotiated with representatives from 197 countries, which included a pact to phase out the use of coal for energy production and consumption [1]. The use of coal to generate energy produces carbon dioxide emissions as a byproduct, which is detrimental to the environment, thus making coal the biggest contributor to climate change [2]. 

In recent years, there has been an increase in the use of renewable energy, such as solar, wind, and geothermal. In particular, California has been recognized as a leader among the US states for promoting renewable energy and policies that support renewable and carbon-free technologies as a solution for reducing greenhouse gas emissions. To balance sustainability and development, California has a diverse renewable energy portfolio. Additionally, the 100 Percent Clean Energy Act of 2018, also known as the Senate Bill 100, sets the goal that by 2045, all retail electricity sold in California and state agency electricity needs to be powered with renewable and zero-carbon resources. Thus, it would be interesting to investigate how the rest of the US compares to California in its initiatives to fully generate and consume clean energy. 

In this final project, we plan to focus on the different US states and understand the changes in renewable energy and nonrenewable energy over time. Our main question to investigate is: **Which state in the US had the largest increase in renewable energy and the largest reduction in the nonrenewable energy over time?** We will be using 1960-2019 state energy production estimate data published by the U.S. Energy Information Administration (EIA) to create visualisations and extract trends and insights [3]. With the identified trends from the visualisations, we expect to be able to pinpoint dates in time when certain bills are enacted to increase renewable energy and decrease nonrenewable energy production (i.e., the Senate Bill 100 in California). In our visualisations, policies and bills will also be added as part of the data. Ultimately, this will help us understand how policies are linked to actions, and how effective policies are in driving renewable energy.

Another question we can focus on is: **How long would it take for renewable energy to replace fossil fuels?** So with our visualisation, we expect to not only understand trends from the past, but also make some educated guesses and extrapolate trends about the future. By identifying trends over time for states that are performing well, we can apply them to certain states that are lagging behind. For example, if state A follows the path of state B, then state A can reach a certain percentage of clean energy in X amount of years.

1. https://en.wikipedia.org/wiki/Glasgow_Climate_Pact
2. https://endcoal.org/climate-change/#:~:text=Coal%20is%20the%20single%20biggest,emissions%20from%20the%20electricity%20sector.
3. https://www.eia.gov/state/seds/sep_prod/SEDS_Production_Report.pdf


# Sketches and Data Analysis
**Data Processing** 
Do you have to do substantial data cleanup? What quantities do you plan to derive from your data? How will data processing be implemented?  Show some screenshots of your data to demonstrate you have explored it.

**System Design**
How will you display your data? What types of interactions will you support? Provide some sketches that you have for the system design.
