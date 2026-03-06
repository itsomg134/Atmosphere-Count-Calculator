import requests
import json
from datetime import datetime
import math
from typing import Dict, List, Tuple
import numpy as np

class AtmosphereCalculator:
    """
    A comprehensive atmosphere calculator that combines weather data
    and news sentiment to create an atmospheric condition score.
    """
    
    def __init__(self, weather_api_key=None, news_api_key=None):
        self.weather_api_key = weather_api_key
        self.news_api_key = news_api_key
        self.atmosphere_score = 0
        self.weather_data = {}
        self.news_data = {}
        
    def calculate_weather_factor(self, temperature: float, humidity: float, 
                               pressure: float, wind_speed: float, 
                               visibility: float, air_quality: float) -> Dict:
        """
        Calculate weather-based atmospheric factors
        """
        # Temperature comfort factor (optimal range 18-24°C)
        temp_factor = 100 - min(abs(temperature - 21) * 5, 100)
        
        # Humidity comfort factor (optimal range 40-60%)
        if 40 <= humidity <= 60:
            humidity_factor = 100
        else:
            humidity_factor = 100 - min(abs(humidity - 50) * 2, 50)
        
        # Pressure stability factor (optimal around 1013 hPa)
        pressure_factor = 100 - min(abs(pressure - 1013) * 2, 40)
        
        # Wind comfort factor (optimal 5-15 km/h)
        if wind_speed < 5:
            wind_factor = 70 + (wind_speed * 6)
        elif wind_speed <= 15:
            wind_factor = 100
        else:
            wind_factor = 100 - min((wind_speed - 15) * 4, 60)
        
        # Visibility factor (optimal >10 km)
        visibility_factor = min(visibility * 10, 100)
        
        # Air quality factor (based on AQI, assuming 0-500 scale, lower is better)
        air_quality_factor = max(100 - (air_quality / 5), 0)
        
        # Calculate weighted weather score
        weather_score = (
            temp_factor * 0.20 +
            humidity_factor * 0.15 +
            pressure_factor * 0.15 +
            wind_factor * 0.15 +
            visibility_factor * 0.15 +
            air_quality_factor * 0.20
        )
        
        return {
            'score': weather_score,
            'factors': {
                'temperature': temp_factor,
                'humidity': humidity_factor,
                'pressure': pressure_factor,
                'wind': wind_factor,
                'visibility': visibility_factor,
                'air_quality': air_quality_factor
            }
        }
    
    def analyze_news_sentiment(self, news_headlines: List[str]) -> Dict:
        """
        Analyze news sentiment and its impact on atmosphere
        """
        # Simple sentiment analysis based on keywords
        positive_keywords = ['good', 'great', 'excellent', 'positive', 'improvement', 
                           'success', 'celebration', 'peace', 'joy', 'beautiful']
        negative_keywords = ['bad', 'terrible', 'crisis', 'disaster', 'conflict', 
                           'war', 'accident', 'tragedy', 'fear', 'danger']
        
        total_score = 0
        news_impacts = []
        
        for headline in news_headlines:
            headline_lower = headline.lower()
            positive_count = sum(1 for word in positive_keywords if word in headline_lower)
            negative_count = sum(1 for word in negative_keywords if word in headline_lower)
            
            # Calculate headline impact (-100 to 100)
            if positive_count > 0 or negative_count > 0:
                impact = (positive_count - negative_count) * 20
                impact = max(min(impact, 100), -100)
                news_impacts.append(impact)
                total_score += impact
        
        # Calculate average impact
        if news_impacts:
            avg_impact = sum(news_impacts) / len(news_impacts)
            # Convert to 0-100 scale (0 = very negative, 100 = very positive)
            news_factor = (avg_impact + 100) / 2
        else:
            news_factor = 50  # Neutral if no news
        
        return {
            'score': news_factor,
            'impacts': news_impacts,
            'headlines_analyzed': len(news_headlines)
        }
    
    def calculate_atmosphere_count(self, weather_data: Dict, news_headlines: List[str]) -> Dict:
        """
        Calculate the final atmosphere count combining weather and news
        """
        # Calculate weather factor
        weather_result = self.calculate_weather_factor(
            temperature=weather_data.get('temperature', 20),
            humidity=weather_data.get('humidity', 50),
            pressure=weather_data.get('pressure', 1013),
            wind_speed=weather_data.get('wind_speed', 10),
            visibility=weather_data.get('visibility', 10),
            air_quality=weather_data.get('air_quality', 50)
        )
        
        # Calculate news factor
        news_result = self.analyze_news_sentiment(news_headlines)
        
        # Combined atmosphere count (weighted average)
        atmosphere_count = (
            weather_result['score'] * 0.6 +  # Weather has 60% weight
            news_result['score'] * 0.4        # News has 40% weight
        )
        
        # Determine atmosphere category
        if atmosphere_count >= 80:
            category = "Excellent"
            description = "Perfect atmospheric conditions"
        elif atmosphere_count >= 60:
            category = "Good"
            description = "Pleasant atmospheric conditions"
        elif atmosphere_count >= 40:
            category = "Moderate"
            description = "Average atmospheric conditions"
        elif atmosphere_count >= 20:
            category = "Poor"
            description = "Unpleasant atmospheric conditions"
        else:
            category = "Severe"
            description = "Very challenging atmospheric conditions"
        
        return {
            'atmosphere_count': round(atmosphere_count, 2),
            'category': category,
            'description': description,
            'weather_score': round(weather_result['score'], 2),
            'news_score': round(news_result['score'], 2),
            'weather_factors': weather_result['factors'],
            'news_analysis': {
                'headlines_analyzed': news_result['headlines_analyzed'],
                'average_impact': round(news_result['score'], 2)
            },
            'timestamp': datetime.now().isoformat()
        }

class AtmosphereMonitor:
    """
    Monitor and track atmospheric conditions over time
    """
    
    def __init__(self):
        self.calculator = AtmosphereCalculator()
        self.history = []
        
    def record_atmosphere(self, location: str, weather_data: Dict, news_headlines: List[str]):
        """
        Record atmosphere count for a specific location and time
        """
        result = self.calculator.calculate_atmosphere_count(weather_data, news_headlines)
        
        record = {
            'location': location,
            'data': result
        }
        
        self.history.append(record)
        return record
    
    def get_trend_analysis(self, location: str, hours: int = 24) -> Dict:
        """
        Analyze atmospheric trends for a location
        """
        location_records = [r for r in self.history if r['location'] == location]
        location_records = location_records[-hours:]  # Get last 'hours' records
        
        if len(location_records) < 2:
            return {'message': 'Insufficient data for trend analysis'}
        
        scores = [r['data']['atmosphere_count'] for r in location_records]
        
        trend = {
            'location': location,
            'current': scores[-1],
            'average': np.mean(scores),
            'min': min(scores),
            'max': max(scores),
            'volatility': np.std(scores),
            'trend_direction': 'improving' if scores[-1] > scores[0] else 'declining' if scores[-1] < scores[0] else 'stable'
        }
        
        return trend

def demo_atmosphere_calculator():
    """
    Demo function to showcase the atmosphere calculator
    """
    
    # Initialize the atmosphere monitor
    monitor = AtmosphereMonitor()
    
    # Sample weather data for different scenarios
    weather_scenarios = [
        {
            'location': 'Beach Paradise',
            'weather': {
                'temperature': 24,
                'humidity': 55,
                'pressure': 1015,
                'wind_speed': 8,
                'visibility': 20,
                'air_quality': 25
            },
            'news': [
                "Local festival brings joy to community",
                "Beach cleanup successful, environment improving",
                "New park opening celebrated by residents"
            ]
        },
        {
            'location': 'Mountain Retreat',
            'weather': {
                'temperature': 12,
                'humidity': 65,
                'pressure': 980,
                'wind_speed': 25,
                'visibility': 5,
                'air_quality': 80
            },
            'news': [
                "Storm warning issued for mountain region",
                "Road closures due to heavy rainfall",
                "Rescue teams on standby for emergencies"
            ]
        },
        {
            'location': 'Urban Center',
            'weather': {
                'temperature': 30,
                'humidity': 70,
                'pressure': 1005,
                'wind_speed': 5,
                'visibility': 8,
                'air_quality': 120
            },
            'news': [
                "City council approves new environmental policies",
                "Heat wave continues with no relief in sight",
                "Public transport disruptions due to technical issues"
            ]
        }
    ]
    
    print("=" * 60)
    print("ATMOSPHERE COUNT CALCULATOR - DEMO")
    print("=" * 60)
    
    # Calculate atmosphere for each scenario
    for scenario in weather_scenarios:
        print(f"\n📍 Location: {scenario['location']}")
        print("-" * 40)
        
        # Record atmosphere count
        record = monitor.record_atmosphere(
            scenario['location'],
            scenario['weather'],
            scenario['news']
        )
        
        result = record['data']
        
        print(f"📊 ATMOSPHERE COUNT: {result['atmosphere_count']}/100")
        print(f"📈 Category: {result['category']}")
        print(f"📝 Description: {result['description']}")
        print(f"\n🌤️ Weather Score: {result['weather_score']}/100")
        print(f"📰 News Score: {result['news_score']}/100")
        
        print("\nWeather Factors:")
        for factor, score in result['weather_factors'].items():
            print(f"  - {factor.replace('_', ' ').title()}: {score:.1f}")
        
        print(f"\nNews Analysis: {result['news_analysis']['headlines_analyzed']} headlines analyzed")
        
    print("\n" + "=" * 60)
    print("TREND ANALYSIS")
    print("=" * 60)
    
    # Show trend analysis
    for location in ['Beach Paradise', 'Urban Center']:
        trend = monitor.get_trend_analysis(location)
        print(f"\n📍 {location} Trends:")
        print(f"  Current: {trend['current']:.1f}")
        print(f"  Average: {trend['average']:.1f}")
        print(f"  Range: {trend['min']:.1f} - {trend['max']:.1f}")
        print(f"  Trend: {trend['trend_direction']}")
        print(f"  Volatility: {trend['volatility']:.2f}")

class WeatherNewsAPI:
    """
    Mock API class for demonstration - in real implementation,
    you would connect to actual weather and news APIs
    """
    
    @staticmethod
    def get_current_weather(location):
        """Mock method to get current weather"""
        # In real implementation, this would call OpenWeatherMap or similar API
        return {
            'temperature': 22,
            'humidity': 60,
            'pressure': 1012,
            'wind_speed': 12,
            'visibility': 15,
            'air_quality': 45
        }
    
    @staticmethod
    def get_current_news():
        """Mock method to get current news headlines"""
        # In real implementation, this would call NewsAPI or similar
        return [
            "Global climate summit reaches historic agreement",
            "Local communities adapt to changing weather patterns",
            "New technology helps predict atmospheric conditions"
        ]

# Real-world usage example
def real_world_usage():
    """
    Example of how to use the atmosphere calculator in a real application
    """
    
    print("\n" + "=" * 60)
    print("REAL-WORLD USAGE EXAMPLE")
    print("=" * 60)
    
    # Initialize components
    calculator = AtmosphereCalculator()
    api = WeatherNewsAPI()
    
    # Get real data (mock data in this example)
    location = "San Francisco"
    weather_data = api.get_current_weather(location)
    news_headlines = api.get_current_news()
    
    # Calculate atmosphere count
    result = calculator.calculate_atmosphere_count(weather_data, news_headlines)
    
    print(f"\n📍 Location: {location}")
    print(f"🌡️  Temperature: {weather_data['temperature']}°C")
    print(f"💧 Humidity: {weather_data['humidity']}%")
    print(f"📰 Top News: {news_headlines[0]}")
    print(f"\n✨ Atmosphere Count: {result['atmosphere_count']} - {result['category']}")
    print(f"   {result['description']}")
    
    # Generate recommendations based on atmosphere count
    if result['atmosphere_count'] >= 70:
        print("\n✅ Recommendations: Great day for outdoor activities!")
    elif result['atmosphere_count'] >= 40:
        print("\n⚠️ Recommendations: Consider indoor activities with breaks")
    else:
        print("\n❌ Recommendations: Stay indoors and monitor updates")

if __name__ == "__main__":
    # Run the demo
    demo_atmosphere_calculator()
    
    # Show real-world usage
    real_world_usage()