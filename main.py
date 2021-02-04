import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = 'nawodya135@gmail.com'
MY_PASSWORD = 'EMAIL_PASSWORD'

MY_LAT = 7.5554942
MY_LONG = 80.7137847


def is_iss_overhead():
    r = requests.get('http://api.open-notify.org/iss-now.json')
    r.raise_for_status()
    data = r.json()

    iss_latitude = float(data['iss_position']['latitude'])
    iss_longitude = float(data['iss_position']['longitude'])

    if MY_LAT -5  <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True

def is_night():

    parameters = {
        'lat' : MY_LAT,
        'lng': MY_LONG,
        'formatted':0,
    }
    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data['results']['sunrise'].split("T")[1].split(":")[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])
 
    time_now = datetime.now().hour
    
    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP('smtp.gmail.com')
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr='nawody135@gmail.com',
            to_addrs=MY_EMAIL,
            msg="Subject: Look Up 👆 \n\n The ISS is above you in the sky.."
        )
    else:
        print("ISS is not above you in the sky..")
