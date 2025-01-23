import streamlit as st
import pandas as pd

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://i.postimg.cc/4xgNnkfX/Untitled-design.png");
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: local;
}}
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
body, .stText, .stMarkdown {{
    color: black !important;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

@st.cache_data
def load_data(file):
    data=pd.read_csv(file)
    return data

data=load_data('car_prices_2.csv')

st.write("PRICE PREDICTION")
def predict():
    st.header("Predict the Price of a Car")

    # Input fields for user input
    Brand = st.selectbox("Car Brand", sorted(set(data.brand)))
    Year = st.selectbox("Year of Manufacture", sorted(set(data.year)))
    Fuel_Type = st.selectbox("Fuel Type", sorted(set(map(str, data.fuel_type))))
    Transmission = st.selectbox("Transmission", sorted(set((map(str,data.transmission_type)))))
    # Use = st.selectbox("Use", ("Foreign", "Local"))
    Engine_Power = st.selectbox("Engine Capacity (cc)", sorted(set((map(str,data.engine_power)))))
    Seats = st.selectbox("Seats", sorted(set((map(str,data.seating_capacity)))))
    Made_in = st.selectbox("Made In", sorted(set((map(str,data.made_in)))))


    # Predict button
    if st.button("Predict Price"):
        # Prepare the input features
        features = {
            "Brand": Brand,
            "Fuel_Type": Fuel_Type,
            "Transmission": Transmission,
            # "Use": Use,
            "Year": Year,
            # "Mileage": Mileage,
            "Engine_Power": Engine_Power,
            "Seats": Seats,
            "Made in": Made_in
        }

        # Create a DataFrame from features
        features_df = pd.DataFrame([features])
        st.write(features_df)

        # Separate the categorical and numerical columns
        # categorical_features = ['Fuel_Type', 'Transmission', 'Use', 'Brand']
        # numerical_features = ["Year", "Mileage", "Engine", "Seats"]

        # # Extract categorical and numerical data
        # categorical_data = features_df[categorical_features]
        # numerical_data = features_df[numerical_features]

        # # Apply the OneHotEncoder
        # encoded_categorical_data = ohe.transform(categorical_data)
        # X_test_ohe_dense = encoded_categorical_data.toarray()
        # X_test_cat_df = pd.DataFrame(X_test_ohe_dense, columns=ohe.get_feature_names_out(categorical_features))

        # # Apply the StandardScaler to numerical features
        # scaled_numerical_data = scaler.transform(numerical_data)
        # X_test_num_df = pd.DataFrame(scaled_numerical_data, columns=numerical_features)

        # # Combine encoded categorical features with scaled numerical features
        # processed_features = pd.concat([X_test_cat_df, X_test_num_df], axis=1)

        # # Predict the car price
        # price = model.predict(processed_features)
        st.success(f"Estimated Price for {Brand}: Ksh{price}")
