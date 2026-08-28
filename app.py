from dotenv import load_dotenv
load_dotenv()  # This MUST run first to populate keys!

import os
import json
import streamlit as st
from openai import OpenAI
import tools

# =====================================================================
# STREAMLIT UI LAYOUT
# =====================================================================
st.set_page_config(page_title="Global Travel Agent", page_icon="✈️", layout="wide")
st.title("✈️ Global Travel & Expense Agent")
st.subheader("Your AI Co-Pilot for International Trip Planning")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("Controls")
    
    # BONUS FEATURE: Interactive Visitor API Key Input Box
    user_api_key = st.text_input(
        "🔑 Enter Your OpenAI API Key (Optional)",
        type="password",
        help="If you leave this blank, the app will safely fall back to the developer's default credit key."
    )
    
    st.markdown("---")
    if st.button("Cursor Reset 🧹 Clear Chat History"):
        if "messages" in st.session_state:
            del st.session_state["messages"]
        st.rerun()

# --- OPTIMIZED CREDENTIAL EVALUATION ENGINE ---
# Check if the user entered a key in the text field. If not, use the hidden background env secret.
active_api_key = user_api_key if user_api_key.strip() else os.environ.get("OPENAI_API_KEY")

if not active_api_key:
    st.error("❌ Configuration Error: No valid OpenAI API key detected. Please paste an active key into the sidebar to proceed.")
    st.stop()

# Initialize the OpenAI client securely using the dynamically selected key instance
client = OpenAI(api_key=active_api_key)

# Localized System Persona for Nigeria / WAT Context
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "You are a professional travel assistant specialized in helping travelers planning international trips from Nigeria. You MUST chain your 5 available tools to answer prompts. Always assume the user's initial budget is in Nigerian Naira (NGN), convert it cleanly to the destination currency, and explicitly highlight time zones relative to West African Time (WAT)."
        }
    ]

# Safely print conversation history without breaking on OpenAI Objects
for msg in st.session_state.messages:
    role = msg.role if hasattr(msg, "role") else msg.get("role")
    content = msg.content if hasattr(msg, "content") else msg.get("content")
    if role != "system" and content:
        with st.chat_message(role):
            st.write(content)

if user_prompt := st.chat_input("Where are you traveling to, for how long, and what is your budget?"):
    
    with st.chat_message("user"):
        st.write(user_prompt)
        
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Defining tool structural schemas cleanly for the model
    tools_schema = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current temperature and conditions for a specific city.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "The city name, e.g., Tokyo, London"}
                    },
                    "required": ["city"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "convert_currency",
                "description": "Convert currency using live exchange rates.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number", "description": "The money amount to convert"},
                        "from_currency": {"type": "string", "description": "The 3-letter currency code converting from, e.g., USD"},
                        "to_currency": {"type": "string", "description": "The 3-letter currency code converting to, e.g., JPY"}
                    },
                    "required": ["amount", "from_currency", "to_currency"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_local_time",
                "description": "Get the timezone offset relative to UTC for a specific city.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "The city name, e.g., Paris, Sydney"}
                    },
                    "required": ["city"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_packing_recommendations",
                "description": "Get item wardrobe packing suggestions based on a temperature reading and weather description text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "temp_celsius": {"type": "number", "description": "The temperature in Celsius degrees"},
                        "condition": {"type": "string", "description": "The weather condition string, e.g., clear sky, rain, snow"}
                    },
                    "required": ["temp_celsius", "condition"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_daily_allowance",
                "description": "Calculate daily spending allowances from a pool budget and total day integers.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "total_budget": {"type": "number", "description": "The total budget amount to parse"},
                        "total_days": {"type": "integer", "description": "The length of the trip in days"}
                    },
                    "required": ["total_budget", "total_days"]
                }
            }
        }
    ]

    with st.chat_message("assistant"):
        with st.spinner("Agent routing engine active... executing tool workflow..."):
            
            max_iterations = 3
            current_iteration = 0
            
            while current_iteration < max_iterations:
                current_iteration += 1
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages,
                    tools=tools_schema,
                    tool_choice="auto"
                )
                
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls
                
                if tool_calls:
                    st.session_state.messages.append(response_message)
                    
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        st.caption(f"⚙️ Running Tool: `{function_name}`")
                        
                        if function_name == "get_current_weather":
                            tool_output = tools.get_current_weather(city=function_args.get("city"))
                        elif function_name == "convert_currency":
                            tool_output = tools.convert_currency(
                                amount=function_args.get("amount"),
                                from_currency=function_args.get("from_currency"),
                                to_currency=function_args.get("to_currency")
                            )
                        elif function_name == "get_local_time":
                            tool_output = tools.get_local_time(city=function_args.get("city"))
                        elif function_name == "get_packing_recommendations":
                            tool_output = tools.get_packing_recommendations(
                                temp_celsius=function_args.get("temp_celsius"),
                                condition=function_args.get("condition")
                            )
                        elif function_name == "calculate_daily_allowance":
                            tool_output = tools.calculate_daily_allowance(
                                total_budget=function_args.get("total_budget"),
                                total_days=function_args.get("total_days")
                            )
                        else:
                            tool_output = json.dumps({"status": "unknown"})
                        
                        st.caption(f"✅ Tool `{function_name}` processed successfully.")
                        
                        st.session_state.messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": tool_output
                        })
                else:
                    break
            
            final_stream_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                stream=True
            )
            output_text = st.write_stream(final_stream_response)
            st.session_state.messages.append({"role": "assistant", "content": output_text})
