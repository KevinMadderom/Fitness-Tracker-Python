"""
Kevin Madderom

Fitness Tracker for inputing and analyzing workout data
"""
import datetime
from datetime import datetime
import json
import os


def create_profile():
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    weight = input("Enter your current bodyweight (lbs): ")
    height = input("Enter your height (ex: 5'10): ")

    profile = {
        'name': name,
        'age': age,
        'weight': weight,
        'height': height
    }

    try:
        with open('profile.json', 'r') as file:
            profiles = json.load(file)
            if not isinstance(profiles, list):
                profiles = []
    except (FileNotFoundError, json.JSONDecodeError):
        profiles = []

    profiles.append(profile)

    with open('profile.json', 'w') as file:
        json.dump(profiles, file, indent=4)

    print(f"Profile for {name} created and saved!")

def select_profile():
    try:
        with open('profile.json', 'r') as file:
            profiles = json.load(file)

        if not isinstance(profiles, list):
            print("Profile data is corrupted. Please create a new profile.")
            return None
    
    except (FileNotFoundError, json.JSONDecodeError):
            print("No profiles found. Please create a profile first.")
            return None
    
    if not profiles:
        print("No profiles found. Please create a profile first.")
        return None
    
    print("Available Profiles:")
    for i, profile in enumerate(profiles, start=1):
        print(f"{i}. {profile['name']}, Age: {profile['age']}, Weight: {profile['weight']} lbs, Height: {profile['height']}")

    while True:
        try:
            choice = int(input("Select a profile by number: "))
            if 1 <= choice <= len(profiles):
                return profiles[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def load_profile():
    try:
        with open('profile.json', 'r') as file:
            profile = json.load(file)
            print(f"Profile loaded: {profile}")
            return profile
    except FileNotFoundError:
        print("No profile found. Please create a profile first.")
        return None
    
''' Load existing workouts from a JSON file or initialize an empty list '''
def date_validator(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False
    
def type_validator(type_text):
    valid_types = ['Weight Training', 'Running', 'Walking', 'HIIT Training', 'Other']
    if type_text in valid_types:
        return True
    else:
        print(f"Invalid workout type. Valid types are: {', '.join(valid_types)}, type 5 to add a new workout type to the list. Type 6 to exit")
        return False
    
def duration_validator(duration_text):
    try:
        duration = float(duration_text)
        if duration <= 0:
            raise ValueError
        return True
    except ValueError:
        print("Invalid duration. Please enter a positive number.")
        return False
    
def calorie_calculator(workoutType, duration):

    calorie_multipliers = {
        'Weight Training': 6.0,
        'Running': 10.0,
        'Walking': 4.0,
        'HIIT Training': 12.0,
        'Other': 8.0
    }
    
    multiplier = calorie_multipliers.get(workoutType, 8.0)

    estimated_calories = multiplier * duration
    return estimated_calories
    
def recommended_calorie_intake(weight, age, height, activity_level):
    if activity_level == 'sedentary':
        multiplier = 1.0
    elif activity_level == 'lightly active':
        multiplier = 1.15
    elif activity_level == 'moderately active':
        multiplier = 1.25
    elif activity_level == 'very active':
        multiplier = 1.35
    elif activity_level == 'extra active':
        multiplier = 1.5
    else:
        raise ValueError("Invalid activity level")

    bmr = 10 * weight + 6.25 * height - 5 * age + 5

    return bmr * multiplier

def main():

    print("Welcome to my Fitness Tracker!")

    current_profile = None
    while not current_profile:
        print("\nProfile Selection:")
        print("1. Create Profile")
        print("2. Select Profile")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            create_profile()
        elif choice == '2':
            current_profile = select_profile()
        elif choice == '3':
            print("Exiting the program.")
            return
        else:
            print("Invalid choice. Please try again.")
   
    workout_file = f"workouts_{current_profile['name']}.json"

    try:
        with open(workout_file, 'r') as file:
            workouts = json.load(file)
    except FileNotFoundError:
        workouts = []

    menu = {
        '1': 'Add Workout:',
        '2': 'View Workouts:',
        '3': 'Average Duration:',
        '4': 'Recommended Calorie Intake:',
        '5': 'Exit'
    }

    ''' Main loop for user interaction '''
    while True:
        print(f"\nHello, {current_profile['name']}! What would you like to do?")
        print("-" * 40)
        print("\nMenu:")
        for key, value in menu.items():
            print(f"{key}. {value}")
        print("-" * 40)
            

        choice = input("Choose an option: ")
        
        if choice == '1':

            workoutType = {
                1 : 'Weight Training',
                2 : 'Running',
                3 : 'Walking',
                4 : 'HIIT Training',
                5 : 'Other',
                6 : 'Exit'
            }

            while True:
                print("Workout Types:")
                for key, value in workoutType.items():
                    print(f"{key}. {value}")

                try:
                    type_choice = int(input("Choose a workout type (1-6): "))
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 6.")
                    continue

                if type_choice not in workoutType:
                    print("Invalid choice. Please choose a number between 1 and 6.")
                    continue

                if type_choice == 6:
                    print("Exiting workout type selection.")
                    break

                if type_choice == 5:
                    new_exercise_type = input("Enter the name of the new workout type: ").strip()
                    if new_exercise_type:
                        workoutType[len(workoutType) + 1] = new_exercise_type
                        print(f"Added new workout type: {new_exercise_type}")
                        exercise_type = new_exercise_type
                        break
                    else:
                        print("Workout type cannot be empty.")
                        continue

                exercise_type = workoutType[type_choice]
                break

            if type_choice == 6:
                continue


            date = input("Enter date (YYYY-MM-DD): ").strip()
            while not date_validator(date):
                print("Invalid date format. Please enter in YYYY-MM-DD format.")
                date = input("Enter date (YYYY-MM-DD): ").strip()

            duration = float(input("Enter duration in minutes: "))
            while not duration_validator(duration):
                duration = float(input("Enter duration in minutes: "))

            calories = calorie_calculator(exercise_type, duration)

            ''' Add the new workout to the list that can be saved to a JSON file '''       
            newWorkout = {
                    'Workout' : len(workouts) + 1,
                    'date': date,
                    'type': exercise_type,
                    'duration': duration,
                    'calories': calories,
                    }
            workouts.append(newWorkout)


            for workout in workouts:
                print(f"Date: {workout['date']}, Type: {workout['type']}, Duration: {workout['duration']}, Estimated Calories Burned: {workout['calories']:.2f}")
                
            ''' Save the updated workouts list to the JSON file indented for readability '''
            with open(workout_file, 'w') as file:
                json.dump(workouts, file, indent=4)
            print(f"Workout added and saved for {current_profile['name']}!")
                

        elif choice == '2':
            if not workouts:
                print("No workouts recorded.")
            else:
                for workout in workouts:
                    print(f"Date: {workout['date']}, Type: {workout['type']}, Duration: {workout['duration']}, Estimated Calories Burned: {workout['calories']:.2f}")
        elif choice == '3':
            if not workouts:
                print("No workouts recorded, please add a workout.")
            else:
                avg_duration = sum(w['duration'] for w in workouts) / len(workouts)
                print(f"Average Duration: {avg_duration:.2f} minutes")
        elif choice == '4':
            personalWeight = float(current_profile['weight'])
            personalAge = int(current_profile['age'])
            personalHeight = int(current_profile['height'].split("'")[0]) * 12 + int(current_profile['height'].split("'")[1])
            activity_level = input("Enter your activity level (sedentary, lightly active, moderately active, very active, extra active): ").strip().lower()
            try:
                recommended_calories = recommended_calorie_intake(personalWeight, personalAge, personalHeight, activity_level)
                print(f"Recommended Daily Calorie Intake: {recommended_calories:.2f} calories")
            except ValueError:
                print("Invalid activity level. Please try again.")
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()