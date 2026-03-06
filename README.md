# Atmosphere Count Calculator

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A comprehensive atmospheric condition analyzer that combines real-time weather data and news sentiment analysis to calculate an "Atmosphere Count" - a unified score representing the overall environmental and social atmosphere of a location.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Atmosphere Count Calculator is a Python-based tool that provides a quantitative measure of atmospheric conditions by analyzing:
- **Weather data**: Temperature, humidity, pressure, wind speed, visibility, and air quality
- **News sentiment**: Impact of current events and headlines on the overall atmosphere

![Screenshot_6-3-2026_23131_127 0 0 1](https://github.com/user-attachments/assets/ccc8c44f-cbb1-4aa9-ac2a-234c91daab3f)

The result is a score from 0-100 that helps users understand the current environmental and social conditions of any location.

### Core Capabilities
- **Weather Analysis**: Evaluates multiple weather parameters for comfort levels
- **News Sentiment Analysis**: Analyzes news headlines for positive/negative impact
- **Combined Scoring**: Weighted algorithm combining weather (60%) and news (40%)
- **Real-time Monitoring**: Track atmospheric conditions over time
- **Trend Analysis**: Identify patterns and changes in atmospheric conditions

### Scoring Categories
| Score Range | Category | Description |
|------------|----------|-------------|
| 80-100 | Excellent | Perfect atmospheric conditions |
| 60-79 | Good | Pleasant atmospheric conditions |
| 40-59 | Moderate | Average atmospheric conditions |
| 20-39 | Poor | Unpleasant atmospheric conditions |
| 0-19 | Severe | Very challenging atmospheric conditions |

## How It Works

### Weather Factor Calculation
The weather score is calculated using weighted factors:

```python
weather_score = (
    temperature_factor * 0.20 +
    humidity_factor * 0.15 +
    pressure_factor * 0.15 +
    wind_factor * 0.15 +
    visibility_factor * 0.15 +
    air_quality_factor * 0.20
)
```

### News Sentiment Analysis
News headlines are analyzed using keyword-based sentiment detection:
- Positive keywords: good, great, excellent, peace, joy, etc.
- Negative keywords: bad, crisis, disaster, conflict, war, etc.

### Final Atmosphere Count
```
Atmosphere Count = (Weather Score × 0.6) + (News Score × 0.4)
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install from source
```bash
# Clone the repository
git clone https://github.com/yourusername/atmosphere-count-calculator.git

# Navigate to project directory
cd atmosphere-count-calculator

# Install required dependencies
pip install -r requirements.txt
```

### Quick Install
```bash
pip install atmosphere-calculator
```

## Usage

### Basic Example

```python
from atmosphere_calculator import AtmosphereCalculator

# Initialize the calculator
calculator = AtmosphereCalculator()

# Prepare weather data
weather_data = {
    'temperature': 24,      # °C
    'humidity': 55,         # %
    'pressure': 1015,       # hPa
    'wind_speed': 8,        # km/h
    'visibility': 20,       # km
    'air_quality': 25       # AQI (lower is better)
}

# Prepare news headlines
news_headlines = [
    "Local festival brings joy to community",
    "Beach cleanup successful, environment improving",
    "New park opening celebrated by residents"
]

# Calculate atmosphere count
result = calculator.calculate_atmosphere_count(weather_data, news_headlines)

print(f"Atmosphere Count: {result['atmosphere_count']}/100")
print(f"Category: {result['category']}")
print(f"Weather Score: {result['weather_score']}/100")
print(f"News Score: {result['news_score']}/100")
```

### Advanced Usage with Monitoring

```python
from atmosphere_calculator import AtmosphereMonitor

# Initialize monitor
monitor = AtmosphereMonitor()

# Record atmospheric conditions over time
locations = ["New York", "London", "Tokyo"]
for location in locations:
    weather_data = get_weather_data(location)  # Your weather API call
    news = get_news_headlines(location)        # Your news API call
    
    record = monitor.record_atmosphere(location, weather_data, news)
    
# Get trend analysis
trends = monitor.get_trend_analysis("New York", hours=24)
print(f"Trend direction: {trends['trend_direction']}")
```

### Integration with Real APIs

```python
from atmosphere_calculator import WeatherNewsAPI

# Initialize API handler (mock example)
api = WeatherNewsAPI()

# Get real data
location = "San Francisco"
weather_data = api.get_current_weather(location)
news_headlines = api.get_current_news()

# Calculate atmosphere
calculator = AtmosphereCalculator()
result = calculator.calculate_atmosphere_count(weather_data, news_headlines)

# Make decisions based on result
if result['atmosphere_count'] >= 70:
    print("Perfect for outdoor activities!")
elif result['atmosphere_count'] >= 40:
    print("Consider indoor activities with breaks")
else:
    print("Stay indoors and monitor updates")
```

## API Reference

### `AtmosphereCalculator`

#### `calculate_weather_factor(temperature, humidity, pressure, wind_speed, visibility, air_quality)`
Calculates individual weather factor scores.

#### `analyze_news_sentiment(news_headlines)`
Analyzes news headlines and returns sentiment score.

#### `calculate_atmosphere_count(weather_data, news_headlines)`
Main method to calculate the final atmosphere count.

### `AtmosphereMonitor`

#### `record_atmosphere(location, weather_data, news_headlines)`
Records atmospheric conditions for a specific location.

#### `get_trend_analysis(location, hours=24)`
Analyzes trends over the specified time period.

## Examples

### Complete Working Example

```python
from atmosphere_calculator import demo_atmosphere_calculator

# Run the built-in demo
demo_atmosphere_calculator()
```

### Sample Output
```
============================================================
ATMOSPHERE COUNT CALCULATOR - DEMO
============================================================

 Location: Beach Paradise
----------------------------------------
 ATMOSPHERE COUNT: 85.6/100
 Category: Excellent
 Description: Perfect atmospheric conditions

 Weather Score: 82.4/100
 News Score: 90.2/100

Weather Factors:
  - Temperature: 95.0
  - Humidity: 90.0
  - Pressure: 96.0
  - Wind: 82.0
  - Visibility: 100.0
  - Air Quality: 95.0
```

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/atmosphere-count-calculator.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 atmosphere_calculator/
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- OpenWeatherMap API for weather data inspiration
- NewsAPI for news aggregation concepts
- Contributors and testers who helped refine the algorithm

## Contact

Project Link: [https://github.com/yourusername/atmosphere-count-calculator](https://github.com/yourusername/atmosphere-count-calculator)

## Future Enhancements

- [ ] Add support for more weather parameters (UV index, pollen count)
- [ ] Implement machine learning for improved sentiment analysis
- [ ] Create web dashboard for visualization
- [ ] Add historical data analysis
- [ ] Support for multiple languages in news analysis
- [ ] Mobile app integration
- [ ] Real-time alert system for extreme conditions

