import requests

def get_vimeo_videos(query, max_results=5):
    # Vimeo API endpoint
    url = "https://api.vimeo.com/videos"

    # Headers with your access token
    headers = {
        "Authorization": "Bearer 7f2305506e92a77af0128d0e24d9375f"  # Replace with your Vimeo token
    }

    # Query parameters
    params = {
        "query": "Gym workouts",  # Search query (e.g., "home workout")
        "per_page": max_results  # Number of results
    }

    try:
        # API request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Check for HTTP request errors
        videos = response.json()

        print(f"\n--- Top {max_results} Videos for '{query}' on Vimeo ---")
        for i, video in enumerate(videos['data'], start=1):
            print(f"{i}. {video['name']}")
            print(f"   URL: {video['link']}")
            print(f"   Description: {video['description'] or 'No description available'}")
            print(f"   Duration: {video['duration']} seconds")
            print(f"   Upload Date: {video['created_time']}\n")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example: Search for videos related to "yoga for beginners"
    get_vimeo_videos("yoga for beginners")
