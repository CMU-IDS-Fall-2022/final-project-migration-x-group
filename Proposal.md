# Final Project Proposal

**GitHub Repo URL**: https://github.com/CMU-IDS-Fall-2022/final-project-migration-x-group <br/>
### Discover Reasons for Young Adult Migration and Its Social-Economic Impacts <br/>
Team Members: Cuiting Li, Haoyu Wang, Xinzhu Wang, Darren Butler, Yue Sun 

## Problem Description
Young adults entering the workforce are important to economic development, but some states in the U.S. see more migration of young adults than others, leading to inequities in workforce development. Therefore, we propose an interactive data science application that will allow stakeholders in economic development to interpret migration patterns of young adults from their state.


Do you ever wonder how far people migrate between childhood and young adulthood? Where do they go? How much does one's location during childhood determine the labor markets that one is exposed to in young adulthood?


We want to explore these questions using publicly available statistics on the migration patterns of young adults in the United States. Use this resource to discover where people in your hometown moved as young adults. What are the reasons behind young adult migration? Is it related to parental income, race, schooling, job market or climate? 

Datasets we will use are:
- Migration Pattern of young adults  https://data.migrationpatterns.org/MigrationPatternsData.zip <br/>


## Questions in action (granular level): 
1. What are the average miles (metric) for young adults who grew up in A and moved to B? 
2. What are the top 10 popular destinations for young adults over the past 10 years?
3. What are the top 10 least popular destinations for young adults over the past 10 years?
4. What is the migration rate of each state?
5. How does migration rates vary by race/climate/parental income/job market ? 
6. What are the top 3 reasons for young adult migration over the past 5 years vs 10 years? 
7. How are local labor market growth benefits geographically distributed across childhood residence locations?
8. [Prediction] Does growing up in a higher-mobility area have a causal effect on children's outcomes [income, social skills, etc.] in adulthood in proportion to childhood exposure?

## Proposed Solution
As the problem is geographically related, we would like to focus on map interactive visuals mainly. A U.S. map will provide a general overview of the distribution and patterns if there are any. We will also include connected charts and user input fields to show detailed information for specific groups, such as grouping by race and parental income.

## Related Work 
- Neighborhood influences on young children's emotional and behavioral problems <br/>
  https://aifs.gov.au/research/family-matters/no-84/neighbourhood-influences-young-childrens-emotional-and-behavioural
- Young Adult Migration <br/>
  https://www.census.gov/newsroom/press-kits/2022/young-adult-migration.html


## Sketches and Data Analysis
### Data Processing
#### PART A: Migration Analysis 
Data Source: https://data.migrationpatterns.org/MigrationPatternsData.zip   <br/>
By using the dataset, we seek the answer for the following questions.
1. What is the migration number for each state?
2. What is the average miles of migration
3. What are the most/least popular destinations?
4. How does the migration rate vary by state?
5. How does the migration rate vary by race?

After the initial EDA, we found that the dataset is clean and complete. The major processing we did is to use below formula to calculate the migration rate : <br/>
 migration_rate = (# of n if o_cz != d_cz) / n          <br/>

Findings are: 
- California has the most number of migration, followed by Texas and Florida.
- Top 3 states (measured by migration rate) are Wyoming, Montana and South Dakota
- Race - Other has the most number of migration across all the states.
- Race - Other has the largest number of migration rate, followed by Asian    <br/>

In addition, the origin and destination counts by state are about the same, which implies that the collectors of the data may have collected the data intentionally to balance the origin and destination representation. 


![image](https://user-images.githubusercontent.com/75749274/201198365-1ba3977b-70e5-4cf6-8e9f-5140a5c215f6.png)


We can also see that counts for the top 100 commuting zone destinations are the same. 

![image](https://user-images.githubusercontent.com/75749274/201198483-316d472e-ddef-4f8e-85ec-a6fd478bd828.png)


Last but not least, we need to consider is that the dataset is quite large (average file size is 50 MB); we might need to cut some of them, figure out how to do that, and make sure the data is representative after being cut.

![image](https://user-images.githubusercontent.com/75749274/201192947-800d7747-b2ad-45ea-8ca4-b02c8a25de7f.png)


#### PART B: Factors Influencing Migration Rate
#### 1.Parental Income   
Data Source: https://data.migrationpatterns.org/MigrationPatternsData.zip. This is the same dataset as above.  <br/>
Objective: by exploring and visualizing dataset: How does migration rates vary by parental income?

#### 2. Economy 
Objective: by exploring and visualizing dataset: try to answer How does the median household income affect migration.
We plan to use median household income as the metric for the commuting zone’s economic development. Given that this data is not available in the original migration dataset, we used the SAIPE ‘State and County Estimates’ Datasets from the United States Census Bureau website. This dataset contains  estimated poverty rate and estimate of median household income of each county in the U.S. from 2000 to 2021. Below is a screenshot of the ‘State and County Estimates for 2004’ data table.
![image](https://user-images.githubusercontent.com/75749274/201193237-0fdcf9f2-f6ba-4c8c-8ea4-f89b1835a5e7.png)

The original formats of State and County Estimates in different years are not consistent, for example, early data tables don’t contain labels but latest datatable contain labels for each column. Besides, the data needs to be aggregated on the commuting zone level. In addition, considering easier implementation and intuitive interaction, we plan to use only one numeric value as the economic metric for each commuting zone. Below are data processing steps:
Aggregate all data from 2000 - 2018 into a big datatable, with each column as the median household income for each year. Below is an example of the desired data table.
Aggregate the county-level data to CZ-level. Since the commuting zone (CZ) is grouped by counties, we can aggregate the county-level median household income data to create a data table with CZ-level median household income. The U.S. Department of Agriculture (USDA) website provides a datatable of Commuting Zones and Labor Market Area, based on which we plan to aggregate county-level data to CZ-level data. <br/>
Calculate the average of median household income from 2000 to 2018. Another data processing task we are facing relates to the time of household income data. Which year(s) of dataset should we use? Given that the samples in the original migration dataset are U.S. born children in the 1978-1992 birth cohorts, and the migration is counted as an individual's location from 16 to 26 years old, it would make sense to analyze the household income data from 2000-2018. 2000 is when the first group of individuals reached 16, and 2018 is when the last group of individuals reached 26 years old. Therefore we decided to calculate the average of median household income from 2000 to 2018 as the metric for CZ’s economic developmental level.

####  3. Education 
Objective: by exploring and visualizing dataset: try to answer How does education level or schooling situation in the region affect the migration.
Education/schooling was selected as an analysis factor. Given that this data is not available in the original migration dataset, we used the SCHOOL ENROLLMENT BY LEVEL OF SCHOOL FOR THE POPULATION 3 YEARS AND OVER dataset from the U.S. Census Bureau website. This dataset contains the number of school enrollments by the level of school for the population 3 years and over by county and state. The dataset I have performed EDA on contains data from 2013 - 2018. 
The original format of SCHOOL ENROLLMENT BY LEVEL OF SCHOOL FOR THE POPULATION 3 YEARS AND OVER is not suitable for Python analysis. City and state combinations were listed as columns, while the levels of school were listed as rows, all of which were in weird formatting. All the numbers had “,” in between and were in the “string” format. In addition, an additional educational rate column would be useful in performing analysis. Initial data processing was done by swapping axes, fixing the indexes and the header, fixing all the formatting, deleting unnecessary text strings, and adding an “Educational rate” column to the data table. Below is a screenshot from the processed ‘SCHOOL ENROLLMENT BY LEVEL OF SCHOOL FOR THE POPULATION 3 YEARS AND OVER’ data table.
![image](https://user-images.githubusercontent.com/75749274/201193414-9a7812d3-8a13-428a-85f0-3359c53355d9.png)



####  4.Job Market
Objective: by exploring and visualizing dataset: try to answer How does job affect the migration. Is there any correlation between employment rate and the destinations that people migrate to?  <br/>
Job openings and employment were selected as an analysis factor. Given that this data is not available in the original migration dataset, we used the dataset https://data.census.gov/cedsci/table?q=job%20opening%20by%20county&tid=ACSDP1Y2021.DP03 from the U.S. Census Bureau website. This dataset contains the total number of employment and percentage of employment of population age 16 and over of different counties in different states from 2010-2018 which is the time frame for the period we want to investigate. We have to do some data formatting of converting different counties into zip code zoom to match the granularity of the study.
For data processing and cleaning, data from 2000-2018 are scattered in different csv files, we have to do some data aggregation. Also, for some counties in certain years the data is missing, so we have to do some data cleaning.

![image](https://user-images.githubusercontent.com/75749274/201193546-93022479-9325-415c-87a5-42d445bc513b.png)



### System Design 

![Average Miles of Migration](https://user-images.githubusercontent.com/75749274/201190201-3d3ef5f6-1355-4a89-b213-c1961587d54c.png)

![Top 10 Popular Destinations](https://user-images.githubusercontent.com/75749274/201190302-1a91a6f3-bfe2-43b8-8603-c65b3fa126af.png)

![Migration Rate by State](https://user-images.githubusercontent.com/75749274/201190316-2d48a95d-7f9f-45be-816a-fb1a07179a69.png)
 “Other” category includes not only other races but also people who are not linked to the Decennial Census or ACS.

![Relationship between Migration Rates and Parental Income](https://user-images.githubusercontent.com/75749274/201190342-f1709d32-4526-48ca-b632-76f3c23b19fc.png)

![Relationship between Median Household Income and Percentage of Immigrants](https://user-images.githubusercontent.com/75749274/201190359-0337ccdd-2c20-4c9e-b42f-4807042c6ecd.png)

![Relationship between Education Rate and Migration Destination](https://user-images.githubusercontent.com/75749274/201190379-96679288-380f-4f8f-8f65-55ee3fd3df0d.png)

![Relationship between Employment and Migration Rate](https://user-images.githubusercontent.com/75749274/201190402-727d13af-5d9b-4c05-9eed-738423b82080.png)
