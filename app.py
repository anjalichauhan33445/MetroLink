import streamlit as st
import pandas as pd
import joblib
import plotly.express as px


# load model

model = joblib.load('metrolink_model.joblib')

# -----------------------------
# page configuration
# -----------------------------
st.set_page_config(page_title="Metro Crowd Predictor 🚆", layout="wide", page_icon="🚆")
st.title("🚆 Metro Crowd Predictor")
st.subheader("Predict crowd levels at Noida Metro stations")
st.markdown("Use the sidebar to input details and see how crowd levels change throughout the day.")

# -----------------------------
# sidebar inputs
# -----------------------------
st.sidebar.header("Input Parameters")

stations = {
    1: "Noida Sector 142", 2: "Noida Sector 143", 3: "Noida Sector 144",
    4: "Noida Sector 145", 5: "Noida Sector 146", 6: "Noida Sector 147",
    7: "Noida Sector 148", 8: "Knowledge Park II", 9: "Pari Chowk",
    10: "Alpha 1", 11: "Delta 1", 12: "GNIDA Office", 13: "Depot Station"
}

station_id = st.sidebar.selectbox(
    "Select Station",
    options=list(stations.keys()),
    format_func=lambda x: f"{x} - {stations[x]}"
)

days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
        4: "Friday", 5: "Saturday", 6: "Sunday"}
day_of_week = st.sidebar.selectbox(
    "Day of Week",
    options=list(days.keys()),
    format_func=lambda x: days[x]
)

time_of_day = st.sidebar.slider(
    "Time of Day (Hour)",
    min_value=0, max_value=23, value=12,
    format="%d:00",
    help="Pick the hour (24-hour format) for single predictions"
)

is_holiday = st.sidebar.selectbox("Holiday?", ["No", "Yes"])
is_holiday = 1 if is_holiday == "Yes" else 0

weather_options = {"Sunny ☀️": 0, "Rainy 🌧️": 1, "Cloudy ☁️": 2}
weather_choice = st.sidebar.selectbox("Weather", options=list(weather_options.keys()))
weather = weather_options[weather_choice]

nearby_events = st.sidebar.slider("Number of Nearby Events", min_value=0, max_value=10, value=0)
temperature = st.sidebar.number_input("Temperature (°C)", min_value=-10, max_value=50, value=25)
platform_capacity = st.sidebar.selectbox("Platform Capacity", options=[300, 500, 700, 900])

st.markdown("---")
st.subheader("Crowd Prediction")


# Single-hour Prediction

if st.button("Predict Current Hour Crowd"):
    input_data = pd.DataFrame([{
        'station_id': station_id,
        'time_of_day': time_of_day,
        'day_of_week': day_of_week,
        'is_holiday': is_holiday,
        'weather': weather,
        'nearby_events': nearby_events,
        'temperature': temperature,
        'platform_capacity': platform_capacity
    }])

    prediction = model.predict(input_data)[0]

    # Color-coded display
    if str(prediction).lower() in ["low", "light"]:
        color = "green"
    elif str(prediction).lower() in ["medium", "moderate"]:
        color = "orange"
    else:
        color = "red"

    st.markdown(f"<h2 style='color:{color};'>Predicted Crowd Level: {prediction}</h2>", unsafe_allow_html=True)


# full-day prediction grph 

if st.button("Predict Full-Day Crowd"):
    hours = list(range(24))
    predictions = []
    colors = []

    for hour in hours:
        input_data = pd.DataFrame([{
            'station_id': station_id,
            'time_of_day': hour,
            'day_of_week': day_of_week,
            'is_holiday': is_holiday,
            'weather': weather,
            'nearby_events': nearby_events,
            'temperature': temperature,
            'platform_capacity': platform_capacity
        }])
        pred = model.predict(input_data)[0]
        pred_lower = str(pred).lower()
        if pred_lower in ["low", "light"]:
            predictions.append(0.3)
            colors.append("green")
        elif pred_lower in ["medium", "moderate"]:
            predictions.append(0.6)
            colors.append("orange")
        else:
            predictions.append(1.0)
            colors.append("red")

    # convert to 12-hour labels
    def to_12hr(h):
        suffix = "AM" if h < 12 else "PM"
        hour = h if 1 <= h <= 12 else h-12 if h>12 else 12
        return f"{hour} {suffix}"

    df_plot = pd.DataFrame({
        "Hour": [to_12hr(h) for h in hours],
        "Crowd Level": predictions,
        "Color": colors
    })

    # plot using plotly
    fig = px.scatter(df_plot, x="Hour", y="Crowd Level", color="Color",
                     color_discrete_map={"green":"green","orange":"orange","red":"red"},
                     size_max=15, size=[10]*len(df_plot), labels={"Crowd Level":"Crowd Intensity"},
                     title=f"Full-Day Crowd Prediction for {stations[station_id]}")
    fig.update_traces(mode='lines+markers', line=dict(width=4))
    st.plotly_chart(fig, use_container_width=True)

    # peak hour
    peak_hour = hours[predictions.index(max(predictions))]
    st.markdown(f"**Peak Crowd Hour:** {to_12hr(peak_hour)} - {stations[station_id]}")

st.markdown("---")
st.markdown("Made with ❤️ by Anjali | Metro Crowd Predictor Demo")