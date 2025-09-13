import requests
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
import io

# Your API key
api_key = "5fd2a7bc80b1d4acc9d3b81d6968633b"

# Function to fetch current weather
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}"
        response = requests.get(url)
        data = response.json()

        if data['cod'] == '404':
            messagebox.showerror("Error", "City not found!")
        else:
            weather = data['weather'][0]['description'].title()
            temp = round(data['main']['temp'])
            feels_like = round(data['main']['feels_like'])
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
            sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')

            # Weather icon
            icon_code = data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url)
            icon_data = icon_response.content
            icon_img = Image.open(io.BytesIO(icon_data))
            icon_photo = ImageTk.PhotoImage(icon_img)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo

            result_text = (
                f"🌍 City: {city}\n"
                f"🌤 Weather: {weather}\n"
                f"🌡 Temperature: {temp}°C (Feels like {feels_like}°C)\n"
                f"💧 Humidity: {humidity}%\n"
                f"💨 Wind Speed: {wind_speed} m/s\n"
                f"🌅 Sunrise: {sunrise}\n"
                f"🌇 Sunset: {sunset}"
            )

            result_label.config(text=result_text)

            # Save to history
            history_listbox.insert(tk.END, f"{city} - {weather}, {temp}°C")

    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error", "Check your internet connection!")

# Function to fetch 5-day forecast
def get_forecast():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&APPID={api_key}"
        response = requests.get(url)
        data = response.json()

        if data['cod'] != "200":
            messagebox.showerror("Error", "City not found!")
        else:
            forecast_text = "📅 5-Day Forecast:\n\n"
            for forecast in data['list'][:5]:  # next 5 forecasts (3-hour intervals)
                time = datetime.fromtimestamp(forecast['dt']).strftime('%d %b %H:%M')
                temp = round(forecast['main']['temp'])
                desc = forecast['weather'][0]['description'].title()
                forecast_text += f"{time}: {temp}°C, {desc}\n"

            forecast_label.config(text=forecast_text)

    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error", "Check your internet connection!")

# Tkinter GUI
root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("500x600")

tk.Label(root, text="Enter City:", font=("Arial", 12)).pack(pady=5)

city_entry = tk.Entry(root, font=("Arial", 12))
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather", command=get_weather, font=("Arial", 12), bg="lightblue").pack(pady=5)
tk.Button(root, text="5-Day Forecast", command=get_forecast, font=("Arial", 12), bg="orange").pack(pady=5)

# Weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Weather result
result_label = tk.Label(root, text="", font=("Arial", 11), justify="left")
result_label.pack(pady=10)

# Forecast result
forecast_label = tk.Label(root, text="", font=("Arial", 10), justify="left")
forecast_label.pack(pady=10)

# History
tk.Label(root, text="🔎 Search History:", font=("Arial", 12)).pack()
history_listbox = tk.Listbox(root, width=50, height=6)
history_listbox.pack(pady=5)

root.mainloop()

