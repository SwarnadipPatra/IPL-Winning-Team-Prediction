import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="wide"
)

pipe = pickle.load(open('pipe.pkl','rb'))

st.markdown(
    "<h1 style='text-align:center;color:#ff4b4b;'>🏏 IPL Winning Team Predictor</h1>",
    unsafe_allow_html=True
)

st.write("")

teams = [
    'Chennai Super Kings',
    'Mumbai Indians',
    'Royal Challengers Bengaluru',
    'Kolkata Knight Riders',
    'Sunrisers Hyderabad',
    'Rajasthan Royals',
    'Delhi Capitals',
    'Punjab Kings',
    'Gujarat Titans',
    'Lucknow Super Giants'
]


team_colors = {
    "Chennai Super Kings": "#fdb913",
    "Mumbai Indians": "#004ba0",
    "Royal Challengers Bengaluru": "#d71920",
    "Kolkata Knight Riders": "#3a225d",
    "Sunrisers Hyderabad": "#ff822a",
    "Rajasthan Royals": "#ea1a85",
    "Delhi Capitals": "#17479e",
    "Punjab Kings": "#ed1b24",
    "Gujarat Titans": "#1c2c5b",
    "Lucknow Super Giants": "#00aaff"
}


cities = [
    'Ahmedabad','Bangalore','Chennai','Delhi','Hyderabad',
    'Jaipur','Kolkata','Lucknow','Mohali','Mumbai',
    'Pune','Sharjah','Dubai','Visakhapatnam'
]

col1, col2, col3 = st.columns(3)

with col1:
    batting_team = st.selectbox("Batting Team", sorted(teams))

with col2:
    bowling_options = [team for team in teams if team != batting_team]
    bowling_team = st.selectbox("Bowling Team", sorted(bowling_options))

with col3:
    city = st.selectbox("Match City", sorted(cities))

st.write("")


target = st.number_input("Target Score", min_value=1, max_value=300)

st.subheader("Match Situation")


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    score = st.number_input("Current Score", min_value=0, max_value=300)

with col2:
    overs = st.number_input("Overs Completed", min_value=0, max_value=20, step=1)

with col3:
    if overs == 20:
        balls = 0
        st.number_input("Balls", value=0, disabled=True)
    else:
        balls = st.number_input("Balls", min_value=0, max_value=5)

with col4:
    wickets = st.number_input("Wickets Out", min_value=0, max_value=10)

with col5:
    st.write("")
    st.write("")
    predict = st.button("Predict Probability")


if predict:

    balls_bowled = overs * 6 + balls
    balls_left = 120 - balls_bowled
    runs_left = target - score
    wickets_left = 10 - wickets

    if balls_bowled > 0:
        crr = score / (balls_bowled / 6)
    else:
        crr = 0

    if balls_left > 0:
        rrr = (runs_left * 6) / balls_left
    else:
        rrr = 0

    input_df = pd.DataFrame({
        'batting_team':[batting_team],
        'bowling_team':[bowling_team],
        'city':[city],
        'runs_left':[runs_left],
        'balls_left':[balls_left],
        'wickets':[wickets_left],
        'total_runs_x':[target],
        'crr':[crr],
        'rrr':[rrr]
    })

    result = pipe.predict_proba(input_df)

    loss = result[0][0]
    win = result[0][1]

    win_percent = int(win * 100)
    loss_percent = int(loss * 100)

    bat_color = team_colors[batting_team]
    bowl_color = team_colors[bowling_team]

    st.write("")
    st.markdown("## 🆚 Match Winning Probability")


    col1, col2, col3 = st.columns([3,6,3])

    with col1:
        st.markdown(
            f"<h3 style='text-align:center'>{batting_team}</h3>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<h1 style='text-align:center;color:{bat_color}'>{win_percent}%</h1>",
            unsafe_allow_html=True
        )

    with col2:

        bar_html = f"""
        <div style="width:100%; background-color:#ddd; border-radius:12px; overflow:hidden; height:40px;">
            <div style="width:{win_percent}%; background-color:{bat_color}; height:40px; float:left;"></div>
            <div style="width:{loss_percent}%; background-color:{bowl_color}; height:40px; float:right;"></div>
        </div>
        """

        st.markdown(bar_html, unsafe_allow_html=True)

    with col3:
        st.markdown(
            f"<h3 style='text-align:center'>{bowling_team}</h3>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<h1 style='text-align:center;color:{bowl_color}'>{loss_percent}%</h1>",
            unsafe_allow_html=True
        )

    st.write("")

    st.markdown("### 📊 Match Stats")

    stat1, stat2, stat3 = st.columns(3)

    with stat1:
        st.metric("Runs Left", runs_left)

    with stat2:
        st.metric("Balls Left", balls_left)

    with stat3:
        st.metric("Required Run Rate", round(rrr,2))