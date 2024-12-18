# Strava Activity Dashboard

## Project Overview
A comprehensive Streamlit dashboard for analyzing Strava activities, providing detailed insights into athletic performance.

## Prerequisites
- Python 3.8+
- Strava Developer Account
- Strava API Credentials

## Project Structure
```
strava-dashboard/
│
├── .env                    # Environment variables for Strava API credentials
├── requirements.txt        # Project dependencies
│
├── src/
│   ├── auth_script.py      # Strava OAuth Authentication
│   ├── strava_data.py      # Data fetching and processing
│   └── dash.py             # Streamlit dashboard
│
└── README.md               # Project documentation
```

## Setup Instructions

### 1. Create Strava Developer Application
1. Go to [Strava Developers](https://developers.strava.com/)
2. Create a new application
3. Note down:
   - Client ID
   - Client Secret
   - Redirect URI (e.g., `http://localhost:8000/`)

### 2. Project Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/strava-dashboard.git
cd strava-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the project root:
```
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
STRAVA_REDIRECT_URI=http://localhost:8000/
```

### 4. Authentication
```bash
# Run authentication script
python -m src/auth_script
```
- A browser window will open for Strava authorization
- After authorizing, copy the entire redirect URL
- Paste the URL when prompted
- Tokens will be saved in `strava_tokens.json`

### 5. Run Dashboard
```bash
streamlit run src/dash.py
```

## Code Optimization Highlights

### 1. `auth_script.py`
- Robust token exchange mechanism
- Secure environment variable management
- User-friendly authentication flow

### 2. `strava_data.py`
- Comprehensive error handling
- Automatic token refresh
- Efficient data processing

### 3. `dash.py`
- Advanced Streamlit styling
- Dynamic filtering
- Interactive visualizations

## Key Features
- OAuth 2.0 Authentication
- Activity data retrieval
- Interactive dashboard
- Detailed performance metrics
- Customizable visualizations

## Security Considerations
- Uses environment variables for credentials
- Secure token management
- No hardcoded sensitive information

## Troubleshooting
- Ensure `.env` file is correctly configured
- Verify Strava API credentials
- Check internet connectivity
- Refresh tokens if authentication fails

## Demo
[Video Link](https://drive.google.com/drive/folders/1X5WYdwM8eMpHmY8Hb8lg_AhJBeTwCIRf?usp=sharing)

---

**Note:** This project is for personal use and learning. Respect Strava's API terms of service.
