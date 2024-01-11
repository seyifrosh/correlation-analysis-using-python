#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing the necessary libaries
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


# In[6]:


#Preparation of data; importing the first dataset
df1 = pd.read_csv("data/brasil-real-estate-1.csv")
df1.head()


# In[ ]:


#inspection of dataset 1

df1.info()
df1.shape 
df1.head() 


# In[ ]:


#Drop all rows with NaN values from the DataFrame df1.

df1.dropna(inplace = True)


# In[ ]:


#"lat-lon" column was used to create two separate columns in df1: "lat" and "lon". 
df1[["lat","lon"]] = df1["lat-lon"].str.split(",",expand = True).astype(float)


# In[ ]:


# data extraction:"place_with_parent_names" column was used  to create a "state" column for df1.
df1["state"] = df1["place_with_parent_names"].str.split("|",expand = True)[2]


# In[ ]:


#conversion of price_usd column from object to float.

df1["price_usd"] = df1["price_usd"].str.replace("$","",regex = False).str.replace(",","",regex = False).astype(float)
df1.info()


# In[ ]:


#Dropping unwanted columns.Drop the "lat-lon" and "place_with_parent_names" columns from df1.

df1.drop(columns = ["lat-lon","place_with_parent_names"], inplace = True)
df1.info() #cross-check to see if variables have been dropped successfully


# In[ ]:


#preparation of dataset2 : importing dataset2

df2 = pd.read_csv("data/brasil-real-estate-2.csv")


# In[ ]:


#inspection of dataset 2
df2.info()


# In[ ]:


#To merge the two dataset, they must have same features.
#Use the "price_brl" column to create a new column named "price_usd". 
#(Keep in mind that, when this data was collected,a US dollar cost 3.19 Brazilian reals.)

df2["price_usd"] = (df2["price_brl"]/3.19).round(2)


# In[ ]:


#Drop the "price_brl" column from df2, as well as any rows that have NaN values.

df2.dropna(inplace = True)
df2.drop(columns = ["price_brl"], inplace = True)
df2.info()


# In[ ]:


#Concatenate df1 and df2 to create a new DataFrame named df.

df = pd.concat([df1,df2])
print("df shape:", df.shape)


# In[ ]:


Exploration of the combined dataframe


# In[ ]:


#create a scatter_mapbox showing the location of the properties in df.

fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    center={"lat": -14.2, "lon": -51.9},  # Map will be centered on Brazil
    width=600,
    height=600,
    hover_data=["price_usd"],  # Display price when hovering mouse over house
)

fig.update_layout(mapbox_style="open-street-map")

fig.show()


# In[ ]:


#DataFrame summary_stats with the summary statistics for the "area_m2" and "price_usd" columns.

summary_stats =df[["area_m2","price_usd"]].describe()
summary_stats


# In[ ]:


#Distribution of prices of houses in Brasil. 
# Build histogram
plt.hist(df["price_usd"]
);

# Label axes
plt.xlabel("Price [USD]")
plt.ylabel("Frequency")
# Add title
plt.title("Distribution of Home Prices")


# In[ ]:


Exploration of combined DataFrame


# In[ ]:


#Distribution of house sizes in Brasil
#Build box plot(Box plot is also a check of normality distribution like histogram)
plt.boxplot(df["area_m2"], vert = False);


# Label x-axis
plt.xlabel("Area [sq meters]")

# Add title
plt.title("Distribution of Home Sizes")


# In[ ]:


# mean home price in each region in Brazil, sorted from smallest to largest.

mean_price_by_region = df.groupby("region")["price_usd"].mean().sort_values()
mean_price_by_region


# In[ ]:


#bar chart of mean_house_price by region in brasil using pandas
# Build bar chart, label axes, add title
mean_price_by_region.plot(
    kind = "bar",
    xlabel = "Region",
    ylabel = "Mean  Price [USD]",
    title = "Mean Home Price by Region"
);


# In[ ]:


#Create a DataFrame df_south that contains all the homes from df that are in the "South" region.
#(south is the Region with the highest house_price in brasil)

df_south = df[df["region"] == "South"]
df_south.head()


# In[ ]:


#value_counts method to create a Series homes_by_state that contains the number of properties in each state in df_south.

homes_by_state = df_south["state"].value_counts()
homes_by_state


# In[ ]:


#CORRELATION ANALYSIS:study the relationship between size and price for states in the southern region of brasil


# In[ ]:


df_south_rgs = df_south[df_south["state"] == "Rio Grande do Sul"]

# Build scatter plot
plt.scatter(x =df_south_rgs["area_m2"],y = df_south_rgs["price_usd"] )


# Label axes
plt.xlabel("Area [sq meters]")
plt.ylabel("Price [USD]")

# Add title
plt.title("Rio Grande do Sul: Price vs. Area")


# In[ ]:


#correlation coefficient of area vs price for respective states in the southern region of brasil

#subset df_south to filter for each state
df_south_rgs = df_south[df_south["state"] == "Rio Grande do Sul"]
df_south_sc =df_south[df_south["state"] == "Santa Catarina"]
df_south_pa =df_south[df_south["state"] == "Paraná"]

south_states_corr = {"Rio Grande do Sul": df_south_rgs["area_m2"].corr(df_south_rgs["price_usd"]),
                     "Santa Catarina": df_south_sc["area_m2"].corr(df_south_sc["price_usd"]),
                     "Paraná"        :  df_south_pa["area_m2"].corr(df_south_pa["price_usd"])}

south_states_corr

