import pandas as pd
import matplotlib.pyplot as plt
import os


# Load the analysed trends data from Task 3
df = pd.read_csv("data/trends_analysed.csv")

# Create the outputs folder if it does not already exist
os.makedirs("outputs", exist_ok=True)


# ---------------------------------------------------------
# Chart 1: Top 10 Stories by Score
# ---------------------------------------------------------

# Select the 10 stories with the highest scores
top_stories = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..." if len(str(title)) > 50 else title
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_stories["short_title"],
    top_stories["score"]
)

plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

# Put the highest-scoring story at the top
plt.gca().invert_yaxis()

plt.tight_layout()

# Save before showing
plt.savefig("outputs/chart1_top_stories.png")

plt.show()
plt.close()


# ---------------------------------------------------------
# Chart 2: Stories per Category
# ---------------------------------------------------------

# Count how many stories belong to each category
category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 6))

# Give each category bar a different colour
plt.bar(
    category_counts.index,
    category_counts.values,
    color=plt.cm.tab10(range(len(category_counts)))
)

plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.xticks(rotation=45)

plt.tight_layout()

# Save before showing
plt.savefig("outputs/chart2_categories.png")

plt.show()
plt.close()


# ---------------------------------------------------------
# Chart 3: Score vs Comments
# ---------------------------------------------------------

plt.figure(figsize=(9, 6))

# Separate popular and non-popular stories
popular = df[df["is_popular"] == True]
non_popular = df[df["is_popular"] == False]

# Plot popular stories
plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

# Plot non-popular stories
plt.scatter(
    non_popular["score"],
    non_popular["num_comments"],
    label="Non-Popular"
)

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.tight_layout()

# Save before showing
plt.savefig("outputs/chart3_scatter.png")

plt.show()
plt.close()


# ---------------------------------------------------------
# Bonus: Combined Dashboard
# ---------------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(16, 11))

fig.suptitle("TrendPulse Dashboard", fontsize=18)


# Dashboard Chart 1
axes[0, 0].barh(
    top_stories["short_title"],
    top_stories["score"]
)

axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")
axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].invert_yaxis()


# Dashboard Chart 2
axes[0, 1].bar(
    category_counts.index,
    category_counts.values,
    color=plt.cm.tab10(range(len(category_counts)))
)

axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")
axes[0, 1].set_title("Stories per Category")
axes[0, 1].tick_params(axis="x", rotation=45)


# Dashboard Chart 3
axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

axes[1, 0].scatter(
    non_popular["score"],
    non_popular["num_comments"],
    label="Non-Popular"
)

axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")
axes[1, 0].set_title("Score vs Comments")
axes[1, 0].legend()


# Hide the unused fourth subplot
axes[1, 1].axis("off")

plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save dashboard
plt.savefig("outputs/dashboard.png")

plt.show()
plt.close()


print("All charts created successfully!")
