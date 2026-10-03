# Member 5 Team Handoff

## Give these files to the teammate integrating the main application

**Main integration file**
- `admin_dashboard.py`

**Supporting demo data**
- `data/recipients.json`
- `data/demo_result.json`
- `data/fallbacks.json`

## Important

Do not run `admin_dashboard.py` as a second final application. It was created and tested as a standalone Member 5 verification app.

For the final team application, the teammate responsible for the main Streamlit app should integrate the dashboard UI/logic into the existing `app.py` and connect it to the workflow's final result.

The dashboard record should contain:
- Donation ID
- Donor
- Food
- Quantity
- Unit
- Recipient
- Match Score
- Status
- Pickup
- Delivery Target
- Priority

Example:
```python
{
    "Donation ID": "D-001",
    "Donor": "ABC Restaurant",
    "Food": "Biryani",
    "Quantity": 50,
    "Unit": "portions",
    "Recipient": "Hope Community Center (DEMO)",
    "Match Score": 96,
    "Status": "Confirmed (demo)",
    "Pickup": "18:30",
    "Delivery Target": "19:00",
    "Priority": "High"
}
```

Member 5 has already independently tested this dashboard in Google Colab.

After integration, Member 5 should test the final dashboard again during the team demo.
