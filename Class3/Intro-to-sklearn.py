#!/usr/bin/env python
# coding: utf-8

# # Iterative Model Development Steps with Application to Airlines Dataset
# - Steps are outlined in Class 3 [slide deck](http://bit.ly/2Gkl7ZB)
# - Link to airlines [dataset](https://github.com/h2oai/h2o-2/wiki/Hacking-Airline-DataSet-with-H2O)

# In[82]:


from collections import Counter
import inspect

from joblib import dump, load
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score, f1_score


# In[48]:


pd.options.display.max_columns = 50
pd.options.display.max_rows = 8


# ## Step 1: Understand Different Modeling Approaches
# - Model development is an art and science -- you may have done these steps differently. 
# - Please let us know what you would have done!

# ## Step 2: Understand Business Use Case
# Per [Class 0](http://bit.ly/2SPtCVi), proposed use case -- there may be (many) others:
# - **Client**: Airline
# - **Statement of Problem**: Airline has to compensate passangers if flight was delayed by 2+ hours or if flight arrived 3+ hours later.
# - **Key Business Question**: Are there (any) aspects of delayed + compensated flights that may be foreseen and potentially prevented, at scheduling time?
# - **Business impact of work**: (Conservative estimate) If we can reduce compensated delays by 1%, we reduce airline expenses by $300K/year

# - POC environment:
#   - Jupyter notebook
#   - Running Python 3.7
#   - requirements.txt

# - Outcome variable: (arrival delay of 3+ hours or departure delay of 2+ hours) or not, per [article](https://upgradedpoints.com/flight-delay-cancelation-compensation)

# ## Step 3: Get Access to Data

# ### Step 3-a: Read-in Data

# In[3]:


file_name = "https://s3.amazonaws.com/h2o-airlines-unpacked/year2012.csv"
df = pd.read_csv(filepath_or_buffer=file_name,
                 encoding='latin-1')
# df = pd.read_csv("2012.csv")


# ### Step 3-b: EDA of Data

# In[4]:


df.shape


# In[5]:


Counter(df['Month'])


# In[6]:


df.head()


# In[7]:


min(df['DepTime']), max(df['DepTime'])


# In[8]:


min(df['ArrTime']), max(df['ArrTime'])


# In[46]:


Counter(df['UniqueCarrier'])


# ## Step 4: Data Splits (later today)
# **Note**: It is best practice to:
# - *first* split the data, 
# - *then* transform variables on training data set and iron-out the POC model, 
# - *before* moving on to test model on test data set **once**
# 
# Because we're *only* transforming TOD, DOW and outcome on rules we decided *a priori*, this is OK. 
# 
# **Warning**: If our outcome variable was total compensation for plane delayed, which depended on size of place, we would have leakage if we created a binned outcome variable based on seeing *both* training and test set first. 

# ## Step 5: Feature Engineering for Baseline Model (v0)

# What potential features would we want to include in model?

# What features should we **not consider** for inclusion into model?

# ### Step 5-a: Create an Outcome Variable

# In[23]:


# Similar to function introduced in Class 2:

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


# In[15]:


df['compensated_delays'] = df[['ArrDelay', 'DepDelay']].apply(
    lambda row: delays_requiring_compensation(row[0], row[1]),
    axis=1)
df[['ArrDelay', 'DepDelay', 'compensated_delays']].head()


# In[24]:


Counter(df['compensated_delays'])


# Let's stop and think about this number... What are client implications?

# ### Step 5-b: Create a Time-of-Day Variable
# Per [documentation](http://stat-computing.org/dataexpo/2009/the-data.html) and EDA, time of day is recorded in hhmm.

# In[25]:
# Recall:
min(df['DepTime']), max(df['DepTime'])


# How is departure delay recorded?

# How would you convert this field to a time-of-day?


print(df['DepTime'][0])
str(int(df['DepTime'][0])).zfill(4)


# In[26]:


print(min(df['DepTime']))
str(int(min(df['DepTime']))).zfill(4)


# In[27]:


# Before processing all the values, assign missing values their own category:
df['DepTime'] = df['DepTime'].fillna(9999.0)


# In[55]:


df['Dep_Hour'] = df['DepTime'].apply(lambda x:
                                     int(
                                         str(int(x)).zfill(4)[0:2]
                                     ))


# In[56]:
# What would be a good comment to the code above?


df['Dep_Hour'].value_counts(sort=False)


# Does anything look weird?

# In[57]:


# Convert TOD for flights that departed at 24 hours to departing at TOD=0 hours:
row_index = np.where(df['Dep_Hour'] == 24)[0].tolist()
col_index = np.where(df.columns == 'Dep_Hour')[0].tolist()[0]
df.iloc[row_index, col_index] = 0


# In[58]:


df['Dep_Hour'].value_counts(sort=False)


# ### Step 3-c: Create Indicator Variables from Features for Use with Sklearn
# Features:
# - Month
# - Day of Week
# - Time of Day

# In[65]:


features_tod = pd.get_dummies(df['Dep_Hour'],
                              drop_first=True,
                              prefix="tod_")


# In[66]:


features_tod.head()


# In[67]:


features_month = pd.get_dummies(df['Month'],
                                drop_first=True,
                                prefix="mo_")


# In[68]:


features_dow = pd.get_dummies(df['DayOfWeek'],
                              drop_first=True,
                              prefix="dow_")


# In[69]:


features = pd.concat([features_tod, features_month, features_dow],
                     axis=1,
                     join='inner')


# In[70]:


features.columns


# In[75]:
# What is our baseline Month, DOW and TOD reference point?


dataset = pd.concat([features,
                     df['compensated_delays']],
                     axis=1)


# In[76]:


dataset.shape


# ## Step 4: Determine Data Splits
# What are some data splits that you would propose?

# In[77]:


df_tmp, df_test = train_test_split(dataset,
                                   test_size=0.25,
                                   random_state=2019,
                                   stratify=dataset['compensated_delays'])


# In[78]:


df_train, df_valid = train_test_split(df_tmp,
                                      test_size=0.25,
                                      random_state=2019,
                                      stratify=df_tmp['compensated_delays'])


# In[79]:
# What are the train, validation, test percentages here?


df_train['compensated_delays'].value_counts(sort=False)


# In[80]:


df_valid['compensated_delays'].value_counts(sort=False)


# In[81]:


df_test['compensated_delays'].value_counts(sort=False)


# ## Step 6: Estimate a Baseline Model (v0)

# In[83]:


y = df_train['compensated_delays']
X = df_train.drop(columns=['compensated_delays'])


# In[84]:


inspect.signature(LogisticRegression)


# In[103]:


est_model = LogisticRegression(penalty="l2",
                               C=0.5,
                               fit_intercept=True,
                               class_weight='balanced',
                               random_state=2019,
                               max_iter=10000,
                               solver='lbfgs')


# In[104]:


est_model


# In[ ]:


est_model.fit(X, y)


# In[88]:


# Save model, per: https://scikit-learn.org/stable/modules/model_persistence.html
dump(est_model, 'logistic.joblib')

## Load saved model:
# est_model = load('logistic.joblib') 


# Remarks:
# - Aside: creating a filename that includes a [timestamp](https://stackoverflow.com/questions/10607688/how-to-create-a-file-name-with-the-current-date-time-in-python)
# - Aside: If interested in seeing more `R`-like output for Logistic Regression, use library `statsmodels`
# - Logistic Regression with [Cross-Validation](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegressionCV.html)
# - (In general) Cross-Validation with sklearn: [approach 1](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html) and [approach 2](https://scikit-learn.org/0.16/modules/generated/sklearn.grid_search.GridSearchCV.html)

# ## Step 7: Interpret Results

# In[100]:
# DataFrame of feature coefficients:
coefficients = [round(x, 2) for x in est_model.coef_.tolist()[0]]
coef_df = pd.concat([pd.DataFrame(X.columns),
                     pd.DataFrame(coefficients)],
                    axis = 1)
coef_df.columns = ["feature_name", "coef_est"]

# DataFrame of intercept coefficient:
intercept_df = pd.DataFrame(["intercept", est_model.intercept_.tolist()[0]]).T
intercept_df.columns = ["feature_name", "coef_est"]

# Combined DataFrame:
coef_df = coef_df.append(intercept_df)
coef_df.head()




# In[ ]:
# Compute odds:
coef_df["odds"] = [round(np.exp(x), 2) for x in coef_df['coef_est']]




# In[ ]:
# Compute probabilities, which need intercept:
intercept = intercept_df['coef_est'].values.tolist()[0]
intercept


# More on odds vs probabilities [here](https://stats.idre.ucla.edu/stata/faq/how-do-i-interpret-odds-ratios-in-logistic-regression/)

# ![Inverse logit](./images/Inverse-logit.png)[Wikipedia](https://en.wikipedia.org/wiki/Logit)

def inverse_logit(intercept, coefficient):
    """Fcn to help calculate probability associated with flight delay,
       given our variable.
    """
    if coefficient == intercept:
        # Make sure we don't double-count the intercept:
        coefficient = 0
    inv_logit = np.exp(intercept + coefficient)/(1+np.exp(intercept + coefficient))
    return round(inv_logit, 2)
                           
coef_df["prob_delay"] = [inverse_logit(intercept, x) for x in coef_df['coef_est']]



coef_df.T


# How would you interpret the coefficients?

# Did we have a good reference point for comparison (of coefficients) for Month, DOW and TOD?

# What is a better reference point?

# Can be interpret the meaning of the TOD=-99?



# Duplicated to make it easier for interpretations:
coef_df.T


# **Interpretations:**
# Relative to midnight flights leaving on Mondays in January (e.g. intercept = baseline),
# - "Red eye" departures tends to increase odds of compensated delays for passengers
# - Flights over:
#   - Spring break or
#   - in summer or
#   - winter holidays
# tend to increase odds of compensated delays for passengers
# - Friday departures also tend to increase odds of compensated delays for passengers

# **How business will use (predicted) model to make decision(s):** e.g. Takeaways/Recommendations to your airline client?
# 

# **As a passenger, what's the best time to travel?**

# ## Step 8: Evaluate Performance

# In[ ]:
# ### Step 8a: Evaluate Performance on In-Sample Data
# Evaluate performance on in-sample data, to see wat the "best-possible" performance is, on data that the model's seen.
# 
# Aside: list available metrics available in `sklearn` [here](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics).



y_pred_train = est_model.predict(X)
y_pred_train[0:5]




y_pred_train_probs = pd.DataFrame(est_model.predict_proba(X))
y_pred_train_probs.head()


# #### Evaluate Performance via Confusion Matrix



inspect.signature(confusion_matrix)




confusion_matrix(y_true=y,
                 y_pred=y_pred_train)


# What does this confusion matrix tell us about our model?

# #### Evaluating Performance with AUC ROC



inspect.signature(roc_auc_score)




# Per documentation
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html#sklearn.metrics.roc_auc_score
# y_score can contain "probability estimates of the positive class":
roc_auc_score(y_true=y,
              y_score=y_pred_train_probs.iloc[:, 1])


# #### Evaluating Performance via F1



f1_score(y_true=y,
         y_pred=y_pred_train)


# Is our F1-score surprising?
# 

# ![F1-score](./images/f1-score.png)[reference](https://stackoverflow.com/questions/35365007/tensorflow-precision-recall-f1-score-and-confusion-matrix)

# Is our F1-score surprising?

# What do we think about the model?

# Should we evaluate out-of-sample performance?

# ### Step 8b: Evaluate Performance on Out-of-Sample Data



y_valid = df_valid['compensated_delays']
X_valid = df_valid.drop(columns=['compensated_delays'])




y_pred_valid = est_model.predict(X_valid)
y_pred_valid[0:5]




y_pred_valid_probs = pd.DataFrame(est_model.predict_proba(X_valid))
y_pred_valid_probs.head()


# Do you think we'll do better or worse or same?

# #### Evaluate Performance via Confusion Matrix



confusion_matrix(y_true=y_valid,
                 y_pred=y_pred_valid)


# #### Evaluating Performance with AUC ROC



roc_auc_score(y_true=y_valid,
              y_score=y_pred_valid_probs.iloc[:, 1])


# #### Evaluating Performance via F1



f1_score(y_true=y_valid,
         y_pred=y_pred_valid)


# How did out-of-sample compare?

# If this were a promising model, **what would the metric monitoring** look like?

# ## Step 9: Determine Next Steps

# What should the next model iteration focus on?
