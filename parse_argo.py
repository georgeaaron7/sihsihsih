import pandas as pd

# Path to the Argo index file (make sure it is in this folder)
file_path = "argo_synthetic-profile_index.txt"

# Column names from the Argo format
columns = [
    "file_path", "date", "latitude", "longitude", 
    "data_mode", "profile_number", "platform", 
    "parameters", "qc_flags", "last_update"
]

# Read the file
df = pd.read_csv(file_path, names=columns, delimiter=",", comment="#")

# Extract float_id from file_path (e.g. /1900722/ → 1900722)
df["float_id"] = df["file_path"].str.extract(r"/(\d{7})/")

# Convert dates into proper datetime
df["date"] = pd.to_datetime(df["date"], format="%Y%m%d%H%M%S", errors="coerce")
df["last_update"] = pd.to_datetime(df["last_update"], format="%Y%m%d%H%M%S", errors="coerce")

# Keep only the latest record for each float_id
df_latest = df.sort_values("date").groupby("float_id").tail(1).reset_index(drop=True)
df
# Save to CSV
df_latest.to_csv("parsed_floats.csv", index=False)

print("✅ Parsing complete! Saved as parsed_floats.csv")
print(df_latest.head())
