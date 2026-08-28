import json

def get_current_weather(city: str):
    """Fetches the current temperature and weather description for a given city."""
    # Ensure city is a string if the model returns a list array format accidentally
    if isinstance(city, list):
        city = city[0]
        
    city_lower = str(city).lower()
    
    mock_weather = {
        "paris": {"temp_celsius": 14.5, "condition": "light drizzle"},
        "london": {"temp_celsius": 12.0, "condition": "overcast clouds"},
        "tokyo": {"temp_celsius": 22.4, "condition": "clear sky"},
        "new york": {"temp_celsius": 18.1, "condition": "scattered clouds"}
    }
    
    data = mock_weather.get(city_lower, {"temp_celsius": 20.0, "condition": "partly cloudy"})
    
    return json.dumps({
        "city": str(city).title(),
        "temp_celsius": data["temp_celsius"],
        "condition": data["condition"]
    })

def convert_currency(amount: float, from_currency, to_currency):
    """Converts a monetary budget amount between Naira (NGN) and international currencies using parallel/baseline metrics."""
    # FIXED: Type introspection logic fixes array conversions if the model returns parameter lists
    if isinstance(from_currency, list):
        from_currency = from_currency[0]
    if isinstance(to_currency, list):
        to_currency = to_currency[0]
        
    from_curr = str(from_currency).upper()
    to_curr = str(to_currency).upper()
    
    rates = {
        ("NGN", "USD"): 0.00063,
        ("NGN", "EUR"): 0.00058,
        ("NGN", "GBP"): 0.00049,
        ("USD", "NGN"): 1580.00,
        ("EUR", "NGN"): 1720.00
    }
    
    rate = rates.get((from_curr, to_curr), 1.0)
    converted_total = float(amount) * rate
    
    return json.dumps({
        "original_amount": amount,
        "from": from_curr,
        "to": to_curr,
        "exchange_rate": rate,
        "converted_total": round(converted_total, 2)
    })

def get_local_time(city: str):
    """Fetches the current timezone offset and calculates the exact hours difference relative to West African Time (WAT / Nigeria)."""
    if isinstance(city, list):
        city = city[0]
        
    city_lower = str(city).lower()
    
    mock_timezones = {
        "paris": {"offset": "UTC+2", "vs_nigeria": "1 hour ahead of Nigeria (WAT)"},
        "london": {"offset": "UTC+1", "vs_nigeria": "Same time as Nigeria (WAT)"},
        "tokyo": {"offset": "UTC+9", "vs_nigeria": "8 hours ahead of Nigeria (WAT)"},
        "new york": {"offset": "UTC-4", "vs_nigeria": "5 hours behind Nigeria (WAT)"}
    }
    
    data = mock_timezones.get(city_lower, {"offset": "UTC+0", "vs_nigeria": "Calculated relative to WAT"})
    
    return json.dumps({
        "city": str(city).title(),
        "destination_timezone": data["offset"],
        "comparison_to_wat": data["vs_nigeria"]
    })

def get_packing_recommendations(temp_celsius: float, condition: str):
    """Generates essential wardrobe packing recommendations based on weather metrics."""
    items = ["International Passport", "Naira Debit Cards", "Universal Travel Adapters"]
    
    try:
        temp_celsius = float(temp_celsius)
    except:
        temp_celsius = 20.0
        
    condition_str = str(condition).lower()
    
    if temp_celsius < 12:
        items.extend(["Heavy Winter Jacket", "Thermal Underwear", "Gloves/Scarves"])
    elif temp_celsius > 25:
        items.extend(["Sunglasses", "Light Breathable Fabrics", "Sunscreen"])
    else:
        items.extend(["Cardigan or Light Jacket", "Jeans", "Comfortable walking shoes"])
        
    if "rain" in condition_str or "drizzle" in condition_str:
        items.extend(["Compact Umbrella", "Waterproof Raincoat"])
        
    return json.dumps({"recommended_packing_list": items})

def calculate_daily_allowance(total_budget: float, total_days: int):
    """Calculates a daily spending allowance, automatically withholding a 15% emergency cash buffer."""
    try:
        total_budget = float(total_budget)
        total_days = int(total_days)
    except:
        return json.dumps({"error": "Invalid numbers entered."})
        
    if total_days <= 0:
        return json.dumps({"error": "Duration must be at least 1 day."})
        
    emergency_buffer = total_budget * 0.15
    spendable_budget = total_budget - emergency_buffer
    daily_allowance = spendable_budget / total_days
    
    return json.dumps({
        "total_budget": total_budget,
        "emergency_buffer_withheld": round(emergency_buffer, 2),
        "total_spendable_pool": round(spendable_budget, 2),
        "days": total_days,
        "recommended_daily_allowance": round(daily_allowance, 2)
    })
