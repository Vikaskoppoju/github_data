import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load dataset from the provided CSV file paths
data = pd.read_csv('./archive/repo_data.csv')
data2 = pd.read_csv('./archive/github_dataset.csv')

# Set the title of the dashboard
st.title('GitHub Repositories Dashboard')

# Function to create and display bar charts using Streamlit's built-in methods
def create_bar_chart(data, x_column, y_column, title):
    st.write(f"### {title}")
    st.bar_chart(data.set_index(x_column)[y_column])

# Function to create and display pie charts using Plotly
def create_pie_chart(data, title):
    st.write(f"### {title}")
    fig, ax = plt.subplots()
    ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90, 
           colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff6666', '#66ccff', 
                   '#99cc99', '#cc99ff', '#cc6666', '#6699ff', '#99ffcc', '#ffcc66'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

# Fetch the top repositories for different metrics
top_stars_repo = data.nlargest(1, 'stars_count').iloc[0]
top_forks_repo = data.nlargest(1, 'forks_count').iloc[0]
top_watchers_repo = data.nlargest(1, 'watchers').iloc[0]
top_pull_requests_repo = data.nlargest(1, 'pull_requests').iloc[0]

# Defining the style for centering content and making the tile look better
centered_text_style = """
    <style>
    .tile-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 150px; /* Increased height */
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        margin: 10px;
        background-color: #111827; /* Background color */
        color: white; /* Text color */
        transition: width 0.3s; /* Smooth transition for width change */
    }
    .tile-title {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .tile-metric {
        font-size: 16px;
        font-weight: bold;
        margin-top: 5px;
        display: flex;
        align-items: center; /* Align items vertically centered */
    }
    svg {
        width: 20px; /* Adjust icon size */
        height: 20px; /* Adjust icon size */
        fill: white; /* Change color to white */
        margin-right: 5px; /* Add space between icon and text */
    }

    @media (max-width: 600px) {
        .tile-container {
            width: calc(100% - 20px); /* Adjust width for small screens */
        }
    }
    </style>
"""

# Function to create a tile for repository metrics
def create_repo_tile(title, metric, metric_value, count, svg_icon=None):
    svg_part = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" id="git-fork">{svg_icon}</svg>' if svg_icon else ''
    return f"""
    <div class="tile-container">
        <div class="tile-title">{title}</div>
        <div class="tile-metric">{svg_part} {metric} {metric_value} ({count})</div>
    </div>
    """

# Render the style for the page
st.markdown(centered_text_style, unsafe_allow_html=True)

# Creating two rows with two columns each
row1 = st.columns(2)  # First row will have two columns
row2 = st.columns(2)  # Second row will have two columns

# Top repository by stars count
with row1[0]:
    st.markdown(create_repo_tile(
        "Top Stars Repository",
        "⭐",
        top_stars_repo['name'],
        top_stars_repo['stars_count'],  # Include stars count
    ), unsafe_allow_html=True)

# Top repository by forks count
with row1[1]:
    st.markdown(create_repo_tile(
        "Top Forks Repository",
        "🍴",
        top_forks_repo['name'],
        top_forks_repo['forks_count'],
          f"""
            <rect width="256" height="256" fill="none"></rect>
            <circle cx="128" cy="188" r="28" fill="none" stroke="white" stroke-linecap="round" stroke-linejoin="round" stroke-width="12"></circle>
            <circle cx="188" cy="67.998" r="28" fill="none" stroke="white" stroke-linecap="round" stroke-linejoin="round" stroke-width="12"></circle>
            <circle cx="68" cy="67.998" r="28" fill="none" stroke="white" stroke-linecap="round" stroke-linejoin="round" stroke-width="12"></circle>
            <path fill="none" stroke="white" stroke-linecap="round" stroke-linejoin="round" stroke-width="12" d="M68,95.99756v8.002a24,24,0,0,0,24.00049,24l72-.00146a24,24,0,0,0,23.99951-24V95.99756"></path>
            <line x1="128.002" x2="128" y1="128" y2="160" fill="none" stroke="white" stroke-linecap="round" stroke-linejoin="round" stroke-width="12"></line>
        """  # Include forks count
    ), unsafe_allow_html=True)

# Top repository by watchers count
with row2[0]:
    st.markdown(create_repo_tile(
        "Top Watchers Repository",
        "👁",
        top_watchers_repo['name'],
        top_watchers_repo['watchers'],  # Include watchers count
    ), unsafe_allow_html=True)

# Top repository by pull requests count
with row2[1]:
    st.markdown(create_repo_tile(
        "Top Pull Requests Repository",
        "📋",
        top_pull_requests_repo['name'],
        top_pull_requests_repo['pull_requests'],  # Include pull requests count
    ), unsafe_allow_html=True)
st.write("")
st.write("")
# Create two columns for side-by-side pie charts
co1, co2 = st.columns(2)

# First column: Top 10 Languages Pie Chart
with co1:
    language_data = data2['language'].dropna()
    language_counts = language_data.value_counts().head(10)
    create_pie_chart(language_counts, 'Language Usage in Repositories (Top 10)')

# Second column: Top 5 Languages Pie Chart
with co2:
    bins = [0, 1, 100, 500, 1000]  # Adjust the bins as needed
    labels = ['0', '1-100', '101-500', '501-1000']  # Labels for bins

    # Create a new column for issues category
    data2['issues_category'] = pd.cut(data2['issues_count'], bins=bins, labels=labels, right=False)

    # Count occurrences of each category
    issues_counts = data2['issues_category'].value_counts()

    # Create pie chart using the existing create_pie_chart function
    create_pie_chart(issues_counts, 'Issues Count Distribution (Top 10)')

st.write("")

# Top 10 Repositories by Stars Count, Forks Count, and Watchers Count
top_10_stars = data.nlargest(10, 'stars_count')
top_10_forks = data.nlargest(10, 'forks_count')
top_10_watchers = data.nlargest(10, 'watchers')

create_bar_chart(top_10_stars, 'name', 'stars_count', 'Top 10 Repositories by Stars Count')
create_bar_chart(top_10_forks, 'name', 'forks_count', 'Top 10 Repositories by Forks Count')
create_bar_chart(top_10_watchers, 'name', 'watchers', 'Top 10 Repositories by Watchers Count')
st.write("### First Dataset:")
st.dataframe(data)
# Data for Stars Count, Forks Count, and Issues Count in second dataset
top_10_stars_data2 = data2.nlargest(10, 'stars_count')
top_10_forks_data2 = data2.nlargest(10, 'forks_count')
top_10_issues_data2 = data2.nlargest(10, 'issues_count')

# Create bar charts for second dataset
create_bar_chart(top_10_stars_data2, 'repositories', 'stars_count', 'Top 10 Repositories by Stars Count (Data2)')
create_bar_chart(top_10_forks_data2, 'repositories', 'forks_count', 'Top 10 Repositories by Forks Count (Data2)')
create_bar_chart(top_10_issues_data2, 'repositories', 'issues_count', 'Top 10 Repositories by Issues Count (Data2)')


st.write("### Second Dataset:")
st.dataframe(data2)  # Display second dataset in a table


st.write("Created By Vikas Kumar Koppoju")
st.write("koppojuvikaskumar@gmail.com")
st.write("https://vikaskoppoju.vercel.app/")
