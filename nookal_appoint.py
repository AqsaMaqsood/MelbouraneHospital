import json
from urllib import parse
import requests
import openai as OPENAI

# Set your OpenAI API key
openai.api_key = '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'

# Define your Nookal API key
api_key = api_key

def generate_response(prompt):
    """
    Generate a response from OpenAI's GPT-3 model given a prompt.

    Args:
    - prompt (str): The prompt to generate a response from.

    Returns:
    - str: The generated response.
    """
    #client = OPENAI()
    response = client.chat.completions.with_raw_response.create (
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def add_appointment_booking(query_data):
    resp = requests.request("GET", 
                            f"https://api.nookal.com/production/v2/addAppointmentBooking?{query_data}")
    data = resp.content.decode('utf-8')  # Decode byte string to a regular string
    json_data = json.loads(data)  # Convert JSON string to a Python dictionary
    return json_data

def appointment_scheduling(callers):
    """
    Simulates a healthcare assistant scheduling appointments based on caller inquiries.

    Args:
    - callers (list): List of dictionaries representing caller information.
                      Each dictionary should contain 'name', 'is_new_user', 'email', 'mobile', 'hospital_id', 'date', 'time'.

    Returns:
    - list: List of dictionaries representing responses to callers.
    """
    responses = []

    for caller in callers:
        # Welcome message
        responses.append({"role": "assistant", "content": generate_response("Welcome to Melbourne Foot and Ankle Hospital. How can I assist you today?")})

        # Check if caller is a new user
        if caller['is_new_user']:
            responses.append({"role": "user", "content": "I'm a new user."})
            responses.append({"role": "assistant", "content": generate_response("Great! Let's get you scheduled for an appointment.")})

            # Ask for name
            responses.append({"role": "assistant", "content": generate_response("May I have your full name, please?")})
            responses.append({"role": "user", "content": caller['name']})

            # Ask for email
            responses.append({"role": "assistant", "content": generate_response("What is your email address?")})
            responses.append({"role": "user", "content": caller['email']})

            # Ask for mobile number
            responses.append({"role": "assistant", "content": generate_response("What is your mobile number?")})
            responses.append({"role": "user", "content": caller['mobile']})

            # Ask for appointment date and time
            responses.append({"role": "assistant", "content": generate_response("When would you like to schedule your appointment? Please provide the date and time.")})
            responses.append({"role": "user", "content": f"{caller['date']} at {caller['time']}."})

        else:
            responses.append({"role": "user", "content": "I'm an existing user."})
            responses.append({"role": "assistant", "content": generate_response("Please provide your hospital ID.")})
            responses.append({"role": "user", "content": caller['hospital_id']})

            # Ask for appointment date and time
            responses.append({"role": "assistant", "content": generate_response("When would you like to schedule your appointment? Please provide the date and time.")})
            responses.append({"role": "user", "content": f"{caller['date']} at {caller['time']}."})

        # Make the appointment booking
        query_params = {
            "api_key": api_key,
            "location_id": 1,
            "appointment_date": caller['date'],
            "start_time": caller['time'],
            "patient_id": caller['hospital_id'] if not caller['is_new_user'] else None,
            "practitioner_id": 1,
            "appointment_type_id": 4,
        }
        response = add_appointment_booking(parse.urlencode(query_params))
        
        # Confirm appointment scheduling
        responses.append({"role": "assistant", "content": generate_response("Thank you! Your appointment has been scheduled.")})

    return responses

def main():
    callers = [
        {"name": "John Doe", "is_new_user": False, "email": "johndoe@example.com", "mobile": "1234567890", "hospital_id": "123456", "date": "2024-03-15", "time": "10:00 AM"},
        {"name": "Jane Smith", "is_new_user": True, "email": "janesmith@example.com", "mobile": "9876543210", "hospital_id": "", "date": "2024-03-16", "time": "11:00 AM"}
    ]

    responses = appointment_scheduling(callers)
    for response in responses:
        print(f"{response['role']}: {response['content']}")

    print("\n")

    print("Now let's schedule a new appointment:")
    appointment_scheduling()

if __name__ == "__main__":
    main()
