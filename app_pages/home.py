

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

@st.cache_data
def load_data(file):
    data=pd.read_csv(file)
    return data

data=load_data('car_prices_2.csv')




def render_home_page():
    """
    Function to recommend restaurants based on restaurant name or cuisine in any state in the database
    """
    with st.container(border=True):          

        st.markdown(
            """
            <style>
            .center-text {
                text-align: center;
                        }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.image('images/banner.webp', use_column_width=True)
        # st.markdown('<h2 class="center-text" style="color: royal blue;">LUXURY VEHICLES</h2>', unsafe_allow_html=True)
        st.markdown('<h3 class="center-text" style="color: royal blue;">EXPLORE THE WORLD OF LUXURY VEHICLES</h3>', unsafe_allow_html=True)

        with st.container(border=True):   
            st.write (" Choose The Car That Tickles Your Fancy!")

            # Split layout into 3 columns for the filters
            col1, col2 = st.columns(2)
            
            # Filter by Brand
            # with col1:
            #     brand = st.selectbox("Select Car Brand", data['brand'].unique())
            # Filter by Brand
            with col1:
                # brand_options = [''] + list(data['brand'].unique())  # Add an empty entry at the start
                brand_options = [''] + sorted(data['brand'].unique())
                brand = st.selectbox("Select Car Brand", brand_options, format_func=lambda x: "Select a brand" if x == "" else x)

            
            # Filter by Make
            with col2:
                make_options = [''] + sorted(data[data['brand'] == brand]['model_number'].unique())  
                make = st.selectbox("Select Car Brand",make_options, format_func=lambda x: "Select a brand" if x == "" else x)
                # make = st.selectbox("Select Car Make", data[data['brand'] == brand]['model_number'].unique())

            # Filter by Year
            # with col3:
            #     year = st.selectbox("Select Car Year", sorted(data[data['model_number'] == make]['year'].unique(), reverse=True))

            # Filter the dataframe based on user input
            filtered_data = data[(data['brand'] == brand) & (data['model_number'] == make)]
            
            # Display the filtered data
            # st.write(f"Showing results for {brand} - {make} ")
            # 
            if not filtered_data.empty:
                for _, row in filtered_data.iterrows():
                    # Display the image
                    st.image(row['image_url'], use_column_width=True)
                    col1, col2 = st.columns(2, gap="large")
    
                    with col1:
                        st.markdown(
                            f"""
                            <style>
                            .aligned-row {{
                                display: flex;
                                justify-content: space-between;
                                width: 100%;
                            }}
                            </style>
                            <div class="aligned-row">
                                <span><b>Brand:</b></span> 
                                <span>{row['brand']}</span>
                            </div>
                            <div class="aligned-row">
                                <span><b>Model Number:</b></span> 
                                <span>{row['model_number']}</span>
                            </div>
                            <div class="aligned-row">
                                <span><b>Price in KES:</b></span> 
                                <span>Ksh{row['price_in_kes']}</span>
                            </div>
                            <div class="aligned-row">
                                <span><b>Price in USD:</b></span> 
                                <span>${row['price_in_usd']}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    with col2:
                        st.markdown(
                            f"""
                            <style>
                            .aligned-row {{
                                display: flex;
                                justify-content: space-between;
                                width: 100%;
                            }}
                            </style>
                            <div class="aligned-row">
                                <span><b>Made In:</b></span> 
                                <span>{row['made_in']}</span>
                            </div>
                            <div class="aligned-row">
                                <span><b>Transmission Type:</b></span> 
                                <span>{row['transmission_type']}</span>
                            </div>
                            <div class="aligned-row">
                                <span><b>Fuel Type:</b></span> 
                                <span>{row['fuel_type']}</span>
                            </div>
                            <div class="aligned-row">
                                <span><b>Seating Capacity:</b></span> 
                                <span>{row['seating_capacity']}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    # Add a separator between rows
                    st.markdown("---")

                    
                    # Button to go to purchase page
                    # st.link_button("Click here to purchase", row['car_link'])
                    st.markdown(
                    f"""
                    <style>
                    .center-button {{
                        display: flex;
                        justify-content: center;
                        margin-top: 20px;
                        margin-bottom: 20px;
                    }}
                    </style>
                    <div class="center-button">
                        <a href="{row['car_link']}" target="_blank" style="text-decoration: none;">
                            <button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; font-size: 16px; border-radius: 5px;">
                                Click here to purchase
                            </button>
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                    
                
            else:
                st.write("No cars found matching the selected criteria.")

            
    
        

        

            
            
