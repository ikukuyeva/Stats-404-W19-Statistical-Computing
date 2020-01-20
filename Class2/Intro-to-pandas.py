#!/usr/bin/env python
# coding: utf-8

# # Introduction to `pandas`
# References: 
# - "Python for Data Analysis" by Wes McKinney - for discussion on `pandas`
# - ["Hacking Airline DataSet with H2O"](https://github.com/h2oai/h2o-2/wiki/Hacking-Airline-DataSet-with-H2O) -- for Airline data sets of [various sizes](https://s3.amazonaws.com/h2o-airlines-unpacked/)

# In[1]:
# **Prerequisities**: `pandas` is installed in your virtual environment


import pandas as pd


# ## `pandas` Data Types

# ### `Series`

tmp = pd.Series([3, 5, -1])
tmp

tmp.values
tmp.index


# `DataFrame`
# In[6]:


df_tmp = pd.DataFrame([3, 5, -1], columns=['col_name'])
df_tmp


df_tmp.shape
df_tmp.columns
df_tmp['col_name'].values
# In[10]:


df_tmp.index


# ## Reading-in Airlines Data for [Business use case](https://docs.google.com/presentation/d/1zOOBaxZtTF_FJat9uGKrgJvMSMzmXQVtO4Vl5J-CpAw/edit#slide=id.g763bd8f17d_0_288)
file_name = "https://s3.amazonaws.com/h2o-airlines-unpacked/year1987.csv"
df = pd.read_csv(filepath_or_buffer=file_name,
                 encoding='latin-1',
                 nrows=1000
                )

# Alternative to ?pd.read_csv to see function arguments:
import inspect
inspect.signature(pd.read_csv)


# Other file formats you can read-in:
# - CSV and non-CSV delimited: `read_table`
# - JSON via `read_json`
# - fixed-width format via `read_fwf`
# - data on clipboard via `read_clipboard`

# ## EDA or Getting to Know your Data Set

# ### Step 1: Read [documentation and data dictionary](http://stat-computing.org/dataexpo/2009/the-data.html)

# ![Screenshot of Airline data documentation](images/Airlines_documentation.png)

# ### Step 2: Basic Checks
# - size
# - shape
# - values/ranges
# - degree of missingness
# - `<your favorite check(s)>`

# In[18]:


df.shape


# In[19]:


df.columns


# In[20]:


df.head()


# In[21]:


pd.options.display.max_columns = 50


# In[22]:


df.tail()


# In[34]:


df['Year'].value_counts(sort=False)


# In[37]:


from collections import Counter
Counter(df['Month'])



# In[48]:


df.describe()


# **Caution**: Missing values are ignored and counts not shown.

df.info()
# ## Aside: Missing Values in Python
# When you need to check for missing values -- similar to R, you can't do `variable == NaN' -- you can check for:
# - `variable_value is None`
# - `math.isnan(variable_value)` -- after importing the `math` library
# - `pd.isnull(variable_value)`
# - non-emptiness per section [Truth Value testing](https://docs.python.org/3/library/stdtypes.html): 
#   - `not []`
#   - `not ""`
#   - etc.
# Topic of handling missing data is an important topic outside scope of class. Recommend book by [Little and Rubin](https://www.amazon.com/Statistical-Analysis-Missing-Probability-Statistics-dp-0470526793/dp/0470526793/ref=mt_hardcover?_encoding=UTF8&me=&qid=) on the subject. 
# 
# Recall that **it's not recommended** to:
# - drop all missing values, OR
# - fill-in missing values with mean (for example)
# to not bias your data.
# 
# It's better to:
# - understand why the data was missing in first place AND, if need to,
# - fill-in with a `missing` category: `dataset.fillna('Missing')`
# ## Subsetting

# In[22]:


# Arrival Delays of 1.5+ hours:
df[ df['ArrDelay'] >= 90]


# In[23]:


# Departure Delays of 1+ hours:
df['DepDelay'][ df['DepDelay'] >= 60].count()


# **Warning** when subsetting and assigning in `pandas`: 
# - When you subset a data set, you can access a view or copy [reference]](https://www.dataquest.io/blog/settingwithcopywarning/) and [[reference]](http://pandas.pydata.org/pandas-docs/stable/indexing.html?highlight=set#indexing-view-versus-copy).
# - If you try to assign values on your subset, you will get a `SettingWithCopy` warning, to make sure you check that you're assigning values to the data set you expect (e.g. view or copy).

# In[24]:


# Recall our data set:
df_tmp


# Example of warning:

# In[25]:


df_tmp[df_tmp['col_name'] == 5]


# In[26]:


df_tmp[df_tmp['col_name'] == 5]['col_name'] = -5


# ![Subsetting in `pandas`](images/pandas-subsetting.png) [Reference](https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/)

# ### Subsetting with `loc` -- based on "**l**abels":

# In[27]:


cols_include = ['Year', 'Month', 'DayofMonth', 'DayOfWeek', 'ArrDelay', 'DepDelay']
df.loc[df['ArrDelay'] >= 90, cols_include]


# ### Subsetting with `iloc` -- based on "**i**ndex":

# In[28]:


import numpy as np
np.where(df['ArrDelay'] >= 90)


# How can we format this to be a list?

# In[29]:


row_index = np.where(df['ArrDelay'] >= 90)[0].tolist()
row_index


# In[30]:


col_index = list(range(4)) + list(range(13, 15))
col_index


# In[31]:


df.iloc[row_index, col_index]


# ## Visual Checks

# In[32]:


get_ipython().run_line_magic('matplotlib', 'inline')

# Flight arrival delays for Friday flights in 10/1987:
df['ArrDelay'][df['DayOfWeek'] == 5].hist(bins=50)


# In[33]:


get_ipython().run_line_magic('matplotlib', 'inline')

df['DayOfWeek'].value_counts(sort=False).plot(kind='barh')


# In[34]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

# Per http://queirozf.com/entries/pandas-dataframe-plot-examples-with-matplotlib-pyplot
# gca stands for 'get current axis'
ax = plt.gca()
df['DayOfWeek'].value_counts(sort=False).plot(kind='barh',
                                              color='0.75',
                                              x="Number of Flights",
                                              y="Day of Week",
                                              ax=ax
                                              )
ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])
ax.set_title("Number of Flights per Day of Week")
ax.set_xlabel("Number of Flights")
ax.set_ylabel("Day of Week")
plt.show()


# In[35]:


# Stacked bar plot
df_crosstab = pd.crosstab(df['DayOfWeek'], df['ArrDelay'] >= 30, normalize=True)
df_crosstab.plot(kind='bar', stacked=True)


# Aside: interactive graphics in Python via [`plotly`](https://plot.ly/python/)
# ## Row/Column Operations

# In[115]:


# Derive quantity based on one column:
df['ArrDelay_hours'] = df['ArrDelay'].apply(lambda x: round(x/60.0, 2))
df[['ArrDelay', 'ArrDelay_hours']].head(5)


# In[216]:


# Derive quantity based on more than one column:
def number_of_delays(arrival_delayed_flag, departure_delayed_flag):
    """Fcn to count how many delays there were per flight."""
    count = 0
    if arrival_delayed_flag == 'YES':
        count += 1
    if departure_delayed_flag == 'YES':
        count += 1
    return count

df['delay_count'] = df[['IsArrDelayed', 'IsDepDelayed']].apply(
    lambda row: number_of_delays(row[0], row[1]),
    axis=1)
df[['ArrDelay', 'IsArrDelayed', 'DepDelay', 'IsDepDelayed', 'delay_count']].head()


# ## 10 minute break

# # Intermediate `pandas`
# ## Concatenating, Merging and Joining, Pivoting, Grouping
# 
# For more examples on concatenating and merging, please see: [pandas documentation](https://pandas.pydata.org/pandas-docs/stable/merging.html)

# ### Example data sets

# In[51]:


df1 = pd.DataFrame({'A': [1, 2],
                    'B': [3, 4]
                   }
                  )
df1


# In[37]:


df2 = pd.DataFrame({'A': [1, 2, 1],
                    'B': [3, 3, 4],
                    'C': [0, -1, 2]
                   },
                   index=[0, 1, 2]
                  )
df2


# ### Concatenating

# In[47]:


# rbind() equivalent:
df1.append(df2)


# In[48]:


# Fix warning message using provided recomendations:
df1.append(df2, sort=False)


# In[39]:


inspect.signature(df1.append)


# In[40]:


# Axis=0 for rows and axis=1 for columns:
pd.concat([df1, df2], axis=1)


# In[41]:


inspect.signature(pd.concat)


# In[49]:


# similar to cbind():
pd.concat([df1, df2], axis=1, join='inner')


# ### Merging and Joining

# ![Visualization of Joins](images/joins.png)[[reference]](https://www.dofactory.com/sql/join)

# In[53]:


pd.merge(left=df1,
         right=df2, 
         how='left',
         on=['A', 'B'])


# In[44]:


inspect.signature(pd.merge)


# In[52]:
# ![Joins that you can do in pandas](./images/pandas-merge-args.png)


df_merged = pd.merge(left=df1,
                     right=df2, 
                     how='outer',
                     on=['A', 'B'],
                     indicator='indicator_column')
df_merged


# **TIPs**: 
# - Write out tables that you're going to be combining, columns of interest (to keep in final table), and column(s) that they share. It will be easier to define the merge/SQL/etc. statements.
# 
# - Usually `merge` is the answer (over `append` or `concat`), and it's easier to follow, as you're explicitly stating what you're doing.

# ### Pivoting
# EX: Get counts of flight delay durations (categorical) by day of week.

# What should be our first step in creating a categorical variable for departure delays?

# In[72]:


# Step 1: Explore distribution of flight departure delays for all days of week:
df['DepDelay'].hist(bins=50)


# In[153]:


# Step 2: Create buckets of departure delays and check distribution:
df['DepDelay_bins'] = pd.cut(df['DepDelay'], bins=[-15, -1, 0, 15, 30, 45, 60, 90, 3000])
df['DepDelay_bins'].value_counts(sort=False)


# In[154]:


# Step 3: Add a count of observations 'n':
df_delays = df[['DayOfWeek', 'DepDelay_bins']]
df_delays = df_delays.assign(n=1)
df_delays.head()


# In[155]:


# Step 4: Get counts of flight delays by DOW and duration of delay:
df_delays.pivot_table(index="DepDelay_bins", columns="DayOfWeek", aggfunc=sum)


# ### Grouping

# ![Split-apply-combine strategy of grouping](./images/split-apply-combine.png) [reference](https://jakevdp.github.io/blog/2017/03/22/group-by-from-scratch/)

# In[191]:


# What paths did the carrier fly out of LA County:
df_origin_dest_LA = df.loc[df['Origin'].isin(('BUR', 'LAX', 'LGB')),
                           ['Origin', 'Dest']]
df_origin_dest_LA = df_origin_dest_LA.assign(n=1)
df_origin_dest_LA.groupby(['Origin', 'Dest']).sum()


# In[161]:


# What's the average delay:
df.groupby(['UniqueCarrier', 'DayOfWeek'])['ArrDelay'].mean()


# In[160]:


# If there is a delay, what's the average delay:
df.loc[df['ArrDelay'] >= 0].groupby(
    ['UniqueCarrier', 'DayOfWeek'])['ArrDelay'].mean()


# In[224]:


# Largest delay type by flightpath origin:

def largest_delay(variables):
    max_arrival_delay = max(variables.ArrDelay)
    max_departure_delay = max(variables.DepDelay)
    if math.fabs(max_arrival_delay) > max_departure_delay:
        return 'arrival'
    elif math.fabs(max_arrival_delay) < max_departure_delay:
        return 'departure'
    else:
        return 'arival-and-departure'
    
df[['Origin', 'ArrDelay', 'DepDelay']].groupby('Origin').apply(
    lambda x: largest_delay(x))
# SAN = San Diego


# ## Prerequisites for Next Section: SQL
# 
# **Please see slide [deck](http://bit.ly/30CPeVe)** for installation instructions of SQLite
# 
# ## 10 minute break

# ## pandas and Databases

# ### `pandasql`
# - [`pandasql`](https://pypi.org/project/pandasql/) gives you ability to run `SQL` queries on your `pandas` data set
# - Similar to [`sqldf`](https://cran.r-project.org/web/packages/sqldf/sqldf.pdf) package in `R`
# - Uses `SQLite` syntax [reference](https://pypi.org/project/pandasql/)

# In[319]:


from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())  
# globals b/c we're using variables defined in global scope, in notebook:


# In[320]:


pysqldf("""SELECT Origin,
                  Dest,
                  count(*) as n
           FROM df_origin_dest_LA
           GROUP BY Origin, Dest;""")


# Now you can run SQL queries against your `pandas` dataset.

# ### Reading-in Data from Database
# 
# Other ways to create `pandas` data frames, from:
# - lists and dictionaries: http://pbpython.com/pandas-list-dict.html
# - JSON (and other file formats), as we saw earlier today
# - direct pull from database
# 

# In[321]:


import sqlite3


# In[322]:


# Step 1: Connect to DB, per https://www.dataquest.io/blog/python-pandas-databases/
conn = sqlite3.connect("chinook.db")


# In[323]:


# Step 2: Execute query and send results to pandas dataframe:
df = pd.read_sql_query("""SELECT *
                          FROM artists
                          LIMIT 5;""",
                       conn)
df


# Now you can execute SQL queries against your database and send results to a `pandas` dataframe.
# 
# **TIP** To determine when to:
# - execute in database and pull-in results into `pandas` dataframe OR 
# - read into `pandas` datafrmae and then execute SQL commands
# 
# answer depends... on size of original dataset, (any) constraints on computational time for end-to-end analysis, etc. Please see [here](https://medium.com/carwow-product-engineering/sql-vs-pandas-how-to-balance-tasks-between-server-and-client-side-9e2f6c95677) for a more in-depth discussion.

# # Advanced `pandas`
# To be covered later in course, when we talk about applications of `pandas` to big data.
