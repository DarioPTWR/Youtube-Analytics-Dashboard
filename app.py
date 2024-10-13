# Import base Streamlit dependency
import streamlit as st 
# Import pandas to load the analytics data
import pandas as pd
# Import youtube module to get the hashtag
import youtube
# Import plotly for visualization
import plotly.express as px
import os

# Setting page configuration
st.set_page_config(page_title='YouTube Analytics Dashboard', page_icon=':bar_chart:', layout='wide')

api_key = st.secrets["RAPIDAPI_KEY"]
api_host = st.secrets["RAPIDAPI_HOST"]

if not api_key or not api_host:
    st.error("API key or host is missing. Please check your environment variables.")
    st.stop()

# Adding custom styles
st.markdown("""
    <style>
        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background-color: #33475b;
            color: white;
        }

        /* Customizing Sidebar Text */
        .sidebar h1 {
            font-size: 1.6rem;
            color: white;
        }

        .sidebar p {
            font-size: 1.1rem;
            color: #f0f2f6;
        }

        /* Header and Section Styling */
        h2 {
            color: #007bff;
        }
    </style>
""", unsafe_allow_html=True)

# Add a sidebar for title, description, and logo
with st.sidebar:
    # Add the logo (use a valid image URL or file path)
    st.image("youtube.png", width=150)
    
    # Add dashboard title
    st.title("Youtube Analytics")
    
    # Add description
    st.markdown("""
    Discover the performance of your YouTube content with powerful analytics. 🚀 Track key metrics, audience engagement, and emerging trends to optimize your content strategy. 📈 Whether you're a creator or marketer, TubeVision helps you make data-driven decisions for growth. 🛩️✨
    """)

    st.sidebar.markdown("**To get started:** <ol><li>Enter the <i>hashtag</i> you wish to analyze.</li> <li>Hit <i>Get Data</i>.</li> <li>Get analyzing.</li></ol>",unsafe_allow_html=True)

# Search input field with a hashtag prompt
st.markdown("<h2 style='text-align: center; color: black;'>YouTube Analytics Dashboard</h2>", unsafe_allow_html=True)
hashtag = st.text_input('Search for a hashtag here', value="")

# Button to trigger data fetch
if st.button('Get Data'):
    result = youtube.get_data(hashtag)
    
    if result is False:
        st.markdown("No data available for this hashtag. Please try a different one.")
    else:
        # Load in data for analysis
        df = pd.read_csv('youtubedata.csv')
        
        # Adding space and padding between sections
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Create a two-column layout for the charts
        col1, col2 = st.columns(2)

        # Pie Chart - Channel Popularity by Views
        with col1:
            st.markdown("### Channel Popularity by Views")
            channel_view_count = df.groupby('Channel Title')['View Count'].sum().reset_index()
            fig_pie = px.pie(channel_view_count, values='View Count', names='Channel Title',
                             hole=0.4, color_discrete_sequence=px.colors.sequential.Plasma)
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(title="Channel Popularity by Views", annotations=[dict(text='Popularity', x=0.5, y=0.5, font_size=20, showarrow=False)])
            st.plotly_chart(fig_pie, use_container_width=True)

        # Scatter Plot - View Count vs. Video Length
        with col2:
           with col2:
            st.markdown("### View Count vs. Video Length")
            fig_scatter = px.scatter(df, x='Video Length Text', y='View Count', color='Channel Title',
                                     size='View Count', hover_data=['Title'], color_discrete_sequence=px.colors.sequential.Viridis)
            fig_scatter.update_layout(title="View Count vs. Video Length", xaxis_title="Video Length", yaxis_title="View Count", showlegend=True)
            st.plotly_chart(fig_scatter, use_container_width=True)

        # Adding space and padding between sections
        st.markdown("<br>", unsafe_allow_html=True)

        # Another two-column layout for additional charts
        col3, col4 = st.columns(2)


        # Top 10 Videos by View Count
        with col3:
            st.markdown("### Top 10 Videos by View Count")
            top_videos = df.nlargest(10, 'View Count')
            fig_bar = px.bar(top_videos, x='Title', y='View Count', color='Channel Title', title="Top 10 Most Popular Videos by Views",
                             text='View Count', color_discrete_sequence=px.colors.sequential.Teal)
            fig_bar.update_layout(xaxis_title="Video Title", yaxis_title="View Count", showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        # Video Length Distribution
        with col4:
            st.markdown("### View Count by Content Duration")
            fig_box_duration = px.box(df, x='Video Length Text', y='View Count',
                                    title="View Count by Content Duration", color_discrete_sequence=px.colors.diverging.RdBu)
            fig_box_duration.update_layout(xaxis_title="Video Length", yaxis_title="View Count")
            st.plotly_chart(fig_box_duration, use_container_width=True)

         # Adding space and padding between sections
        st.markdown("<br>", unsafe_allow_html=True)

        # Full-width histogram chart for View Count Distribution
        st.markdown("### Video View Distribution")
        fig_hist = px.histogram(df, x='View Count', nbins=50, title="View Count Distribution",
                                color_discrete_sequence=['#ff7f0e'])
        fig_hist.update_layout(bargap=0.2)
        st.plotly_chart(fig_hist, use_container_width=True)

        # Average Views per Channel
        # Calculate average views per channel and sort by View Count in descending order
        st.markdown("### Average Views per Channel")
        avg_views_per_channel = df.groupby('Channel Title')['View Count'].mean().reset_index()
        avg_views_per_channel = avg_views_per_channel.sort_values(by='View Count', ascending=False)

        # Create bar chart
        fig_avg_views = px.bar(avg_views_per_channel, x='Channel Title', y='View Count', 
                            title="Average Views per Channel", text='View Count')

        # Update layout
        fig_avg_views.update_layout(xaxis_title="Channel Title", 
                                    yaxis_title="Average View Count", 
                                    showlegend=False)

        st.plotly_chart(fig_avg_views, use_container_width=True)

        # Adding horizontal divider
        st.markdown("---")

        # Tabular view for detailed data exploration
        st.markdown("### Data Overview")
        st.dataframe(df, use_container_width=True)