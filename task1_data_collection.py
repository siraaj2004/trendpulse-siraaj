import requests
import time
import json
import os
from datetime import datetime


# HackerNews API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required User-Agent header
HEADERS = {
    "User-Agent": "TrendPulse/1.0"
}


# Keywords for each category
KEYWORDS = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}


def get_category(title):
    """
    Check the story title against the keywords.
    Matching is case-insensitive.
    """

    title_lower = title.lower()

    for category, keywords in KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in title_lower:
                return category

    return None


def fetch_top_story_ids():
    """Fetch the list of top HackerNews story IDs."""

    try:
        response = requests.get(
            TOP_STORIES_URL,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        return response.json()[:500]

    except requests.RequestException as error:
        print("Failed to fetch top stories:", error)
        return []


def fetch_story(story_id):
    """Fetch details of one HackerNews story."""

    try:
        url = ITEM_URL.format(story_id)

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print(f"Failed to fetch story {story_id}: {error}")
        return None


def main():

    # Get the first 500 top story IDs
    story_ids = fetch_top_story_ids()

    if not story_ids:
        print("No story IDs were collected.")
        return

    # Store stories separately by category
    category_stories = {
        "technology": [],
        "worldnews": [],
        "sports": [],
        "science": [],
        "entertainment": []
    }

    # Fetch story details
    for story_id in story_ids:

        # Stop when all categories have 25 stories
        if all(len(stories) >= 25 for stories in category_stories.values()):
            break

        story = fetch_story(story_id)

        if story is None:
            continue

        # Only process stories that have a title
        title = story.get("title", "")

        if not title:
            continue

        category = get_category(title)

        # Ignore stories that don't match any category
        if category is None:
            continue

        # Don't collect more than 25 per category
        if len(category_stories[category]) >= 25:
            continue

        collected_time = datetime.now().isoformat()

        # Create the required output structure
        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": collected_time
        }

        category_stories[category].append(story_data)

    # Combine all categories into one list
    all_stories = []

    for category in category_stories:

        all_stories.extend(category_stories[category])

        # One 2-second sleep per category loop
        time.sleep(2)

    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Create filename using today's date
    date_string = datetime.now().strftime("%Y%m%d")

    output_file = f"data/trends_{date_string}.json"

    # Save the collected stories
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(all_stories, file, indent=4, ensure_ascii=False)

    # Print category counts
    print("\nStories collected by category:")

    for category, stories in category_stories.items():
        print(f"{category}: {len(stories)}")

    print(f"\nCollected {len(all_stories)} stories.")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()
