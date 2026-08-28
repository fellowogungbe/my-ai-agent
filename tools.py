import json

# =====================================================================
# NIGERIAN CONTEXT TOOL 1: Weather (Bypasses network blocks)
# =====================================================================
def get_current_weather(city: str):
    """Fetches the current temperature and weather description for a given city."""
    city_lower = city.lower()
    
    mock_weather = {
        "paris": {"temp_celsius": 14.5, "condition": "light drizzle"},
        "london": {"temp_celsius": 12.0, "condition": "overcast clouds"},
        "tokyo": {"temp_celsius": 22.4, "condition": "clear sky"},
        "new york": {"temp_celsius": 18.1, "condition": "scattered clouds"}
    }
    
    data = mock_weather.get(city_lower, {"temp_celsius": 20.0, "condition": "partly cloudy"})
    
    return json.dumps({
        "city": city.title(),
        "temp_celsius": data["temp_celsius"],
        "condition": data["condition"]
    })

# =====================================================================
# NIGERIAN CONTEXT TOOL 2: Currency Converter (Base: NGN Naira)
# =====================================================================
def convert_currency(amount: float, from_currency: str, to_currency: str):
    """Converts a monetary budget amount between Naira (NGN) and international currencies using recent standard parallel/baseline metrics."""
    from_curr = from_currency.upper()
    to_curr = to_currency.upper()
    
    # Custom exchange matrix handling Naira (NGN) as the localized base
    # Rates approximated for educational simulation context
    rates = {
        ("NGN", "USD"): 0.00063,  # 1 Naira to USD
        ("NGN", "EUR"): 0.00058,  # 1 Naira to EUR
        ("NGN", "GBP"): 0.00049,  # 1 Naira to GBP
        ("USD", "NGN"): 1580.00,  # 1 USD to Naira
        ("EUR", "NGN"): 1720.00   # 1 EUR to Naira
    }
    
    rate = rates.get((from_curr, to_curr), 1.0)
    converted_total = amount * rate
    
    return json.dumps({
        "original_amount": amount,
        "from": from_curr,
        "to": to_curr,
        "exchange_rate": rate,
        "converted_total": round(converted_total, 2)
    })

# =====================================================================
# NIGERIAN CONTEXT TOOL 3: Timezone Relative to WAT (Nigeria)
# =====================================================================
def get_local_time(city: str):
    """Fetches the current timezone offset and calculates the exact hours difference relative to West African Time (WAT / Nigeria)."""
    city_lower = city.lower()
    
    # WAT is UTC+1. We map destinations relative to Nigeria's offset
    mock_timezones = {
        "paris": {"offset": "UTC+2", "vs_nigeria": "1 hour ahead of Nigeria (WAT)"},
        "london": {"offset": "UTC+1", "vs_nigeria": "Same time as Nigeria (WAT)"},
        "tokyo": {"offset": "UTC+9", "vs_nigeria": "8 hours ahead of Nigeria (WAT)"},
        "new york": {"offset": "UTC-4", "vs_nigeria": "5 hours behind Nigeria (WAT)"}
    }
    
    data = mock_timezones.get(city_lower, {"offset": "UTC+0", "vs_nigeria": "Calculated relative to WAT"})
    
    return json.dumps({
        "city": city.title(),
        "destination_timezone": data["offset"],
        "comparison_to_wat": data["vs_nigeria"]
    })

# =====================================================================
# NIGERIAN CONTEXT TOOL 4: Packing Advisor
# =====================================================================
def get_packing_recommendations(temp_celsius: float, condition: str):
    """Generates essential wardrobe packing recommendations based on weather metrics."""
    items = ["International Passport", "Naira Debit Cards (Enabled for international use)", "Universal Travel Adapters", "Basic Travel Medications"]
    
    if temp_celsius < 12:
        items.extend(["Heavy Winter Jacket", "Thermal Underwear", "Gloves/Scarves"])
    elif temp_celsius > 25:
        items.extend(["Sunglasses", "Light Breathable Fabrics", "Sunscreen"])
    else:
        items.extend(["Cardigan or Light Jacket", "Jeans", "Comfortable walking shoes"])
        
    if "rain" in condition.lower() or "drizzle" in condition.lower():
        items.extend(["Compact Umbrella", "Waterproof Raincoat"])
        
    return json.dumps({"recommended_packing_list": items})

# =====================================================================
# NIGERIAN CONTEXT TOOL 5: Daily Expense Budget Calculator
# =====================================================================
def calculate_daily_allowance(total_budget: float, total_days: int):
    """Calculates a daily spending allowance, automatically withholding a 15% emergency cash buffer."""
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
