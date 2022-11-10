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


### System Design 
![Average Miles of Migration](https://user-images.githubusercontent.com/75749274/201190201-3d3ef5f6-1355-4a89-b213-c1961587d54c.png)

![Top 10 Popular Destinations](https://user-images.githubusercontent.com/75749274/201190302-1a91a6f3-bfe2-43b8-8603-c65b3fa126af.png)

![Migration Rate by State](https://user-images.githubusercontent.com/75749274/201190316-2d48a95d-7f9f-45be-816a-fb1a07179a69.png)

![Relationship between Migration Rates and Parental Income](https://user-images.githubusercontent.com/75749274/201190342-f1709d32-4526-48ca-b632-76f3c23b19fc.png)


![Relationship between Median Household Income and Percentage of Immigrants](https://user-images.githubusercontent.com/75749274/201190359-0337ccdd-2c20-4c9e-b42f-4807042c6ecd.png)


![Relationship between Education Rate and Migration Destination](https://user-images.githubusercontent.com/75749274/201190379-96679288-380f-4f8f-8f65-55ee3fd3df0d.png)


![Relationship between Employment and Migration Rate](https://user-images.githubusercontent.com/75749274/201190402-727d13af-5d9b-4c05-9eed-738423b82080.png)
