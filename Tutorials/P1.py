import requests

def get_exercises():
    # API endpoint
    url = "https://exercisedb.p.rapidapi.com/exercises"

    # Headers from RapidAPI
    headers = {
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com",
        "X-RapidAPI-Key": "3e33a52aebmshd529755bd74bb43p10b5f2jsn050e6ade2e72"  # Your provided key
    }

    # Query parameters (optional)
    params = {
        "limit": 10,
        "offset": 0
    }

    try:
        # API request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        exercises = response.json()

        # Display the fetched exercises
        print("\n--- Top Exercises ---")
        for i, exercise in enumerate(exercises, start=1):
            print(f"{i}. {exercise['name']}")
            print(f"   Body Part: {exercise['bodyPart']}")
            print(f"   Equipment: {exercise['equipment']}")
            print(f"   Target: {exercise['target']}\n")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_exercises()
