import pandas as pd
import numpy as np


# Load the cleaned CSV created in Task 2
input_file = "data/trends_clean.csv"
df = pd.read_csv(input_file)

print(f"Loaded data: {df.shape}")


# Show the first 5 stories
print("\nFirst 5 rows:")
print(df.head())


# Calculate average score and average comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print(f"\nAverage score   : {average_score:,.2f}")
print(f"Average comments: {average_comments:,.2f}")


# Get score values as a NumPy array
scores = df["score"].to_numpy()

# NumPy statistics
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:,.2f}")
print(f"Median score : {median_score:,.2f}")
print(f"Std deviation: {std_score:,.2f}")
print(f"Max score    : {max_score:,}")
print(f"Min score    : {min_score:,}")


# Find the category containing the most stories
category_counts = df["category"].value_counts()

most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()

print(
    f"\nMost stories in: "
    f"{most_common_category} ({most_common_count} stories)"
)


# Find the story with the highest number of comments
most_commented_index = df["num_comments"].idxmax()

most_commented_title = df.loc[most_commented_index, "title"]
most_commented_count = df.loc[most_commented_index, "num_comments"]

print(
    f'\nMost commented story: '
    f'"{most_commented_title}" — {most_commented_count:,} comments'
)


# Create engagement column
df["engagement"] = df["num_comments"] / (df["score"] + 1)


# Create is_popular column
# A story is popular when its score is greater than the average score
df["is_popular"] = df["score"] > average_score


# Save the analysed data
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")
