import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime
from strava_data import StravaDataFetcher

def apply_styling():
    """Apply custom styling to dashboard."""
    st.markdown("""
    <style>
    /* Global Styling */
    .stApp {
        background-color: #f4f6f9;
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }

    /* Metrics Card Design */
    .stMetric {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        padding: 20px;
        transition: transform 0.3s ease;
        border: 1px solid #e1e4e8;
    }
    .stMetric:hover {
        transform: scale(1.03);
    }
    .stMetric-value {
        font-size: 2.2rem;
        color: #2c3e50;
        font-weight: 700;
    }
    .stMetric-label {
        color: #7f8c8d;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Header and Title Styling */
    .stHeader {
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 12px;
        margin-top: 25px;
    }
    .stTitle {
        color: #2c3e50;
        font-weight: 800;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        padding: 15px;
    }
    .sidebar .stSelectbox, .sidebar .stMultiSelect {
        background-color: #f8f9fa;
        border-radius: 8px;
    }

    /* Tab Styling */
    .stTabs > div {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f3f5;
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab-selected"] {
        background-color: #3498db;
        color: white !important;
    }

    /* Profile Image */
    .profile-image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        transition: transform 0.3s ease;
    }
    .profile-image-container:hover {
        transform: scale(1.05);
    }
    .profile-image-border {
        border: 4px solid #3498db;
        border-radius: 50%;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def create_summary_metrics(df):
    """Create summary metrics with visuals and insights."""
    col1, col2, col3 = st.columns(3)
    
    # Total Activities
    with col1:
        total_activities = len(df)
        last_week_activities = len(df.iloc[-7:])
        st.metric(
            "Total Activities", 
            total_activities, 
            delta=f"{total_activities - last_week_activities} vs Last Week",
            delta_color="normal"
        )
    
    # Total Distance
    with col2:
        total_distance = df['distance_km'].sum()
        last_week_distance = df.iloc[-7:]['distance_km'].sum()
        st.metric(
            "Total Distance", 
            f"{total_distance:.2f} km", 
            delta=f"{total_distance - last_week_distance:.2f} km",
            delta_color="normal"
        )
    
    # Average Speed
    with col3:
        avg_speed = df['average_speed_kmh'].mean()
        st.metric(
            "Avg Speed", 
            f"{avg_speed:.2f} km/h", 
            delta_color="off"
        )

def create_activity_filter_sidebar(df):
    """Create an enhanced sidebar for filtering activities with improved UX."""
    st.sidebar.header("🔍 Activity Explorer")
    
    # Collapsible sections for better organization
    with st.sidebar.expander("Activity Types", expanded=True):
        selected_types = st.multiselect(
            "Select Activity Types", 
            df['type'].unique(), 
            default=df['type'].unique(),
            label_visibility="collapsed"
        )
    
    # Convert datetime column to local date for comparison
    df['local_start_date'] = df['start_date'].dt.date
    
    with st.sidebar.expander("Date Range", expanded=True):
        # Date Range Filter with more intuitive selection
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "From", 
                min_value=df['local_start_date'].min(), 
                max_value=df['local_start_date'].max(), 
                value=df['local_start_date'].min()
            )
        with col2:
            end_date = st.date_input(
                "To", 
                min_value=df['local_start_date'].min(), 
                max_value=df['local_start_date'].max(), 
                value=df['local_start_date'].max()
            )
    
    # Optional intensity filter
    with st.sidebar.expander("Performance Intensity", expanded=False):
        min_speed = st.slider(
            "Minimum Average Speed (km/h)", 
            float(df['average_speed_kmh'].min()), 
            float(df['average_speed_kmh'].max()), 
            float(df['average_speed_kmh'].min())
        )
    
    # Filter DataFrame
    filtered_df = df[
        (df['type'].isin(selected_types)) & 
        (df['local_start_date'].between(start_date, end_date)) &
        (df['average_speed_kmh'] >= min_speed)
    ]
    
    # Drop the temporary column
    filtered_df = filtered_df.drop(columns=['local_start_date'])
    
    return filtered_df

def main():
    # Page Configuration
    st.set_page_config(
        page_title="Strava Activity Insights", 
        page_icon="🚴", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply Styling
    apply_styling()
    
    # Dynamic Title with Greeting
    current_time = datetime.datetime.now()
    greeting = "Good Morning" if current_time.hour < 12 else "Good Afternoon" if current_time.hour < 18 else "Good Evening"
    st.markdown(f"<h1 class='stTitle'>🚲 {greeting}, Athlete!</h1>", unsafe_allow_html=True)
    
    # Fetch and process data
    try:
        # Data Fetching
        fetcher = StravaDataFetcher()
        
        # Fetch Athlete Profile
        athlete_profile = fetcher.get_athlete_profile()
        
        # Profile Display
        col1, col2 = st.columns([1, 3])
        with col1:
            # Profile Image with Enhanced Styling and Larger Size
            if athlete_profile.get('profile_image'):
                st.markdown(f"""
                <div class="profile-image-container" style="width: 250px; height: 250px;">
                    <div class="profile-image-border" style="width: 100%; height: 100%; border-radius: 50%; overflow: hidden;">
                        <img src="{athlete_profile['profile_image']}" 
                            style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.write("Profile Image Not Available")
        
        with col2:
            # Athlete Details
            st.markdown(f"## 👤 {athlete_profile['name']}")
            
            profile_col1, profile_col2 = st.columns(2)
            
            with profile_col1:
                st.metric("Username", athlete_profile.get('username', 'N/A'))
                st.metric("Followers", athlete_profile.get('total_followers', 0))
            
            with profile_col2:
                st.metric("Friends", athlete_profile.get('total_friends', 0))
        
        # Fetch and Process Activities
        activities = fetcher.get_activities()
        df = fetcher.process_activities(activities)
        df['athlete_name'] = athlete_profile['name']

        # Sidebar Filtering
        filtered_df = create_activity_filter_sidebar(df)
        
        # Summary Metrics
        create_summary_metrics(filtered_df)
        
        # Tabs
        tab1, tab2, tab3 = st.tabs([
            "🏋️ Activity Distribution", 
            "📊 Performance Overview", 
            "📝 Detailed Analysis"
        ])
        
        with tab1:
            # Activity Type Distribution
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader("Activity Type Distribution")
                type_dist = filtered_df['type'].value_counts()
                fig_type = px.pie(
                    values=type_dist.values,
                    names=type_dist.index,
                    title="Breakdown of Your Activities",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_type.update_layout(
                    title_x=0.5, 
                    height=450, 
                    margin=dict(t=50, b=0, l=0, r=0)
                )
                st.plotly_chart(fig_type, use_container_width=True)
            
            with col2:
                st.subheader("Quick Stats")
                for activity_type in type_dist.index:
                    st.metric(
                        activity_type, 
                        f"{type_dist[activity_type]} activities"
                    )
        
        with tab2:
            # Performance Overview
            st.subheader("Performance Metrics")
            col1, col2 = st.columns(2)
            
            with col1:
                # Distance and Moving Time Grouped Bar Chart
                fig_details = go.Figure(data=[
                    go.Bar(name='Distance (km)', x=filtered_df['name'], y=filtered_df['distance_km']),
                    go.Bar(name='Moving Time (min)', x=filtered_df['name'], y=filtered_df['moving_time_min'])
                ])
                fig_details.update_layout(
                    barmode='group', 
                    title="Distance vs Moving Time",
                    xaxis_title="Activity Name",
                    yaxis_title="Value"
                )
                st.plotly_chart(fig_details, use_container_width=True)
            
            with col2:
                # Elevation and Speed Scatter Plot
                fig_elevation = px.scatter(
                    filtered_df,
                    x='distance_km',
                    y='total_elevation_gain',
                    color='type',
                    size='average_speed_kmh',
                    hover_name='name',
                    title='Distance vs Elevation by Activity Type',
                    labels={
                        'distance_km': 'Distance (km)',
                        'total_elevation_gain': 'Elevation Gain',
                        'average_speed_kmh': 'Average Speed'
                    }
                )
                st.plotly_chart(fig_elevation, use_container_width=True)
        
        with tab3:
            # Detailed Data Analysis
            st.subheader("Raw Activity Data")
            st.dataframe(
                filtered_df, 
                use_container_width=True,
                column_config={
                    "name": st.column_config.TextColumn(width="medium"),
                    "distance_km": st.column_config.NumberColumn(
                        format="%.2f km"
                    ),
                    "average_speed_kmh": st.column_config.NumberColumn(
                        format="%.2f km/h"
                    ),
                    "calories": st.column_config.NumberColumn(
                        format="%d cal"
                    )
                }
            )
    
    except Exception as e:
        st.error(f"Error loading Strava data: {e}")
        st.info("Ensure you've completed the authentication process.")

if __name__ == "__main__":
    main()