from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import json

from urllib.parse import quote


ua = UserAgent()  # UA object
user_agent = ua.random  # random user agent
headers = {'User-Agent': user_agent}
def encode_to_url(text):
    encoded_string = quote(text)
    return encoded_string


from urllib.parse import quote


def collectData(city):
    encoded_string = quote(city)
    ukrainian_text = f"погода-{city}"
    encoded_url = encode_to_url(ukrainian_text)

    url = f"https://ua.sinoptik.ua/{encode_to_url(ukrainian_text)}"

    res = requests.get(url, headers=headers)
    filename = "weather_data.html"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(res.text)

    print("The page is saved successfully in 'weather_data.html'.")

    soup = BeautifulSoup(res.text, 'lxml')
    current_weather = soup.find_all("div", class_="main")

    weather_array = []

    current_time = soup.find("p", class_ = "today-time").text
    current_temp = soup.find("p", class_="today-temp").text

    for index, days in enumerate(current_weather):
        day_data = {
            "day": days.find(class_="day-link").text if days.find(class_="day-link") else "",
            "date": days.find(class_="date").text if days.find(class_="date") else "",
            "month": days.find(class_="month").text if days.find(class_="month") else "",
            "weather_description": days.find("div", class_="weatherIco").get("title") if days.find("div",class_="weatherIco") else "",
            "min_temp": days.find("div", class_="min").text if days.find("div", class_="min") else "",
            "max_temp": days.find("div", class_="max").text if days.find("div", class_="max") else "",
        }
        if index == 0:
            day_data["current_time"] = current_time
            day_data["current_temp"] = current_temp
        weather_array.append(day_data)

    with open("weather_data.json", "w") as file:
        json.dump(weather_array, file, indent=2)
    return weather_array


def main():
    collectData("Київ")


if __name__ == "__main__":
    main()
