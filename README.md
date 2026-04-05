# Metro Crowd Predictor

A Python Streamlit app that predicts crowd levels at Noida Metro stations using a pre-trained machine learning model.
This app provides real-time insights into metro station crowd density and helps commuters plan their travel accordingly.

---

## Features

- Predict crowd levels for a specific hour
- Full-day crowd forecast with interactive colored charts
- Configurable parameters:
  - Station
  - Day of the week
  - Time of day
  - Weather
  - Nearby events
  - Holiday
  - Temperature
  - Platform capacity
- Visual indicators for Low / Medium / High crowd levels
- Realistic simulation based on historical patterns and events

---

## Installation

1. Clone the repository  
   git clone https://github.com/anjalichauhan33445/MetroLink.git  

2. Go into the folder  
   cd MetroLink

3. Install dependencies  
   pip install -r requirements.txt  

4. Run the app  
   streamlit run app.py  

Open in browser: http://localhost:8501

---

## File Structure

MetroLinkT/
- app.py
- metro_crowd_data.csv
- data.ipynb
- metro_link.ipynb
- requirements.txt
- README.md
- .gitignore


---

## How It Works

1. Users select station, day, time, weather, events, and other parameters
2. The model predicts a crowd score
3. Output is shown as Low / Medium / High
4. Charts visualize crowd trends across the day

---

## Customization

- Edit stations in app.py
- Modify features like weather/events
- Replace with your own trained model

---

## License

Free to use and modify.
