import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Loading data
Rapid_df = pd.read_csv(r"CSV files\Rapid_Games.csv")

# Create features
Rapid_df["EloDifference"] = Rapid_df["WhiteElo"] - Rapid_df["BlackElo"]
Rapid_df["OmarsayehElo"] = 0  # Placeholder for your Elo

# Set your Elo based on whether you played as White or Black
Rapid_df.loc[Rapid_df["White"] == "omarsayeh", "OmarsayehElo"] = Rapid_df["WhiteElo"]
Rapid_df.loc[Rapid_df["Black"] == "omarsayeh", "OmarsayehElo"] = Rapid_df["BlackElo"]

# Convert Date to datetime and sort
Rapid_df["Date"] = pd.to_datetime(Rapid_df["Date"])
Rapid_df.sort_values("Date", inplace=True)

Rapid_df["DaysSinceLastGame"] = Rapid_df["Date"].diff().dt.days.fillna(0)

# Assuming 'OmarsayehElo' is your target variable
X = Rapid_df[["EloDifference", "DaysSinceLastGame"]]
y = Rapid_df["OmarsayehElo"]

# Train a linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict future Elo for omarsayeh
future_dates = pd.date_range(start="2023-01-01", end="2026-01-01", freq="D")
future_data = pd.DataFrame({"Date": future_dates})
future_data["EloDifference"] = 1080 - 1022  # Adjust with your specific values
future_data["DaysSinceLastGame"] = (
    future_data["Date"] - Rapid_df["Date"].max()
).dt.days
future_data["PredictedOmarsayehElo"] = model.predict(
    future_data[["EloDifference", "DaysSinceLastGame"]]
)

# Plot results
plt.plot(Rapid_df["Date"], Rapid_df["OmarsayehElo"], label="Actual Omarsayeh Elo")
plt.plot(
    future_data["Date"],
    future_data["PredictedOmarsayehElo"],
    label="Predicted Omarsayeh Elo",
    linestyle="--",
    color="red",
)
plt.xlabel("Date")
plt.ylabel("Omarsayeh Elo Rating")
plt.title("Actual and Predicted Omarsayeh Elo Over Time")
plt.legend()
plt.show()
