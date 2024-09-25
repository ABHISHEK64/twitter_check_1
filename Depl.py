import streamlit as st
import pandas as pd
import requests
import pickle
import zipfile
import os
st.markdown(
    """
    <style>
    /* Change background color */
    .stApp {
        background-color: black;
        color:white;
    }
    h1{
    color:blue;
    }
    p{
    color:blue
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Path to the zip file
zip_path = r'C:\Users\abhis\OneDrive\Documents\Twitter_cast\Tweets.zip'

# Folder where you want to extract the files
extract_folder = r'C:\Users\abhis\OneDrive\Documents\Twitter_cast\extracted'

# Extract the zip file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)

# Path to the extracted .pkl file
pkl_file = os.path.join(extract_folder, 'Tweets.pkl')
st.title('Tweeter Checking System')
Twitter_list=pickle.load(open(pkl_file,'rb'))
search_term=st.text_input("Enter search term:")
if search_term:
    # Filter the DataFrame for the search term in the 'text' column
    required_df = Twitter_list[Twitter_list['text'].str.contains(search_term, case=False, na=False)]

    # Display total unique tweets
    st.write(f'Total Unique Tweets Posted containing "{search_term}": {required_df["id"].nunique()}')

    # Total Tweets per weekday
    tweet_per_day = required_df['created_at_Weekday'].value_counts().reset_index().rename(columns={'created_at_Weekday': 'Day', 'count': 'Tweets'})
    st.write(f'Total Tweets Posted containing "{search_term}" Each Day:')
    st.write(tweet_per_day)
    st.bar_chart(tweet_per_day.set_index('Day'))

    # Times of day tweets were posted
    time_of_day_data = required_df['time_of_day'].value_counts().reset_index().rename(columns={'time_of_day': 'Time', 'count': 'Tweets'})
    st.write(f'Times of Day When Tweets Were Posted containing "{search_term}":')
    st.write(time_of_day_data)
    st.bar_chart(time_of_day_data.set_index('Time'))

    # Users who posted tweets
    user_tweet_data = required_df['author_handle'].value_counts().head(10).reset_index().rename(columns={'author_handle': 'User', 'count': 'Tweets'})
    st.write(f'Users Who Posted Tweets containing "{search_term}":')
    st.write(user_tweet_data)
    st.bar_chart(user_tweet_data.set_index('User'))

    # Average likes on the tweets
    avg_likes = required_df['like_count'].mean()
    st.write(f'Average Likes on Tweets containing "{search_term}": {avg_likes}')

    # Source of the tweets
    source_data = required_df['source'].value_counts().head(10).reset_index().rename(columns={'source': 'Source', 'count': 'Tweets'})
    st.write(f'Sources of Tweets containing "{search_term}":')
    st.write(source_data)
    st.bar_chart(source_data.set_index('Source'))
