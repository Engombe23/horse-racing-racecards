## Horse Racing Racecards (Streamlit)

Simple Streamlit app that fetches and displays UK/IE racecards as user‑friendly cards. Built as a practical, shareable project aligned with part‑time betting shop experience.

### Aims
- Present daily racecards for Britain and Ireland in a clean UI.
- Let users filter by day and region and quickly scan meetings.
- Show key race details and runners for each meeting.
- Demonstrate API consumption, env‑based auth, and a minimal Streamlit UI.

### Features
- Two‑column “meeting cards” with:
  - Course, region, off time, class/type, distance, going, surface
  - Field size, prize, age/rating bands
  - Runners table (No, Draw, Horse, Age, Sex, Trainer, Jockey, Headgear, OR, Lbs, Last, Form)
- Sidebar filters: Day (`today` or `tomorrow`) and Regions (`gb`, `ire`)
- Manual fetch button and auto‑refresh option

### Tech Stack
- Streamlit
- requests
- python‑dotenv

## Getting Started

### Prerequisites
- Python 3.11+ (3.12 recommended)
- A terminal/PowerShell

### Clone
```bash
git clone https://github.com/Engombe23/horse-racing-racecards.git
cd Horse-Racing-Programming
```

### Virtual environment (Windows PowerShell)
```powershell
python -m venv venv
./venv/Scripts/Activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Environment variables
Create a `.env` file in the project root with your API credentials:
```env
USER=your_api_username
PASSWORD=your_api_password
```

Never commit your `.env` to source control.

### Run the app
```bash
streamlit run main.py
```
Open the URL shown in your terminal (usually `http://localhost:8501`).

## Usage
1. Choose Day and Regions in the sidebar.
2. Click “Fetch racecards” or enable auto refresh.
3. Browse meeting cards; expand runners table as needed.

## Configuration
- API endpoint: `https://api.theracingapi.com/v1/racecards/free`
- Auth: HTTP Basic using `USER` and `PASSWORD` from `.env`

## Notes, Attribution, and Compliance
- Data provided by The Racing API (`theracingapi.com`). Check usage terms/attribution.
- This app is for informational/educational purposes only; it is not betting advice.
- If you mention a workplace, clarify that this is a personal project.

## Troubleshooting
- 401/403: Check `USER`/`PASSWORD` in `.env` or Streamlit Secrets.
- No data: The endpoint may be restricted or empty for selected filters.
- Network/timeouts: Retry; ensure internet access and that the API is reachable.

## Project Structure
```text
Horse-Racing-Programming/
├─ main.py            # Streamlit app
├─ requirements.txt   # Python dependencies
└─ README.md          # This file
```