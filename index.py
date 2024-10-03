import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset from the provided Excel file path
data = pd.read_excel('./archive/repo_data.xlsx')

# Apply automatic fixes for column types to make it Arrow-compatible
for col in data.columns:
    if data[col].dtype == 'object':
        try:
            # Try converting columns to numeric, forcing errors to NaN for problematic entries
            data[col] = pd.to_numeric(data[col], errors='coerce')
        except:
            # Convert to string as a fallback if numeric conversion fails
            data[col] = data[col].astype(str)

# Set the title of the dashboard
st.title('GitHub Repositories Dashboard')

# Display the raw data after conversion
st.write("### Raw Data")
st.write(data)

# Visualizing Stars Count by Repository
st.write("### Stars Count by Repository")
fig, ax = plt.subplots()
data.plot(kind='bar', x='name', y='stars_count', ax=ax, color='orange')
st.pyplot(fig)

# Visualizing Forks Count by Repository
st.write("### Forks Count by Repository")
fig, ax = plt.subplots()
data.plot(kind='bar', x='name', y='forks_count', ax=ax, color='blue')
st.pyplot(fig)

# Visualizing Watchers by Repository
st.write("### Watchers Count by Repository")
fig, ax = plt.subplots()
data.plot(kind='bar', x='name', y='watchers', ax=ax, color='green')
st.pyplot(fig)

# Add more visualizations as needed (pull requests, commit counts, etc.)
