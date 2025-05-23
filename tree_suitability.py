# -*- coding: utf-8 -*-
"""tree_suitability.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15I-xpzJn0YLdAadgFha9FJrKhhs7ajnn
"""

import pandas as pd

# Load data
df = pd.read_csv('greehill.csv')

# Show first 5 rows
print(df.head())

def classify_tree_based_on_scores(env_score, health_score, suitability_score, canopy_score, stability_score):
    if suitability_score >= 0.42 and env_score >= 0.4 and health_score >= 0.4 and canopy_score <= 0.6 and stability_score >= 0.35:
        return 'Highly Suitable'
    elif suitability_score >= 0.28 and env_score >= 0.25 and health_score >= 0.25 and canopy_score <= 0.7 and stability_score >= 0.25:
        return 'Moderately Suitable'
    else:
        return 'Not Suitable'

df['Predicted_Suitability'] = df.apply(
    lambda row: classify_tree_based_on_scores(
        row['Environmental_Score'],
        row['Health_Score'],
        row['Suitability_Score'],
        row['Canopy_Score'],
        row['Stability_Score']
    ), axis=1)

print(df[['Genus', 'Species', 'Street Name And Number', 'Predicted_Suitability']].head())

# Ask client to input location
user_input = input("Enter a street name (e.g., Jalan Perda Utama): ")

# Filter data based on the street name (case-insensitive)
filtered_df = df[df['Street Name And Number'].str.contains(user_input, case=False, na=False)]

# Show how many results found
print(f"\nFound {len(filtered_df)} trees for location '{user_input}':\n")

# Filter only highly or moderately suitable trees
recommended_df = filtered_df[
    filtered_df['Predicted_Suitability'].isin(['Highly Suitable', 'Moderately Suitable'])
]

# Sort by most suitable score
recommended_df = recommended_df.sort_values(by='Suitability_Score', ascending=False)

# Show top 5 recommendations
print("Top Recommended Trees:")
print(recommended_df[['Genus', 'Species', 'Predicted_Suitability', 'Suitability_Score']].head())

recommended_df.to_csv(f'recommendation_for_{user_input.replace(" ", "_")}.csv', index=False)
print(f"\nSaved to recommendation_for_{user_input.replace(' ', '_')}.csv")

for i, row in recommended_df.iterrows():
    print("\n-----------------------------")
    print(f"Genus: {row['Genus']}, Species: {row['Species']}")
    print(f"Predicted Suitability: {row['Predicted_Suitability']}")
    print(f"Suitability Score: {row['Suitability_Score']:.2f}")
    print(f"Environmental Score: {row['Environmental_Score']:.2f}")
    print(f"Health Score: {row['Health_Score']:.2f}")
    print(f"Stability Score: {row['Stability_Score']:.2f}")
    print(f"Canopy Score: {row['Canopy_Score']:.2f}")

import streamlit as st
import pandas as pd

# Title
st.title("Tree Suitability Recommendation System")

# Step 1: Upload Dataset
st.subheader("Step 1: Upload Tree Dataset")
uploaded_file = st.file_uploader("greehill.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Dataset loaded successfully!")
    st.write("Sample data:")
    st.dataframe(df.head())

    # Step 2: Get user input
    st.subheader("Step 2: Enter your location info")
    location_input = st.text_input("Enter your street name or location (e.g., Jalan Perda Utama)")

    if location_input:
        # Step 3: Filter data based on location
        filtered_df = df[df['Street Name And Number'].str.contains(location_input, case=False, na=False)]

        if not filtered_df.empty:
            st.success(f"Found {len(filtered_df)} trees at {location_input}")
            st.dataframe(filtered_df[['Scientific Name', 'Genus', 'Species', 'Suitability_Score', 'Suitability_Label']])
        else:
            st.warning("No trees found at this location.")

# Show filtered recommendations
st.subheader("Recommended Trees")
st.write(recommended_df)

# Bar chart of top 10 trees based on Suitability Score
st.subheader("Top 10 Recommended Trees by Suitability Score")
top10 = recommended_df.sort_values(by="Suitability_Score", ascending=False).head(10)
st.bar_chart(top10.set_index("Scientific Name")["Suitability_Score"])

# Download CSV
st.subheader("Download Recommendations")
csv = recommended_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download as CSV",
    data=csv,
    file_name=f'recommendation_for_{user_input.replace(" ", "_")}.csv',
    mime='text/csv',
)

# Optional filters
st.sidebar.header("Filter Options")

# Suitability filter
suitability_filter = st.sidebar.multiselect(
    "Select Suitability Levels",
    options=recommended_df['Suitability_Label'].unique(),
    default=recommended_df['Suitability_Label'].unique()
)

# Score thresholds
min_stability = st.sidebar.slider("Minimum Stability Score", 0.0, 1.0, 0.0, 0.05)
min_env = st.sidebar.slider("Minimum Environmental Score", 0.0, 1.0, 0.0, 0.05)
min_health = st.sidebar.slider("Minimum Health Score", 0.0, 1.0, 0.0, 0.05)

# Apply filters
filtered_df = recommended_df[
    (recommended_df["Suitability_Label"].isin(suitability_filter)) &
    (recommended_df["Stability_Score"] >= min_stability) &
    (recommended_df["Environmental_Score"] >= min_env) &
    (recommended_df["Health_Score"] >= min_health)
]

