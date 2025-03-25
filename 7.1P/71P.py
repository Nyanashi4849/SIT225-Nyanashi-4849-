import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Prevents Tkinter issue (no GUI)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import os

# ==============================
# 1. Load DHT22 Sensor Data from CSV Safely
# ==============================
file_name = "mann.csv"

# Ensure file exists and is readable
if not os.path.exists(file_name):
    print(f"❌ ERROR: '{file_name}' not found! Check the file path.")
    exit()

if not os.access(file_name, os.R_OK):
    print(f"❌ ERROR: No read permission for '{file_name}'. Try running as Administrator.")
    exit()

# Read CSV file
data = pd.read_csv(file_name)

# Drop Timestamp column if it exists
if "Timestamp" in data.columns:
    data = data.drop(columns=["Timestamp"])

# Show first 5 rows
print("✅ First 5 Rows of Data:")
print(data.head())

# ==============================
# 2. Scatter Plot of Raw Data
# ==============================
plt.figure(figsize=(8, 5))
sns.scatterplot(x=data["Temperature"], y=data["Humidity"], color="blue", label="Original Data")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.title("Temperature vs. Humidity (Raw Data)")
plt.legend()
plt.savefig("scatter_raw.png")  # Save graph
plt.close()

# ==============================
# 3. Train Initial Linear Regression Model
# ==============================
X = data["Temperature"].values.reshape(-1, 1)  # Reshape for sklearn
y = data["Humidity"].values

model = LinearRegression()
model.fit(X, y)

# Generate predictions for a range of temperatures
temp_range = np.linspace(data["Temperature"].min(), data["Temperature"].max(), 100).reshape(-1, 1)
humidity_pred = model.predict(temp_range)

# Plot regression trend
plt.figure(figsize=(8, 5))
sns.scatterplot(x=data["Temperature"], y=data["Humidity"], color="blue", label="Original Data")
plt.plot(temp_range, humidity_pred, color="red", label="Regression Line")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.title("Temperature vs. Humidity (With Regression)")
plt.legend()
plt.savefig("regression_raw.png")  # Save graph
plt.close()

print(f"✅ Initial Model Coefficients: Slope={model.coef_[0]:.3f}, Intercept={model.intercept_:.3f}")

# ==============================
# 4. Identify & Highlight Outliers
# ==============================
data["z_score"] = (data["Humidity"] - data["Humidity"].mean()) / data["Humidity"].std()
outliers = data[(data["z_score"].abs() >= 2)]  # Outliers (Z-score outside ±2)
filtered_data = data[(data["z_score"].abs() < 2)]  # Keep only valid data

print(f"✅ Removed {len(outliers)} Outliers")

# Plot data with outliers highlighted
plt.figure(figsize=(8, 5))
sns.scatterplot(x=data["Temperature"], y=data["Humidity"], color="blue", label="Original Data")
sns.scatterplot(x=outliers["Temperature"], y=outliers["Humidity"], color="red", label="Outliers", marker="x", s=100)
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.title("Temperature vs. Humidity (Outliers Highlighted)")
plt.legend()
plt.savefig("outliers_highlighted.png")  # Save graph
plt.close()

# ==============================
# 5. Retrain Model After Removing Outliers
# ==============================
X_filtered = filtered_data["Temperature"].values.reshape(-1, 1)
y_filtered = filtered_data["Humidity"].values

model_filtered = LinearRegression()
model_filtered.fit(X_filtered, y_filtered)
humidity_pred_filtered = model_filtered.predict(temp_range)

# Plot new regression trend after outlier removal
plt.figure(figsize=(8, 5))
sns.scatterplot(x=filtered_data["Temperature"], y=filtered_data["Humidity"], color="blue", label="Filtered Data")
plt.plot(temp_range, humidity_pred_filtered, color="green", label="Filtered Regression Line")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.title("Temperature vs. Humidity (After Removing Outliers)")
plt.legend()
plt.savefig("regression_filtered.png")  # Save graph
plt.close()

print(f"✅ Filtered Model Coefficients: Slope={model_filtered.coef_[0]:.3f}, Intercept={model_filtered.intercept_:.3f}")

# ==============================
# 6. Save Cleaned Data to CSV
# ==============================
filtered_data = filtered_data.drop(columns=["z_score"])  # Remove z-score column
filtered_data.to_csv("71P_filtered.csv", index=False)
print("✅ Cleaned Data Saved to '71P_filtered.csv'")
