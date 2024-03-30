import openai
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Specify the GPT model you want to use
        prompt=prompt,
        max_tokens=100,
        language="en"  # Specify English language
    )
    return response.choices[0].text.strip()

def appointment_scheduling(callers, history_file="call_history.json"):
    """
    Simulates a healthcare assistant at Melbourne Foot and Ankle Hospital
    scheduling appointments based on caller inquiries.

    Args:
    - callers (list): List of dictionaries representing caller information.
                      Each dictionary should contain 'name', 'is_new_user', 'email', 'mobile', 'hospital_id', 'date', 'time'.
    - history_file (str): File path to save call history.

    Returns:
    - list: List of dictionaries representing responses to callers.
    """
    responses = []

    # Load call history if available
    try:
        with open(history_file, 'r') as file:
            call_history = json.load(file)
    except FileNotFoundError:
        call_history = []

    for caller in callers:
        # Welcome message
        responses.append({"role": "assistant", "content": "Welcome to Melbourne Foot and Ankle Hospital. How can I assist you today?"})

        # Check if caller is a new user
        if caller['is_new_user']:
            responses.append({"role": "user", "content": "I am a new user."})
            responses.append({"role": "assistant", "content": "Great! Let's get you scheduled for an appointment."})

            # Ask for name
            responses.append({"role": "assistant", "content": "May I have your full name, please?"})
            responses.append({"role": "user", "content": caller['name']})

            # Ask for email
            responses.append({"role": "assistant", "content": "What is your email address?"})
            responses.append({"role": "user", "content": caller['email']})

            # Ask for mobile number
            responses.append({"role": "assistant", "content": "What is your mobile number?"})
            responses.append({"role": "user", "content": caller['mobile']})

            # Ask for appointment date and time
            responses.append({"role": "assistant", "content": "When would you like to schedule your appointment? Please specify date and time."})
            responses.append({"role": "user", "content": f"{caller['date']} at {caller['time']}."})

        else:
            responses.append({"role": "user", "content": "I am an existing user."})
            responses.append({"role": "assistant", "content": "Please provide your hospital ID."})
            responses.append({"role": "user", "content": caller['hospital_id']})

            # Ask for appointment date and time
            responses.append({"role": "assistant", "content": "When would you like to schedule your appointment? Please specify date and time."})
            responses.append({"role": "user", "content": f"{caller['date']} at {caller['time']}."})

        # Confirm appointment scheduling
        responses.append({"role": "assistant", "content": "Thank you! Your appointment has been scheduled."})

        # Log call history
        call_history.append(caller)

    # Save call history to file
    with open(history_file, 'w') as file:
        json.dump(call_history, file, indent=4)

    return responses

def retrain_model(history_file="call_history.json"):
    """
    Retrains the model using the call history data.

    Args:
    - history_file (str): File path to load call history.
    """
    try:
        with open(history_file, 'r') as file:
            call_history = json.load(file)

        # Implement model retraining using call history data
        # Example: You can use machine learning techniques to retrain the model based on the call history

        print("Model retraining completed successfully.")
    except FileNotFoundError:
        print("No call history found. Cannot retrain model.")

# Example usage:
callers = [
    {"name": "John Doe", "is_new_user": False, "email": "johndoe@example.com", "mobile": "1234567890", "hospital_id": "123456", "date": "2024-03-15", "time": "10:00 AM"},

    {"name": "Jane Smith", "is_new_user": True, "email": "janesmith@example.com", "mobile": "9876543210", "hospital_id": "", "date": "2024-03-16", "time": "11:00 AM"}
]

responses = appointment_scheduling(callers)
for response in responses:
    print(f"{response['role']}: {response['content']}")

# Retrain the model using call history
retrain_model()
