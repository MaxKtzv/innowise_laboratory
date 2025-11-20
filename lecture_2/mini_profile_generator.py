"""
Mini-Profile Generator - A simple and lightweight user profile creation script.

Collect user information via prompts (name, year of birth and favorite
hobbies), generate a profile (name, age, life stage and hobbies)
and print it.
"""

print("Welcome to the Mini-Profile Generator!")

user_name = input("Enter your full name: ")
birth_year_str = input("Enter your birth year: ")

birth_year: int = int(birth_year_str)
current_age: int = 2025 - birth_year


def generate_profile(age: int) -> str:
    """
    Check the age and return the life stage.

    Args:
        age (int): The age of the user.

    Returns:
        str: The life stage of the user.
    """
    if age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    elif age >= 20:
        return "Adult"


hobbies = []

while True:
    hobby = input("Enter a favorite hobby or type 'stop' to finish: ")
    if hobby.lower() == "stop":
        break
    else:
        hobbies.append(hobby)

life_stage: str = generate_profile(current_age)

user_profile = {
    "name": user_name,
    "age": current_age,
    "stage": life_stage,
    "hobbies": hobbies,
}

print(f"\n---\nProfile Summary:")
print(f"Name: {user_name}")
print(f"Age: {current_age}")
print(f"Life Stage: {life_stage}")

if not hobbies:
    print("You didn't mention any hobbies.")
else:
    print(f"Favorite Hobbies ({len(hobbies)}):")
    for hobby in hobbies:
        print(f"- {hobby}")
print("---")
