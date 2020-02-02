#!/usr/bin/env python
# coding: utf-8

# # Iterative Model Development Steps with Application to Fashion-MNIST Dataset
# - Steps are outlined in https://goo.gl/A7P4vX
# - Link to Fashion-MNIST [dataset](https://github.com/zalandoresearch/fashion-mnist)

# ## Step 1: Understand Different Modeling Approaches
# - Model development is an art and science -- you may have done these steps differently. 
# - Please let us know what you would have done!

# In[1]:


# Standard libraries:
from collections import Counter
import inspect
import os

# Third-party libraries:
from joblib import dump, load
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score,                             mean_squared_error, roc_auc_score

# Custom libraries:
import network


# In[2]:


np.random.seed(2000)


# ## Step 2: Understand Business Use Case
# Proposed use case -- there may be (many) others:
# - *Client*: Online marketplace for buyers and sellers of retail goods
# - *Statement of Problem*: Marketplace allows sellers to upload goods and requires an item's description, that's indexed by the platform's search engine. 
# - *Question*: Can we improve search results by automatically tagging an item's category for the seller (and surfacing that tag to the platform's search engine)?
# - *Business Impact*: Improved search results may affect engagement, conversion and AOV. If AOV increases by 5%, assuming a `$40` AOV and `$200K` revenue/month, our work increases revenue by `$100K`/year.  

# What approach would you recommend?

# **Approach 1 (v0, today)**: Aim to derive tags based on item's image.

# **Approach 2 (outside scope of class)**: Aim to derive tags based on item's description.

# **Approach 3 (outside scope of class)**: Aim to derive tags based on ensemble of item's image and description.

# ## Step 3: Get Access to Data

# ### Step 3-a: Access Helper Function to Read-in Data
# To access the data set, we'll be following instructions under `Loading data with Python` section, outlined below:

# In[3]:


# Save location of notebook:
notebook_dir = os.getcwd()
notebook_dir


# **Step 1**: Clone Fashion-MNIST repo: https://github.com/zalandoresearch/fashion-mnist.git located [here](https://github.com/zalandoresearch/fashion-mnist)
# 
# **Step 2**: Specify path to this direcotry on your local machine:

# In[4]:


# Path to repository on my machine:
fashion_mnist_dir = "/Users/irina/Documents/Stats-Related/Fashion-MNIST-repo"


# **Step 3**: Change directories to the repository on your local machine:

# In[5]:


os.chdir(fashion_mnist_dir)


# **Step 4**: Import the helper function to read-in the data

# In[6]:


from utils import mnist_reader


# ### Step 3-b: Read-in Data
# Read-in the data using the helper function of data set's repository.

# In[7]:


X_train, y_train = mnist_reader.load_mnist('data/fashion', kind='train')
X_test, y_test = mnist_reader.load_mnist('data/fashion', kind='t10k')


# In[8]:


X_train.shape


# Prevent overflow of computation by dividing by the max value of scale, to be on 0-1 scale, not 0-255:
X_train_normalize = [x/256.0 for x in X_train]
# In[9]:


X_test.shape


# In[10]:


Counter(y_train)


# In[11]:


# Create dictionary of outcome variable labels, per repository:
label_dict = {
    0: "T-shirt/top",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Ankle boot"
}


# ### Step 3-c: EDA of Data

# In[12]:


def visualize_image(dataset_x, dataset_y, img_index, y_labels=label_dict):
    """Helper function to visualize image and associated label, for
       specified image in index.
       ---
       Note: Assume image size is 28 x 28.
    """
    plt.imshow(dataset_x[img_index].reshape(28, 28),
               cmap='Greys')
    print(y_labels[dataset_y[img_index]])


# In[13]:


visualize_image(X_train_normalize, y_train, 0)


# In[14]:


visualize_image(X_train_normalize, y_train, 10)


# ## Step 4: Determine Data Splits
# What are some data splits that you would propose?

# In[15]:


# Add outcome column to data set of features, to be able to split dataset
# into training and validation, statifying by outcome variable:
df_tmp = pd.concat([pd.DataFrame(X_train_normalize),
                    pd.DataFrame(y_train, columns=["outcome"])], axis=1)
df_tmp.columns


# In[16]:


df_train, df_valid = train_test_split(df_tmp,
                                      test_size=0.25,
                                      random_state=2019,
                                      stratify=df_tmp['outcome'])


# In[17]:


df_train['outcome'].value_counts(sort=False)


# In[18]:


df_valid['outcome'].value_counts(sort=False)


# In[ ]:


Counter(y_test)


# ## Step 5: Feature Engineering

# Baseline model (v0) will use raw images as features.

# Using this assumptions, how many features are there per image?

# ## Step 6: Estimate a Baseline Model (v0)

# In[ ]:


y = df_train['outcome']
X = df_train.drop(columns=['outcome'])


# In[ ]:


X.shape


# In[ ]:


inspect.signature(RandomForestClassifier)


# In[ ]:


### --- Step 1: Specify different number of trees in forest, to determine
###             how many to use based on leveling-off of OOB error:
n_trees = [50, 100, 250, 500, 1000, 1500, 2500]


# In[ ]:


### --- Step 2: Create dictionary to save-off each estimated RF model:
rf_dict = dict.fromkeys(n_trees)


# In[ ]:


for num in n_trees:
    print(num)
    ### --- Step 3: Specify RF model to estimate:
    rf = RandomForestClassifier(n_estimators=num,
                                min_samples_leaf=30,
                                oob_score=True,
                                random_state=2019,
                                class_weight='balanced',
                                verbose=1)
    ### --- Step 4: Estimate RF model and save estimated model:
    rf.fit(X, y)
    rf_dict[num] = rf


# *Note:* We could have used [`GridSearchCV`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html#sklearn.model_selection.GridSearchCV) to perform the optimization, but `GridSearchCV` performs 2+ Fold Cross-Validation that's repeated 3 times.

# In[ ]:


### --- Save-off model:
# Specify location and name of object to contain estimated model:
model_object_path = os.path.join(notebook_dir, 'rf.joblib')
# Save estimated model to specified location:
dump(rf_dict, model_object_path) 

# Load model:
# rf_dict = load(model_object_path) 


# In[ ]:


# Compute OOB error per
# https://scikit-learn.org/stable/auto_examples/ensemble/plot_ensemble_oob.html
oob_error_list = [None] * len(n_trees)

# Find OOB error for each forest size:
for i in range(len(n_trees)):
    oob_error_list[i] = 1 - rf_dict[n_trees[i]].oob_score_
else:
    # Visulaize result:
    plt.plot(n_trees, oob_error_list, 'bo',
             n_trees, oob_error_list, 'k')


# How many trees are enough for our forest?

# # Step 7: Interpret Results

# In[ ]:


# Feature importance plot, modified from: 
# https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html
top_num = 20
forest = rf_dict[500]
importances = forest.feature_importances_

# Sort in decreasing order:
indices = np.argsort(importances)[::-1]


# In[ ]:


# Plot the feature importances of the forest
ax = plt.gca()
plt.title(f"Top {top_num} feature importances")
plt.bar(range(top_num), importances[indices[0:top_num]])
plt.xticks(range(top_num))
ax.set_xticklabels(indices[0:top_num], rotation = 90)
ax.set_xlabel("Pixel position in image")
ax.set_ylabel("Feature Importance")
plt.show()


# How can you decided how many top X features are important?

# ## Step 8: Evaluate Performance

# ### Step 8a: Evaluate Performance on In-Sample Data
# Evaluate performance on in-sample data, to see wat the "best-possible" performance is, on data that the model's seen.
# 

# In[ ]:


y_pred_train = forest.predict(X)
y_pred_train[0:5]


# In[ ]:


y_pred_train_probs = pd.DataFrame(forest.predict_proba(X))
y_pred_train_probs.head()


# #### Evaluate Performance via Confusion Matrix

# In[ ]:


conf_mat = confusion_matrix(y_true=y,
                            y_pred=y_pred_train)
conf_mat


# In[ ]:


# To have columns be in correct order:
class_names = [label_dict[x] for x in range(10)]


# In[ ]:


conf_df = pd.DataFrame(conf_mat, class_names, class_names)
conf_df


# In[ ]:


conf_df_pct = conf_df/conf_df.sum(axis=1)
round(conf_df_pct, 2)


# What does the confusion matrix tell us about our model?

# Aside:
# - `seaborn` [gallery](https://seaborn.pydata.org/examples/index.html) for visualizations
# - [Conditional highlighting](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html) of pandas dataframes

# #### Evaluate Performance via F1-score
# We have a multi-class outcome, let's use an associated F1-score, per:
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html and https://medium.com/@ramit.singh.pahwa/micro-macro-precision-recall-and-f-score-44439de1a044

# In[ ]:


# Class-level performance:
f1_score(y_true=y,
         y_pred=y_pred_train,
         average='macro')


# In[ ]:


# Overall performance across all classes:
f1_score(y_true=y,
         y_pred=y_pred_train,
         average='micro')


# Is our F1-score surprising?

# What do we think about the model?

# # Step 9: Fit An Alternative Model (v1)
# **Alternative Model**: Estimate a fully connected neural network with 1 hidden layer to try ot predict category of image... in (base) Python (!).
# 
# **Motivation**: 
# - Aim to understand what's happening behind-the-scenes with simple NN model first
# - Learning + practicing concepts, not syntax
# - Easier to debug

# # Before we tackle Neural Networks in (base) Python... Brief Introduction to OOP  
# Reference: https://realpython.com/python3-object-oriented-programming/

# - **Procedural programming**
#   - e.g. this notebook
# - **Object Oriented Programming (OOP)**
#   - e.g. person, with behaviors such as 'attending class'
# - OOP components:
#   - Classes contain properties (e.g. 'attending class')
#   - Instance of class (e.g. person 1, person 2, etc.)
#   - Class inheritance (outside scope of today's lecture)
# 

# In[ ]:


class Person():
    """Class person"""
    
    def __init__(self, name):
        """Class requires that each Person has a name."""
        self.name = name


# In[ ]:


instructor = Person('Irina')
instructor.name


# In[ ]:


TA = Person('Hao')
TA.name


# In[ ]:


type(instructor)


# # 10 minute break

# # (Back to) Step 9: Fit An Alternative Model (v1)
# Reference: http://neuralnetworksanddeeplearning.com/chap1.html and
# simplified `network.py` code from repository:
# https://github.com/mnielsen/neural-networks-and-deep-learning/blob/master/src/network.py
# 

# In[ ]:


X = X.reset_index(drop=True)
y = y.reset_index(drop=True)


# #### Reshape Dataset to Format Expected by Fully Connected NN
# Format:
# - list of same length as number of images in (training) data set
# - each entry in list is a tuple of length 2, containing (features, outcome) of a given image
# - features are an 784 x 1 Numpy Ndarray
# - outcome is 10 x 1 Numpy Ndarray

# In[ ]:


num_rows = X.shape[0]
training_data = [None]*num_rows
for i in range(num_rows):
    if i % 15000 == 0:
        print(i)
    # Create ndarray for each row of X:
    tmp_x = pd.DataFrame(X.iloc[i]).values
    # Create ndarray of length 10 for each value of y:
    tmp_y = pd.DataFrame(np.zeros(10)).values
    tmp_y[y[i]] = y[i]
    # Create tuple for each image:
    training_data[i] = (tmp_x, tmp_y)


# In[ ]:


# type(training_data)
training_object_path = os.path.join(notebook_dir, 'training_data.joblib')
dump(training_data, training_object_path) 


# In[ ]:





# #### Define the Fully Connected NN and its Estimation
# - Please see `network.py` in this repository for commented version of the code.

# In[ ]:
# < Walk through of network.py>



# Network specs: 
#     28*28 neurons in input layer, 
#     30 in hidden layer, 
#     predicting 1 of 10 classes in output layer:
net = network.Network([784, 30, 10])


# In[ ]:


res = net.SGD(training_data, learning_rate=3.0)


# Accuracy at convergence:
# ![NN convergence](./images/NN-convergence.png)

# Is convergence monotonic?
# #### Ad-hoc (Mis)classifications Check

# In[ ]:


img_number = 10
res[img_number].round(2)


# In[ ]:


img_number = 0
predicted = label_dict[np.argmax(res[img_number])]
observed = label_dict[y[img_number]]
(predicted, observed)


# #### Evaluate Performance via Confusion Matrix

# In[ ]:


y_pred_train_nn = [np.argmax(x) for x in res]


# In[ ]:


conf_mat_nn = confusion_matrix(y_true=y,
                               y_pred=y_pred_train_nn)
conf_mat_nn


# In[ ]:


conf_df_nn = pd.DataFrame(conf_mat_nn, class_names, class_names)
conf_df_pct_nn = conf_df_nn/conf_df_nn.sum(axis=1)
round(conf_df_pct_nn, 2)


# In[ ]:
# Anything jump out as reasonable misclassification?

# Anything jump out as egregious misclassification?


# Compare with confusion matrix from RF:
round(conf_df_pct, 2)


# Should we refactor this code:
# ```
# conf_df_nn = pd.DataFrame(conf_mat_nn, class_names, class_names)
# conf_df_pct_nn = conf_df_nn/conf_df_nn.sum(axis=1)
# round(conf_df_pct_nn, 2)
# ```
# into a function?

# #### Evaluate Performance via F1-score

# In[ ]:


# Class-level performance:
f1_score(y_true=y,
         y_pred=y_pred_train_nn,
         average='macro')


# In[ ]:


# Class-level performance:
f1_score(y_true=y,
         y_pred=y_pred_train_nn,
         average='micro')


# Are we suprised by these results?

# What do we think about the model?

# ![Warning](./images/warning.png) Just because we iterated on the model, model improvement is not guaranteed (!).

# Should we ensemble current NN with RF model? Why?

# What are some approaches to improve NN model performance?

# What are alternative approaches for next model iteration?

# # Back to the Business Question

# **Use case**: Help tag item category to improve search results.

# Models are not perfect and model may make a mistake. Let's think about misclassification rate... Which is more costly to seller?

# Which is more costly to buyer?

# Ideas to improve recommendations using current model framework (RF or NN)?

# Hint: can we leverage probabilities?

# Hint: can we leverage category hierarchy?
