import requests
from datetime import datetime
import os


GENDER = "Female"
WEIGHT_KG = 57.0
HEIGHT_CM = 154.0
AGE = 50


exercise_text = input("What exercise did you do?: ")


SHEET_USERNAME = os.environ["SHEET_USERNAME"]
SHEET_PASSWORD = os.environ["SHEET_PASSWORD"]
APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]


exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEET_ENDPOINT = os.environ["SHEET_ENDPOINT"]

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}


response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)


today_date = datetime.now().strftime("%d%m%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["nf_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(url=SHEET_ENDPOINT, json=sheet_inputs, auth=(os.environ["SHEET_USERNAME"], os.environ["SHEET_PASSWORD"]))

    print(sheet_response.text)
