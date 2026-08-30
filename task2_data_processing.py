import pandas as pd
from pathlib import Path


# Find the JSON file inside the data folder
data_folder = Path("data")
json_files = sorted(data_folder.glob("trends_*.json"))

if not json_files:
    print("No trends JSON file found in the data folder.")
    exit()

input_file = json_files[-1]

# Load JSON data into a DataFrame
df = pd.read_json(input_file)

print(f"Loaded {len(df)} stories from {input_file}")


# 1. Remove duplicate stories based on post_id
df = df.drop_duplicates(subset="post_id")

print(f"After removing duplicates: {len(df)}")


# 2. Remove rows missing important values
df = df.dropna(subset=["post_id", "title", "score"])

print(f"After removing nulls: {len(df)}")


# 3. Convert score and num_comments to integers
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

# Remove rows that became invalid after type conversion
df = df.dropna(subset=["score", "num_comments"])

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# 4. Remove stories with score less than 5
df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")


# 5. Remove extra whitespace from titles
df["title"] = df["title"].astype(str).str.strip()


# Save cleaned data
output_file = data_folder / "trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")


# Print number of stories in each category
print("\nStories per category:")

category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(f"  {category:<16} {count}")
