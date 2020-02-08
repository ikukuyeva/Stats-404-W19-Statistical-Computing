#!/usr/bin/env python
# coding: utf-8

# # Speeding-Up Computations
# **Please Note**: Approaches presented in each section are listed in no particular order -- some (or many) may work better for your use case; performance of approach may differ on data set, where it's hosted, computing resources, etc.

# In[156]:


from collections import Counter
import dask.dataframe as dd
import inspect
from joblib import Parallel, delayed
import numpy as np
import os
import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier


# [Timing results](https://stackoverflow.com/questions/17579357/time-time-vs-timeit-timeit): `%%time` and `%%timeit`

# ## Speeding-up Data Read

# In[2]:


file_name = "https://s3.amazonaws.com/h2o-airlines-unpacked/year2012.csv"


# In[3]:


get_ipython().run_cell_magic('time', '', 'df = pd.read_csv(filepath_or_buffer=file_name,\n                 encoding=\'latin-1\'\n                )\n# df = pd.read_csv("../Class3/2012.csv")')


# Parsing output, per [SO](https://stackoverflow.com/questions/556405/what-do-real-user-and-sys-mean-in-the-output-of-time1/556411#556411):
# - **Wall time**: "time from start to finish of the call". 
# - **User time**: CPU time outside the kernel within the process, such as in library code. 
# - **Sys time**: CPU time inside the kernel within the process. 
# - **User + Sys time**: how much actual CPU time your process used. 

# In[5]:


df.shape


# In[123]:


get_ipython().run_cell_magic('time', '', 'df["UniqueCarrier"].value_counts(sort=False)')


# Recode missing values to large negative # as compensated delays are large positive #s:
df["DepDelay"] = df["DepDelay"].fillna(-9999)
df["ArrDelay"] = df["ArrDelay"].fillna(-9999)
# ### 1. `pandas` - Read File in Chunks
# [Reference](https://towardsdatascience.com/why-and-how-to-use-pandas-with-large-data-9594dda2ea4c)

# In[7]:


get_ipython().run_cell_magic('time', '', "# Create an object for iteration over, to spead-up read-ing process:\ndf_chunked = pd.read_csv(filepath_or_buffer=file_name,\n                         encoding='latin-1',\n                         chunksize=1000000)\n\n# Create a list to store data set chunks:\nchunk_list = []\n\n\n# Each chunk is in df format\nfor chunk in df_chunked:  \n    chunk_list.append(chunk)\nelse:\n    # concat the list into dataframe \n    df = pd.concat(chunk_list)")


# ### 2. (If Possible) Perform in-database Computations
# - **Approach** (if possible), as we did in [Class 2](https://goo.gl/JkLxHq):
#   1. Connect script to database
#   2. Perform aggregations and variable transformations in-database
#   3. Send results back to script
# - **Please note**, this may not be possible, because:
#   - data is not in database to begin with, or
#   - time to put data into database to aggegate in, is too time consuming, or
#   - you're querying a production database -- and running this query may slow-down performance of services running in production that depend on this database

# ### 3. `dask` -- Read File as is
# [Documentation](http://docs.dask.org/en/latest/) and more [examples](https://www.analyticsvidhya.com/blog/2018/08/dask-big-datasets-machine_learning-python/)

# In[129]:


get_ipython().run_cell_magic('timeit', '', "dd.read_csv(file_name, encoding='latin-1')")


# In[136]:


get_ipython().run_cell_magic('time', '', "df_dask = dd.read_csv(file_name,\n                      encoding='latin-1',\n                      assume_missing=True)")


# ### 4. `pySpark` -- Read File as is
# [Documentation](https://spark.apache.org/docs/2.2.0/) and more examples of Airlines data set [analysis](https://github.com/goldshtn/spark-workshop/blob/master/scala/lab2-airlines.md) in `pySpark`

# Please go this [Databricks notebook](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/2873656090782679/2252219718088020/7574928746777728/latest.html) to view `pySpark` code that reads-in Airlines dataset.

# Time duration (seconds) = 90 seconds (0.02 to get `file_name`, 60.02 to read into DBFS and 29.93 to read into notebook)

# To run the code, you'll need a Databricks account (see class slides on instructions) to `Import Notebook` into. (`Import Notebook` prompt is at top-right of screen of the [Databricks notebook](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/2873656090782679/2252219718088020/7574928746777728/latest.html))

# ### Which was the fastest for reading-in Airlines data set?

# ## Speeding-Up Data Munging

# ### 1. `pandas`
# Suggested (non-exhaustive) list of approaches:
# - Pre-allocate (vs `append()` to) lists, etc.
# - Drop [unnecessary columns](https://realpython.com/python-data-cleaning-numpy-pandas/#dropping-columns-in-a-dataframe)
# - Create a better index for [faster subsetting](https://realpython.com/python-data-cleaning-numpy-pandas/#changing-the-index-of-a-dataframe)
# - Type optimization of variables in dataset, per [this](https://www.dataquest.io/blog/pandas-big-data/) and [this](https://medium.com/@vincentteyssier/optimizing-the-size-of-a-pandas-dataframe-for-low-memory-environment-5f07db3d72e) blog post
# - Saving intermediate results in HDF5 store, per Wes McKinney's book [Python for Data Analysis](http://wesmckinney.com/pages/book.html) and this [blog post](https://realpython.com/fast-flexible-pandas/#prevent-reprocessing-with-hdfstore)

# #### a. `for-loop` versus `apply()` versus `applymap()` versus `cut()`

# **Goal** [as in Class 2](https://github.com/ikukuyeva/Stats-404-W19-Statistical-Computing/blob/master/Class2/Intro-to-pandas.ipynb): Convert delays from minutes to hours

# In[9]:


num_rows = df.shape[0]
dep_delay_hr = [None] * num_rows
col_index = np.where(df.columns == 'DepDelay')[0].tolist()[0]


# In[10]:


get_ipython().run_cell_magic('time', '', 'for i in range(num_rows):\n    dep_delay_hr[i] = df.iloc[i, col_index]/60.0')


# In[11]:


get_ipython().run_cell_magic('time', '', "dep_delay_hr_apply = df['DepDelay'].apply(lambda x: x/60.0)")


# In[12]:


get_ipython().run_cell_magic('timeit', '', "delay_hr_apply = df[['DepDelay', 'ArrDelay']].apply(lambda x: x/60.0)")


# In[13]:


get_ipython().run_cell_magic('timeit', '', "delay_hr_applymap = df[['DepDelay', 'ArrDelay']].applymap(lambda x: x/60.0)")


# ### Which was the fastest for converting minutes to hours?

# **Goal** [as in Class 2](https://github.com/ikukuyeva/Stats-404-W19-Statistical-Computing/blob/master/Class2/Intro-to-pandas.ipynb): Convert continuous variable into categorical

# In[56]:


def bin_departure_delays(delay_min):
    if (delay_min >= -60.0) & (delay_min < 15.0):
        return "no_delay"
    elif (delay_min >= 15.0) & (delay_min < 30.0):
        return "small_delay"
    elif (delay_min >= 30.0) & (delay_min < 60.0):
        return "medium_delay"        
    elif (delay_min >= 60.0) & (delay_min < 120.0):
        return "big_delay"        
    elif (delay_min >= 120.0):
        return "compensated_delay"        
    else:
        return "missing_delay"


# In[57]:


get_ipython().run_cell_magic('time', '', "delay_bin = df['DepDelay'].apply(lambda x: bin_departure_delays(x))")


# In[58]:


delay_bin.value_counts()


# In[59]:


get_ipython().run_cell_magic('time', '', 'delay_bin_cut = pd.cut(df[\'DepDelay\'],\n                       bins=[-10000, -60.0, 15, 30, 60, 120, 3000],\n                       labels=["missing_delay", "no_delay", "small_delay", "medium_delay", "big_delay", "compensated_delay"],\n                       include_lowest=True,\n                       right=False)')


# In[60]:


delay_bin_cut.value_counts()


# More [examples](https://realpython.com/fast-flexible-pandas/)
# 

# ### Which was the fastest for binning departure delays?

# #### b. Vectorization

# Visual explanation of [vectorization:](https://datascience.blog.wzb.eu/2018/02/02/vectorization-and-parallelization-in-python-with-numpy-and-pandas/)
# 
# ![Visual explanation of what vectorization is](./images/vectorization.png)
# 

# **Goal** [As in Class 3](https://github.com/ikukuyeva/Stats-404-W19-Statistical-Computing/blob/master/Class3/Intro-to-sklearn.ipynb): Create outcome variable for compensated delay

# In[110]:


def delays_requiring_compensation(arrival_delay, departure_delay):
    """Fcn to return if arrival and/or departure delay resulted in passenger
       compensation.
       
       Arguments:
           - arrival_delay:   delay in minutes
           - departure_delay: delay in minutes
       
       Returns:
           - number of delays (arrival and or departure) that were delayed
             so long that passenger got compensated
    """
    count = 0
    if (arrival_delay/60.0 >= 3) | (departure_delay/60.0 >= 2):
        # If arrival delay is 3+ hours, or if departure delay is 2+ hours:
        count += 1
    return count


# In[63]:


get_ipython().run_cell_magic('time', '', "df['compensated_delays'] = df[['ArrDelay', 'DepDelay']].apply(\n    lambda row: delays_requiring_compensation(row[0], row[1]),\n    axis=1)")


# In[111]:


Counter(df['compensated_delays'])


# Prerequisite for vectorizing with Boolean logic:

# In[98]:


print(True | True)
print(True | False)
print(False | True)
print(False | False)


# In[113]:


def delays_requiring_compensation_vec(arrival_delay, departure_delay):
    """Fcn to return if arrival and/or departure delay resulted in passenger
       compensation.
       
       Arguments:
           - arrival_delay:   delay in minutes
           - departure_delay: delay in minutes
       
       Returns:
           - number of delays (arrival and or departure) that were delayed
             so long that passenger got compensated
    """
    count_arrival_delays = arrival_delay >= (3 * 60.0)
    count_departure_delays = departure_delay >= (2 * 60.0)
    # Leveraging Boolean logic:
    compensated_delays = count_arrival_delays | count_departure_delays
    return compensated_delays


# In[114]:


get_ipython().run_cell_magic('time', '', "df['compensated_delays_vec'] = delays_requiring_compensation_vec(df['ArrDelay'], \n                                                                 df['DepDelay'])")


# In[115]:


Counter(df['compensated_delays_vec'])


# More [examples](https://engineering.upside.com/a-beginners-guide-to-optimizing-pandas-code-for-speed-c09ef2c6a4d6)
# 

# #### c. `numpy` Operations via `.values`

# In[120]:


type(df['ArrDelay'])


# In[121]:


type(df['ArrDelay'].values)


# In[118]:


get_ipython().run_cell_magic('time', '', "df['compensated_delays_vec_np'] = delays_requiring_compensation_vec(df['ArrDelay'].values, \n                                                                    df['DepDelay'].values)")


# In[119]:


Counter(df['compensated_delays_vec_np'])


# More examples: [here](https://engineering.upside.com/a-beginners-guide-to-optimizing-pandas-code-for-speed-c09ef2c6a4d6) and [here](https://jakevdp.github.io/PythonDataScienceHandbook/02.04-computation-on-arrays-aggregates.html)

# ### Which was the fastest for processing multiple columns?

# What does the difference in counts between `(a)` and ( `(b)` or `(c)` ) tell us about the nature of delays?

# ### 2. In-database Computations
# Please see Section "Speeding-up Data Read" (above) for more information and caveats. 

# ### 3. `dask`

# In[141]:


get_ipython().run_cell_magic('time', '', "df_dask['UniqueCarrier'].value_counts().compute()")


# ![Warning](./images/warning.png) Per [bug submission](https://github.com/dask/dask/issues/442), while Dask's `value_counts()` [documentation](http://docs.dask.org/en/latest/dataframe-api.html) states that you can sort results as in `pandas`, Dask does not have that functionality implemented.

# ### 4. `pySpark` + `SparkSQL`
# Please go this [Databricks notebook](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/2873656090782679/2252219718088020/7574928746777728/latest.html) to view `SparkSQL` code that performs counts by airline carrier for Airlines dataset.

# Time duration (seconds) = 7.35 seconds (0.05 s to specify that we'll be running SparkSQL against dataset, 7.33 s to perform aggregation)

# ### Which was the fastest for getting number of flight paths by carrier?

# ## Speeding-up Embarrassingly Parallel Steps

# From [Class 4](https://github.com/ikukuyeva/Stats-404-W19-Statistical-Computing/blob/master/Class4/Fashion-MNIST.ipynb): We estimated 7 different Random Forest models in serial.

# In[152]:


# Path to repository on my machine:
fashion_mnist_dir = "/Users/irina/Documents/Stats-Related/Fashion-MNIST-repo"
os.chdir(fashion_mnist_dir)


# In[ ]:


# Load Fashion-MNIST data set using helper function from Fashion-MNIST repository:
from utils import mnist_reader
# Load 10K images for this demo:
X, y = mnist_reader.load_mnist('data/fashion', kind='t10k')


# In[162]:


rf_base = RandomForestClassifier(n_estimators=500,
                                 min_samples_leaf=30,
                                 oob_score=True,
                                 random_state=2019,
                                 class_weight='balanced',
                                 verbose=1).fit(X, y)


# #### a. (Potentially) Leverage Parralel Backend of `sklearn` model
# Example: `sklearn` RF model

# In[147]:


inspect.signature(RandomForestClassifier)


# Per sklearn documentation of [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html):
# 
# `n_jobs` : int or None, optional (default=None)
# 
# The number of jobs to run in parallel for **both fit and predict**. None means 1 unless in a joblib.parallel_backend context. 
# -1 means using all processors...
# 
# Note: Parallel backend is [joblib](https://joblib.readthedocs.io/en/latest/parallel.html#joblib.parallel_backend)

# In[164]:


rf_base_parallel2 = RandomForestClassifier(n_estimators=500,
                                 min_samples_leaf=30,
                                 oob_score=True,
                                 random_state=2019,
                                 class_weight='balanced',
                                 verbose=1,
                                 n_jobs=2).fit(X, y)


# How much speed-up did we get by using 2 cores?

# In[165]:


rf_base_parallel4 = RandomForestClassifier(n_estimators=500,
                                 min_samples_leaf=30,
                                 oob_score=True,
                                 random_state=2019,
                                 class_weight='balanced',
                                 verbose=1,
                                 n_jobs=4).fit(X, y)


# Why is speed-up not 4x?

# #### b. `joblib` for Embarrassingly Parallel Computations

# In[171]:


def rf_spec(num_trees, features=X, outcome=y):
    ### --- RF model to estimate:
    rf = RandomForestClassifier(n_estimators=num_trees,
                                min_samples_leaf=30,
                                oob_score=True,
                                random_state=2019,
                                class_weight='balanced',
                                verbose=1)
    ### --- Estimate RF model and save estimated model:
    rf.fit(features, outcome)
    return rf


# In[154]:


n_trees = [50, 100, 250, 500, 1000, 1500, 2500]


# ##### Baseline for Estimating 7 RFs

# In[172]:


for num_trees in n_trees:
    rf_spec(num_trees)


# ##### Leveraging Parallelization to Estimate Forests Simultaneously

# In[174]:


# Per http://academic.bancey.com/parallelization-in-python-example-with-joblib/
results = Parallel(n_jobs=4, verbose=1, backend="threading")(map(delayed(rf_spec), n_trees))


# #### Which is fastest for parallelizing RF model estimation?

# Aside: [Explanation](https://stackoverflow.com/questions/42220458/what-does-the-delayed-function-do-when-used-with-joblib-in-python) of `delayed` argument

# # Key Takeaways

# - There is no clear tech stack winner for which solution will speed-up computations for each use case; speed depends on:
#   - size of dataset
#   - analyses you want to perform
#   - computing architecture
#   - (many others)
#  
#  
# - Airlines data set (using 2012 flight paths only) might be too small for our pySpark cluster

# # Further Reading
# - [High Performance Python](http://shop.oreilly.com/product/0636920028963.do)
#   - Appropriate usage of lists vs tuples 
#   - Iterators and Generators
#   - Compiling to C
#   - (more on) Cluster Computing
