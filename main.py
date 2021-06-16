import requests
import os
from twilio.rest import Client
import config
from twilio.http.http_client import TwilioHttpClient
import datetime as dt


OWM_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = config.OWM_api_key
account_sid = config.twilio_account_sid
auth_token = config.twilio_auth_token

parameters = {
    "lat": 51.657909,
    "lon": -0.270480,
    "appid": api_key,
    "exclude": "current,minutely,daily,alerts"

}

response = requests.get(url=OWM_endpoint, params=parameters)
response.raise_for_status()
print(response.status_code)

weather_data = response.json()

weather_slice = weather_data["hourly"][:13]

will_rain = False

for hour_data in weather_slice:
    if hour_data['weather'][0]['id'] <= 700:
        proxy_client = TwilioHttpClient()
        proxy_client.session.proxies = {'https': os.environ['https_proxy']}
        ts = hour_data["dt"]
        time_now = dt.datetime.utcfromtimestamp(ts).strftime('%H:%M')
        print(f"It's going to rain at {time_now}")
        will_rain = True

if will_rain:
    client = Client(account_sid,auth_token,http_client=proxy_client)
    message = client.messages.\
        create(
                 body="It's going to rain today, bring an umbrella.",
                 from_='+12016279239',
                 to=config.receiving_number
                )
    print(message.status)

