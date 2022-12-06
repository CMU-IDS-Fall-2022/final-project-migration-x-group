# Discover Reasons for Young Adult Migration and Its Social-Economic Impacts <br />
Datasets we have used are from:
- Migration Pattern of young adults https://data.migrationpatterns.org/MigrationPatternsData.zip
- https://www.edweek.org/policy-politics/grading-the-states/2008/01
- 
## Data Transformation
In order to accurately compare migration status state by state, we decide to use migration rate rather than the total number of migrants. 

- state_lvl_migr_rate['total'] = state_lvl_migr_rate['inbound_migration']+state_lvl_migr_rate['outbound_migration']+state_lvl_migr_rate['within_state_migration'] 
- state_lvl_migr_rate['inbound_rate'] = state_lvl_migr_rate['inbound_migration'] / state_lvl_migr_rate['total']  
- state_lvl_migr_rate['outbound_rate'] = state_lvl_migr_rate['outbound_migration'] / state_lvl_migr_rate['total']  
- state_lvl_migr_rate['within_state_rate'] = state_lvl_migr_rate['within_state_migration'] / state_lvl_migr_rate['total']  


# Discover U.S. Migration Pattern <br />
## Part1. Migration Rate by State and Race <br />
Data sample includes all children who were born in the U.S. between 1984-92, and tracked individual's migration activity from age 16 to age 26. 
By viewing the average migration rate for each state by different races, race Black reached its peak in Hawaii; race Asian peaked in Kansas, and Hispanic peaked in Vermont.
From website https://files.hawaii.gov/dbedt/census/Census_2010/SF1/Hawaii_Population_Facts_6-2011.pdf, it also shows that from 2000 to 2010, Black or African American population dropped by 2.6%.
On the other side, race Black's lowest point is in Maryland; race Hispanic's lowest point is in Illinois;race Asian's lowest point is in New York.

## Part2. Popular Migration Routes <br />
We discovered the migration trends from three dimensions:
### Outbound Migration  <br />
  Top 5 states with highest outbound migration rates are : New Hampshire, Vermont and Wyoming, Connecticut and New Jersey. 
  Among these 5 states, 4 out of 5 are from the east coast.
  Top 1 states with the lowest outbound migration rate is Califonia, which is located at west coast. 
  - Finding 1. Young adults from east coast tend to move out. 
  - Finding 2. Massachussetts, Maine, New York and California are the top 4 destination states for young adult of New Hampshire migrated to. 
  - Finding 3. From the popular routes of young adults in New Hampshire, we see that education is one of the factors attracting young adults migrated out.
  
### Inbound Migration  <br />
   Most popular 5 states per inbound migration rates are: Colorado, Nevada, DC, North Dakota and Alaska. And all of them are not located either east or west coast.
   - For Colorado and Nevada, most of young migrants are from California. 
   Least popular 5 states per inboud migration rates are: Michigan, Ohio, New Jerse, Pennsylvania and Mississippi. 
   Further analysis: why does Alaska become popular destination during that time? and why dose Michigan not attract young adults? 
   
### Within State Migration   <br />
Despite California is the No.1 state for the most popular destination Colorado, young adults from California have a higher stay in home state rate compared to young adults from other states; whereas young adults from Wyoming tend to move out.
