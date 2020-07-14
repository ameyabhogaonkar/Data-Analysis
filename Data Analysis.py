#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import os


# In[27]:


# MERGE ALL 12 MONTHS DATA

files = [file for file in os.listdir("E:\python-ethans\Sales_Data")]
# print(files)

all_months_data = pd.DataFrame()  # space for new file

for file in files:
    df = pd.read_csv("E:\python-ethans\Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data, df])

all_months_data.to_csv("E:\python-ethans\Pandas project\ll_data.csv", index=False)


# In[28]:


all_data = pd.read_csv("E:\python-ethans\Pandas project\ll_data.csv")
all_data.head()


# In[30]:


#CLEAN DATA LIKE DROP NAN ROW

nan_df = all_data[all_data.isna().any(axis=1)] #it will show u NaN data
nan_df.head()

all_data = all_data.dropna(how='all')
all_data.head()


# In[32]:


all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']  #TO REMOVE 'OR' ERROR


# In[36]:


#CONVERT COLUMN INTO CORRECT DATATYPE

all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])
all_data.head()


# In[33]:


#ADD MONTH COLUMN

all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# In[37]:


#ADD SALES COLUMN

all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.head()


# In[44]:


# Task 1 - WHAT WAS THE BEST MONTH FOR SALES?HOW MUCH WAS EARNED THAT MONTH?

result = all_data.groupby('Month').sum()
#result


# In[51]:


import matplotlib.pyplot as plt

months = range(1,13)

plt.bar(months,result['Sales']) #bar(x-axis,y-axis)
plt.xticks(months)
plt.ylabel('sales')
plt.xlabel('months')
plt.show()


# #TASK 2- WHAT CITY HAD THE HIGHEST NO OF SALES

# In[53]:


# ADD CITY COLUMN
# LET'S USE .apply()

def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")
all_data.head()


# In[55]:


#TASK 2- WHAT CITY HAD THE HIGHEST NO OF SALES

result = all_data.groupby('City').sum()
result


# In[61]:


import matplotlib.pyplot as plt

cities = [city for city,df in all_data.groupby('City')]

plt.bar(cities,result['Sales'])
plt.xticks(cities,rotation ='vertical')
plt.xlabel('city')
plt.ylabel('sales')
plt.show()


# # TASK 3 - WHAT TIME SHOULD WE DISPLAY ADVERTISEMENTS TO MAXIMIZE LIKELIHOOD OF CUSTOMER'S BUYING PRODUCT

# In[66]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])

all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
all_data['Count'] = 1
all_data.head()


# In[67]:


hours = [hour for hour,df in all_data.groupby('Hour')]

plt.plot(hours,all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.grid()
plt.show()


# #TASK 4 - WHICH PRODUCTS ARE MOST OFTEN SOLD TOGETHER?

# In[70]:


df = all_data[all_data['Order ID'].duplicated(keep=False)]

df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))

df = df[['Order ID','Grouped']].drop_duplicates()
df.head()


# In[72]:


from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,2)))
print(count.most_common(10))    


# # TASK 5 - WHICH PRODUCT SOLD MOST AND WHY?

# In[84]:


product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']
#quantity_ordered

products = [product for product,df in product_group]

plt.bar(products,quantity_ordered)
plt.xticks(products, rotation='vertical')
plt.xlabel('Quantity Order')
plt.ylabel('Products')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




