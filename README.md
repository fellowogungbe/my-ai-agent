# ✈️ Global Travel & Expense AI Agent (Nigerian Edition)

This is a Python-based AI travel assistant built using **Streamlit** for the chat interface and the **OpenAI API** for the agent's logic. 

I designed this project specifically for travelers departing from Nigeria. The agent is configured to automatically treat budget inputs as Nigerian Naira (NGN), map out packing lists based on climate, and show destination time zones relative to West African Time (WAT).

---

## 🏗️ Project Files
- **`app.py`**: The main file that runs the Streamlit user interface, remembers the chat history, and manages the loop that allows the AI to choose and run tools.
- **`tools.py`**: A standalone file that holds 5 custom Python functions (the tools). The AI agent calls these functions to get travel data.
- **`.env`**: A hidden text file used to safely store my secret `OPENAI_API_KEY` so it doesn't get exposed in the code.
- **`.gitignore`**: A file that tells Git to ignore background folders like `__pycache__/` and `.venv/` so the repository stays clean.
- **`requirements.txt`**: A list of the Python packages needed to run this application.

---

## 🛠️ The 5 Travel Tools Built In
1. `get_current_weather`: Looks up the temperature and weather conditions for a city.
2. `convert_currency`: Converts budgets from Nigerian Naira (NGN) into foreign currencies (like Euros or Yen).
3. `get_local_time`: Figures out the time zone of the destination and calculates how many hours ahead or behind Nigeria it is.
4. `get_packing_recommendations`: Checks the temperature of the destination and outputs a smart wardrobe packing list.
5. `calculate_daily_allowance`: Automatically takes a 15% emergency buffer out of the budget, then splits the remaining money equally across the trip days.

---

## 🚀 How to Run the App

1. Make sure your OpenAI key is saved inside your hidden `.env` file like this:
   ```text
   OPENAI_API_KEY=your-actual-api-key-here
   ```

2. Run the application from your terminal using `uv`:
   ```bash
   uv run streamlit run app.py
   ```

---

## 💡 Project Reflection & Key Takeaways

### Why I Built It This Way
When I first built this project, I tried connecting the weather and currency tools to live online web APIs. However, my internet connection kept blocking the requests, causing the app to freeze up and throw network errors like `NameResolutionError`. 

To solve this, I moved the data directly into a local matrix inside `tools.py`. This fixed the problem completely. Now the app runs instantly in less than a second, doesn't rely on an active internet connection to process data, and still allows the AI to choose and use tools correctly.

### What I Learned (Engineering Challenges)

1. **Fixing the Infinite Loop:** Because my prompt asks for multiple things at once (weather, budget, time), the AI kept trying to run tools over and over again in circles, which froze the Streamlit screen. I fixed this by adding a `while` loop with a maximum limit of 3 turns. As soon as the AI finishes gathering the tool data, the code forces it to break out of the loop and give the final answer.
2. **Handling Modern OpenAI Variables:** I hit a frustrating error where Python said `TypeError: 'ChatCompletionMessage' object is not subscriptable`. I discovered this happens because the newest OpenAI library returns data as a complex object instead of a standard dictionary, meaning `msg["role"]` crashes the app on a page refresh. I fixed this by adding code that safely checks if the message is an object or a dictionary, allowing the chat history to reload perfectly.
3. **Adding Local Context:** Building this for a Nigerian context taught me how powerful system prompts are. By simply telling the AI to view budgets as Naira and compare times to West African Time, a standard travel tool instantly became highly practical for users here at home.
