# Import the necessary libraries
import requests  # Library for making HTTP requests
import json      # Library for working with JSON data
import tkinter.messagebox as messagebox  # Library for creating message boxes in the GUI
import tkinter as tk # tkinter

# Create a function to center the main window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

# Create a function to set up the initial home screen
def create_home_screen():
    home_frame = tk.Frame(root, bg="light blue")  # Create a frame for the home screen
    home_frame.pack(pady=50)  # Add some padding

    zip_code_label = tk.Label(home_frame, text="Enter Zip Code:", bg="light blue")  # Create a label for Zip Code
    zip_code_label.pack()  # Display the label

    zip_code_entry = tk.Entry(home_frame)  # Create an input field for Zip Code
    zip_code_entry.pack()  # Display the input field

    get_weather_button = tk.Button(home_frame, text="Get Weather", command=lambda: get_weather(zip_code_entry.get()), bg="lightgreen")
    get_weather_button.pack()  # Display a button to fetch weather data

    return home_frame  # Return the home frame

# Create a function to clear frames from the main window
def clear_frames(*frames):
    for frame in frames:
        frame.pack_forget()  # Remove the frame from the window

# Create a function to show the home screen and hide other frames
def show_home_screen():
    clear_frames(aqi_frame, temperature_frame, forecast_frame)  # Hide AQI, temperature, and forecast frames
    back_button.pack_forget()  # Hide the back button
    home_frame.pack()  # Show the home screen

# Create a function to display weather information frames
def show_weather_frames(aqi, temperature_c, weather_description, forecast_message):
    global aqi_frame, temperature_frame, forecast_frame
    clear_frames(home_frame)  # Hide the home frame

    aqi_frame = tk.LabelFrame(root, text="Air Quality", bg="lightblue", padx=10, pady=10)  # Create a frame for air quality
    aqi_frame.pack()  # Display the air quality frame

    aqi_label = tk.Label(aqi_frame, text=f"AQI: {aqi}", bg="lightblue", fg=get_aqi_color(aqi))  # Display the AQI value
    aqi_label.pack()  # Display the AQI label

    temperature_frame = tk.LabelFrame(root, text="Temperature", bg="lightblue", padx=10, pady=10)  # Create a frame for temperature
    temperature_frame.pack()  # Display the temperature frame

    temperature_label = tk.Label(temperature_frame, text=f"Temperature: {temperature_c}°C\nWeather: {weather_description}", bg="lightblue", fg="black")
    temperature_label.pack()  # Display temperature and weather description

    forecast_frame = tk.LabelFrame(root, text="Weather Forecast", bg="lightblue", padx=10, pady=10)  # Create a frame for weather forecast
    forecast_frame.pack()  # Display the forecast frame

    forecast_label = tk.Label(forecast_frame, text=forecast_message, bg="lightblue", fg="black")  # Display the weather forecast
    forecast_label.pack()  # Display the forecast message

    back_button.pack()  # Display the back button

# Create a function to fetch weather data
def get_weather(zip_code):
    if not zip_code.isdigit() or len(zip_code) < 5:
        messagebox.showerror("Invalid ZIP Code", "Please enter a valid ZIP code with at least 5 digits.")  # Show an error message
        return
    elif not zip_code.isnumeric():
        messagebox.showerror("Invalid ZIP Code", "ZIP code must not contain any letters or non-numeric characters.")  # Show an error message
        return

    global aqi_frame, temperature_frame, forecast_frame
    try:
        # Make a request to the first API for air quality
        api_request1 = requests.get(f"https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode={zip_code}&distance=25&API_KEY=50291F57-D2B8-4A51-BE2F-D20C8D11574A")
        data1 = json.loads(api_request1.content)
        aqi = data1[0]['AQI']
        category = data1[0]['Category']['Name']
        city = data1[0]['ReportingArea']

        # Make a request to the second API for current weather
        url = "https://weatherapi-com.p.rapidapi.com/current.json"
        querystring = {"q": f"{city}"}
        headers = {
            "X-RapidAPI-Key": "3f7a419a4bmshedff67ee6b0ede2p173affjsn1119dcb9971b",
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }
        response2 = requests.get(url, headers=headers, params=querystring)
        data2 = response2.json()
        temperature_c = data2['current']['temp_c']
        weather_description = data2['current']['condition']['text']

        # Make a request to the third API for a 3-day forecast
        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
        querystring = {"q": f"{city}", "days": "3"}
        response3 = requests.get(url, headers=headers, params=querystring)
        data3 = response3.json()

        forecast_message = "3-Day Forecast:\n"
        for day_data in data3['forecast']['forecastday'][:3]:
            weekday = day_data['date']
            condition = day_data['day']['condition']['text']
            forecast_message += f"{weekday}: {condition}\n"

        show_weather_frames(aqi, temperature_c, weather_description, forecast_message)  # Display weather information frames

    except Exception as e:
        if aqi_frame:
            aqi_frame.config(text="Error: Unable to fetch weather data", fg="red")
        if temperature_frame:
            temperature_frame.config(text="", fg="black")
        if forecast_frame:
            forecast_frame.config(text="", fg="black")
        show_home_screen()  # Show the home screen on error

# Create a function to determine the color for the AQI value
def get_aqi_color(aqi):
    if 0 <= aqi <= 50:
        return "green"
    elif 51 <= aqi <= 100:
        return "yellow"
    elif 101 <= aqi <= 150:
        return "orange"
    elif 151 <= aqi <= 200:
        return "red"
    elif 201 <= aqi <= 300:
        return "purple"
    else:
        return "darkred"

# Create the main tkinter window
root = tk.Tk()
root.title("Weather App")  # Set the window title
root.configure(bg="lightblue")  # Set the background color
center_window(root, 400, 600)  # Center the window on the screen

home_frame = create_home_screen()  # Create the home screen frame
back_button = tk.Button(root, text="Back", command=show_home_screen, bg="lightcoral")  # Create a back button

# Define frames for AQI, temperature, and forecast
aqi_frame = None
temperature_frame = None
forecast_frame = None

root.mainloop()  # Start the main GUI loop