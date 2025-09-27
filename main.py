import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

API_URL = "https://api.theracingapi.com/v1/racecards/free"

def fetch_racecards(day: str, regions: list[str]):
  params = {
    "day": day,
    "region_codes": regions
  }
  username = os.getenv("USER")
  password = os.getenv("PASSWORD")
  if not username or not password:
    raise ValueError("Missing USER or PASSWORD in environment variables. Create a .env with USER and PASSWORD.")
  response = requests.request(
    "GET",
    API_URL,
    auth=HTTPBasicAuth(f"{username}", f"{password}"),
    params=params,
    timeout=20,
  )
  response.raise_for_status()
  return response.json()

st.set_page_config(page_title="Racecards (GB & IRE)", page_icon="🏇", layout="wide")
st.title("🏇 Racecards: Britain & Ireland")

with st.sidebar:
  st.header("Filters")
  day = st.selectbox("Day", options=["today", "tomorrow"], index=0)
  regions = st.multiselect("Regions", options=["gb", "ire"], default=["gb", "ire"])
  auto_refresh = st.toggle("Auto refresh on change", value=True)

placeholder = st.empty()

def _get(d: dict, path: str, default=""):
  cur = d
  for key in path.split("."):
    if isinstance(cur, dict) and key in cur:
      cur = cur[key]
    else:
      return default
  return cur

def render_results(data):
  if not data:
    st.info("No results returned.")
    return
  # Try to present common shapes, fallback to raw JSON
  if isinstance(data, dict) and "racecards" in data and isinstance(data["racecards"], list):
    racecards = data["racecards"]
    st.subheader(f"Results: {len(racecards)} meetings")
    cols = st.columns(2)
    for i, card in enumerate(racecards):
      course_name = card.get("course", "Unknown course")
      region = card.get("region", "")
      start_time = card.get("off_time") or card.get("off_dt") or ""
      going = card.get("going", "")
      race_name = card.get("race_name", "")
      race_class = card.get("race_class", "")
      race_type = card.get("type", "")
      field_size = card.get("field_size", "")
      prize = card.get("prize", "")
      distance_f = card.get("distance_f", "")
      surface = card.get("surface", "")
      age_band = card.get("age_band", "")
      rating_band = card.get("rating_band", "")

      with cols[i % 2].container():
        st.markdown(f"**{course_name}**  {f'`{region}`' if region else ''}")
        if race_name:
          st.write(race_name)
        meta_bits_top = []
        if start_time:
          meta_bits_top.append(f"Off: {start_time}")
        if field_size:
          meta_bits_top.append(f"Field: {field_size}")
        if prize:
          meta_bits_top.append(f"Prize: {prize}")
        if meta_bits_top:
          st.caption(" • ".join(meta_bits_top))

        meta_bits_bottom = []
        if race_class:
          meta_bits_bottom.append(race_class)
        if race_type:
          meta_bits_bottom.append(race_type)
        if distance_f:
          meta_bits_bottom.append(f"{distance_f}f")
        if going:
          meta_bits_bottom.append(f"Going: {going}")
        if surface:
          meta_bits_bottom.append(surface)
        if age_band:
          meta_bits_bottom.append(age_band)
        if rating_band:
          meta_bits_bottom.append(rating_band)
        if meta_bits_bottom:
          st.caption(" • ".join(meta_bits_bottom))

        # Runners table
        runners = card.get("runners", [])
        if isinstance(runners, list) and runners:
          rows = []
          for r in runners:
            if not isinstance(r, dict):
              continue
            rows.append({
              "No": r.get("number", ""),
              "Draw": r.get("draw", ""),
              "Horse": r.get("horse", ""),
              "Age": r.get("age", ""),
              "Sex": r.get("sex_code", r.get("sex", "")),
              "Trainer": r.get("trainer", ""),
              "Jockey": r.get("jockey", ""),
              "Headgear": r.get("headgear", ""),
              "OR": r.get("ofr", ""),
              "Lbs": r.get("lbs", ""),
              "Last": r.get("last_run", ""),
              "Form": r.get("form", ""),
            })
          if rows:
            df = st.dataframe(
              rows,
              use_container_width=True,
              hide_index=True
            )
  else:
    st.json(data)

def run_fetch_and_render():
  with placeholder.container():
    with st.spinner("Fetching racecards..."):
      try:
        data = fetch_racecards(day=day, regions=regions)
        st.success("Fetched successfully")
        render_results(data)
      except requests.HTTPError as http_err:
        st.error(f"HTTP error: {http_err}")
        try:
          st.json(http_err.response.json())
        except Exception:
          st.write(http_err.response.text if getattr(http_err, "response", None) else "")
      except ValueError as ve:
        st.warning(str(ve))
      except requests.RequestException as re:
        st.error(f"Network error: {re}")
      except Exception as e:
        st.error(f"Unexpected error: {e}")

col1, col2 = st.columns([1, 3])
with col1:
  fetch_clicked = st.button("Fetch racecards", type="primary")
with col2:
  st.caption("Tip: Use the sidebar to adjust day/regions.")

if auto_refresh or fetch_clicked:
  run_fetch_and_render()