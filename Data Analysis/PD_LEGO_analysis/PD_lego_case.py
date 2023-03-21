# Use this cell to begin your analyses, and add as many cells as you would like!
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/KeithGalli/lego-analysis/master/datasets/lego_sets.csv')
parent_theme = pd.read_csv('https://raw.githubusercontent.com/KeithGalli/lego-analysis/master/datasets/parent_themes.csv')


print("\n\nDataset given: \n", df,  "\n \n", parent_theme, "\n\n")

###########################################################################################
print("\nTask 1: \nWhat % of all licensed sets ever released were star wars themed? ")

merged = df.merge(parent_theme, left_on="parent_theme", right_on="name")
merged.drop(columns="name_y", inplace= True) ## Names the second 'name'coulmn 'y_name' 
starwars_rows = merged.loc[merged["parent_theme"] == "Star Wars"]
starwars_rows_licensed = starwars_rows.loc[starwars_rows["is_licensed"] == True]
total_licensed = merged.loc[merged["is_licensed"] == True ]

print(f"Percent of total licensed lego sets is starwars:  {(starwars_rows.shape[0]/total_licensed.shape[0])*100:.2f}%")

###########################################################################################
print("\nTask 2: \nIn whitch year was Star Wars not the most popular licensed theme (in terms of number of sets released that year?)")

years_not_most_pop = [] 
for year in range (1999, 2017) : 

    # For all licensed, take from each year, the parent_theme and run valuecounts 
    year_n = total_licensed.loc[total_licensed["year"] == year ]["parent_theme"].value_counts()
    sw_sold = year_n["Star Wars"]
    most_sold = year_n[0]
    if sw_sold < most_sold:
        years_not_most_pop.append(year) 

print("The year/years Star Wars not the most popular licensed theme: ", years_not_most_pop)


for year in years_not_most_pop: 
    print(f"\nCounts in year: {year}")
    print(total_licensed.loc[total_licensed["year"] == year ]["parent_theme"].value_counts())


