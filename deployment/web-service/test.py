# pylint: disable=line-too-long
import requests

stress_data = {
    "text": "Its like that, if you want or not. ME: I have no problem, if it takes longer. But you asked my friend for help and let him wait for one hour and then you haven’t prepared anything. Thats not what you asked for. Instead of 3 hours, he helped you for 10 hours till 5am...",
    "lex_liwc_Tone": 5.95,
    "lex_liwc_i": 5.45,
    "lex_liwc_negemo": 1.82,
    "lex_liwc_Clout": 57.22,
    "sentiment": 0.0,
}

url = "http://localhost:9696/predict"
response = requests.post(url, json=stress_data)
# print(response)
print(response.json())
