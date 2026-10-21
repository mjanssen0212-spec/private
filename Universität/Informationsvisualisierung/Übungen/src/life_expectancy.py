import pandas as pd

# Exercise 6 of IV course 
# Put your code at the end of this file


# Load dataset from the library
df = pd.read_csv('data/life_expectancy_data.csv')

"""
Source: World Health Organization (WHO)
Time Frame: 2000–2015
Observations: 2,938 rows (country-year combinations)
Variables: 22 columns, including:
 Country: Name of the country
 Year: Year of the observation
 Status: Development status (Developed/Developing)
 LifeExpectancy: Average life expectancy in years
 AdultMortality: Probability of dying between ages 15 and 60
 InfantCeaths: Number of infant deaths per 1,000 live births
 AlcoholConsumption: Per capita alcohol consumption (liters)
 PercentageExpenditure: Expenditure on health as a percentage of GDP
 HepatitisB: Percentage of 1-year-olds immunized
 Measles: Number of reported measles cases
 BMI: Average Body Mass Index
 UnderFiveDeaths: Number of deaths under age five per 1,000 live births
 Polio: Percentage of 1-year-olds immunized
 TotalExpenditure: Total health expenditure per capita
 Diphtheria: Percentage of 1-year-olds immunized
 HIVAIDS: Estimated number of people living with HIV/AIDS
 GDP: Gross Domestic Product per capita
 Population: Total population
 Thinness1To19Years: Prevalence of thinness among children and adolescents
 Thinness5To9Years: Prevalence of thinness among children aged 5–9
 IncomeCompositionOfResources: Human Development Index in terms of income composition
 Schooling: Average number of years of schooling

This dataset is particularly useful for analyzing the relationships between 
various health indicators and life expectancy across different countries and years.
"""


# Now you can access this dataset as a pandas DataFrame

# First look at the data set
print(df)  # print(df.head())  # To see the first few rows of the dataset

# For this exercise, we only look at a single year, e.g. 2015

df_2015 = df[df['Year'] == 2015]

# Let's look at the levels of measurement of the variables in the dataset

# For example, Country and Status are categorial
print(df_2015['Country'])

# Other variables like LifeExpectancy are interval scaled, actually numerical
print(df_2015['LifeExpectancy'])

# For this exercise, we select some variables having at least interval scale (level of measurement)
selected_columns = ['LifeExpectancy', 'AlcoholConsumption', 'BMI', 'TotalExpenditure', 'GDP', 'Schooling']
selection = df_2015[selected_columns]

# Now your task is to compute the following values resp. generate the following diagrams:

# a) Mean, median, quartiles (lower, upper), minimum, maximum



# b) One boxplot with all interval scale variables



# c) Histograms for all interval scale variables in one graphic



# d) Scatterplot matrix with all numerical variables

