#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import Counter
import copy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import multivariate_normal
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


np.random.seed(2021)


# ### Step 1: Simulation of highly collinear 
# Simulation adapted from [scipy documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.multivariate_normal.html) and [SO](https://stackoverflow.com/questions/16024677/generate-correlated-data-in-python-3-3):

# In[3]:


mean = np.array([0.5, 0.5])
corr = np.array([[1, 0.99], [0.99, 1]])


# In[4]:


x = np.random.multivariate_normal(mean,
                                  corr,
                                  size=100)
y = np.random.binomial(n=1,
                       p=.5,
                       size=100)


# In[5]:


# Check correlations of simulated data:
np.corrcoef(x[:, 0], x[:, 1])


# In[6]:


Counter(y)


# In[7]:


X = pd.DataFrame(x, columns=["var1", "var2"])
# Create interaction term:
X["var1_x_var2"] = X["var1"] * X["var2"]


# In[8]:


# X.head()


# In[9]:


y = pd.Series(y)


# In[10]:


pd.DataFrame(np.corrcoef(X.T.values))


# ### Step 2: Model Estimation with Collinear Data

# In[11]:


def est_logistic_coeff(data_X, data_y, random_seed):
    #
    # Specify logistic model without regularization:
    est_logistic_model = LogisticRegression(penalty="none",
                                            fit_intercept=True,
                                            random_state=random_seed,
                                            solver='lbfgs')
    #
    # Estimate model:
    est_logistic_model.fit(data_X, data_y)
    #
    # Calculate coefficients:
    coefficients = [round(x, 2) for x in est_logistic_model.coef_.tolist()[0]]
    coef_df = pd.concat([pd.DataFrame(data_X.columns),
                         pd.DataFrame(coefficients)],
                        axis = 1)
    coef_df.columns = ["feature_name", "coef_est"]
    return coef_df


# In[12]:


est_logistic_coeff(X, y, random_seed=1)


# In[13]:


est_logistic_coeff(X, y, random_seed=2021)


# Note: Expected behavior per [Cross Validated](https://stats.stackexchange.com/questions/116804/coefficient-changes-sign-when-adding-a-variable-in-logistic-regression): coefficients switch signs. 

# In[14]:


def est_rf_importances(data_X, data_y, random_seed):
    #
    # Specify RF model:    
    est_rf_model = RandomForestClassifier(n_estimators=500,
                                          min_samples_leaf=30,
                                          oob_score=True,
                                          random_state=random_seed,
                                          class_weight='balanced',
                                          verbose=1)
    #
    # Estimate model:
    est_rf_model.fit(data_X, data_y)
    # 
    # Find most important features:
    importances = est_rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    #
    # Per https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html
    for feature in range(data_X.shape[1]):
        print("%d. feature %d (%f)" % (feature + 1, indices[feature], importances[indices[feature]]))


# In[15]:


est_rf_importances(X, y, random_seed=100)


# In[16]:


est_rf_importances(X, y, random_seed=2019)


# Note: RF accounts for interactions.
