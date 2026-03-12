import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter city name:")
        self.city_input = QLineEdit()
        self.get_weather_button = QPushButton("Get Weather")

        self.temperature_label = QLabel("")
        self.emoji_label = QLabel("")
        self.description_label = QLabel("")
        self.extra_info_label = QLabel("")

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.resize(400, 500)

        layout = QVBoxLayout()

        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.emoji_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.extra_info_label)

        self.setLayout(layout)

        # Alignment
        for widget in [
            self.city_label,
            self.city_input,
            self.temperature_label,
            self.emoji_label,
            self.description_label,
            self.extra_info_label
        ]:
            widget.setAlignment(Qt.AlignCenter)

        # Object names
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.extra_info_label.setObjectName("extra_info_label")

        # Style
        self.setStyleSheet("""
        QLabel, QPushButton{
            font-family: Calibri;
        }

        QLabel#city_label{
            font-size: 40px;
            font-style: italic;
        }

        QLineEdit#city_input{
            font-size: 40px;
        }

        QPushButton#get_weather_button{
            font-size: 30px;
            font-weight: bold;
        }

        QLabel#temperature_label{
            font-size: 75px;
        }

        QLabel#emoji_label{
            font-size: 100px;
            font-family: Segoe UI Emoji;
        }

        QLabel#description_label{
            font-size: 50px;
        }

        QLabel#extra_info_label{
            font-size: 25px;
        }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        city = self.city_input.text().strip()

        if not city:
            self.display_error("Please enter a city name")
            return

        api_key = "62d33d7f7a31db4cdaf58a8f0e6c8c85"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            if response.status_code == 200:
                self.display_weather(data)
            else:
                self.display_error("City not found")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck Internet")

        except requests.exceptions.Timeout:
            self.display_error("Request Timed Out")

        except Exception as e:
            self.display_error(str(e))

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        self.extra_info_label.clear()

    def display_weather(self, data):

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_id = data["weather"][0]["id"]
        description = data["weather"][0]["description"]

        self.temperature_label.setStyleSheet("font-size:75px;")

        self.temperature_label.setText(f"{temperature:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(description.capitalize())

        self.extra_info_label.setText(
            f"Humidity: {humidity}%  |  Wind: {wind_speed} m/s"
        )

    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "🍃"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())              
