#!/usr/bin/env python
# coding: utf-8

# # Introduction to AWS Simple Cloud Storage Service (S3)
# Prerequisites:
# - Installation of `boto3`
# - Creating and adding AWS credentials to `.aws/credentials` file
# - Creating and adding AWS region for computing resources in `.aws/config` file

# In[39]:


import boto3
import joblib
import pandas as pd

# Documentation: https://s3fs.readthedocs.io/en/latest/?badge=latest
# Note: s3fs is a wrapper for boto3
import s3fs 


# Specify name of AWS S3 bucket you created:
bucket_name = "stats404-project"
# ## Connect to S3 Bucket on AWS

# In[40]:


# Approach 1: 
s3 = boto3.resource('s3')

# Approach 2:
# - anon=False: use AWS credentials to connect to file system, not as an anonymous user
s3_fs = s3fs.S3FileSystem(anon=False)


# View list of all buckets available on AWS. Note: These are mine -- yours will differ:
# 

# In[36]:


for bucket in s3.buckets.all():
    print(bucket.name)


# View list of objects in given bucket:

# In[21]:


for file in s3.Bucket(bucket_name).objects.all():
    print(file.key)


# ## Upload CSV File to S3 Bucket

# In[11]:


# --- Step 1: Create a data set to upload -- or use one for your project:
file_name = "https://s3.amazonaws.com/h2o-airlines-unpacked/year1987.csv"
df = pd.read_csv(filepath_or_buffer=file_name,
                 encoding='latin-1',
                 nrows=1000
                )


# In[24]:



# --- Step 3: Specify name of file to be created on s3, to store this CSV:
key_name = "airlines_data_1987_1000rows.csv"

# --- Step 4: Upload file to bucket and file name specified: 
with s3_fs.open(f"{bucket_name}/{key_name}","w") as file:
    df.to_csv(file)


# In[25]:


# --- Step 5: Check that file got uploaded:
for file in s3.Bucket(bucket_name).objects.all():
    print(file.key)


# ## Upload Model Object to S3 Bucket

# In[27]:


# --- Step 1: Load a previously estimated model object in workspace:
rf_dict = joblib.load("../Class4/rf.joblib") 

# --- Step 2: Keep bucket the same


# In[33]:


# --- Step 3: Specify name of file to be created on s3, to store this model object:
key_name = "rf_Fashion_MNIST_500_trees.joblib"

# --- Step 4: Upload file to bucket and file name specified:
with s3_fs.open(f"{bucket_name}/{key_name}","wb") as file:
    joblib.dump(rf_dict[500], file) 


# In[41]:


# --- Step 5: Check that file got uploaded:
for file in s3.Bucket(bucket_name).objects.all():
    print(file.key)


# On AWS, our bucket would look like this:

# ![AWS_bucket](./images/bucket.png)
