import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import os


file_name = "mann.csv"


if not os.path.exists(file_name):
    print(f" ERROR: '{file_name}' not found! Check the file path.")
    exit()

if not os.access(file_name, os.R_OK):
    print(f" ERROR: No read permission for '{file_name}'. Try running as Administrator.")
    exit()

data = pd.read_csv(file_name)

if "Timestamp" in data.columns:
    data = data.drop(columns=["Timestamp"])

print(" First 5 Rows of Data:")
print(data.head())


plt.figure(figsize=(8, 5))
sns.scatterplot(x=data["Temperature"], y=data["Humidity"], color="blue", label="Original Data")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.title("Temperature vs. Humidity (Raw Data)")
plt.legend()
plt.savefig("scatter_raw.png") 
plt.close()


X = data["Temperature"].values.reshape(-1, 1) 
y = data["Humidity"].values

model = LinearRegression()
model.fit(X, y)

temp_range = np.linspace(data["Temperature"].min(), data["Temperature"].max(), 100).reshape(-1, 1)
humidity_pred = model.predict(temp_range)

plt.figure(figsize=(8, 5))
sns.scatterplot(x=data["Temperature"], y=data["Humidity"], color="blue", label="Original Data")
plt.plot(temp_range, humidity_pred, color="red", label="Regression Line")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.title("Temperature vs. Humidity (With Regression)")
plt.legend()
plt.savefig("regression_raw.png") 
plt.close()

print(f" Initial Model Coefficients: Slope={model.coef_[0]:.3f}, Intercept={model.intercept_:.3f}")


data["z_score"] = (data["Humidity"] - data["Humidity"].mean()) / data["Humidity"].std()
outliers = data[(data["z_score"].abs() >= 2)]  
filtered_data = data[(data["z_score"].abs() < 2)]  

print(f" Removed {len(outliers)} Outliers")

plt.figure(figsize=(8, 5))
sns.scatterplot(x=data["Temperature"], y=data["Humidity"], color="blue", label="Original Data")
sns.scatterplot(x=outliers["Temperature"], y=outliers["Humidity"], color="red", label="Outliers", marker="x", s=100)
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.title("Temperature vs. Humidity (Outliers Highlighted)")
plt.legend()
plt.savefig("outliers_highlighted.png") 
plt.close()

X_filtered = filtered_data["Temperature"].values.reshape(-1, 1)
y_filtered = filtered_data["Humidity"].values

model_filtered = LinearRegression()
model_filtered.fit(X_filtered, y_filtered)
humidity_pred_filtered = model_filtered.predict(temp_range)

plt.figure(figsize=(8, 5))
sns.scatterplot(x=filtered_data["Temperature"], y=filtered_data["Humidity"], color="blue", label="Filtered Data")
plt.plot(temp_range, humidity_pred_filtered, color="green", label="Filtered Regression Line")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.title("Temperature vs. Humidity (After Removing Outliers)")
plt.legend()
plt.savefig("regression_filtered.png") 
plt.close()

print(f" Filtered Model Coefficients: Slope={model_filtered.coef_[0]:.3f}, Intercept={model_filtered.intercept_:.3f}")

filtered_data = filtered_data.drop(columns=["z_score"])  
filtered_data.to_csv("71P_filtered.csv", index=False)
print(" Cleaned Data Saved to '71P_filtered.csv'")

