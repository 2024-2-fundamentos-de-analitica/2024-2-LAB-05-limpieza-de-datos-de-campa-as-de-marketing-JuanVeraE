import pandas as pd

campaign = pd.read_csv("files/output/campaign.csv")

for name in (
        "client_id,number_contacts,contact_duration,"
        "previous_campaign_contacts,previous_outcome,"
        "campaign_outcome,last_contact_date".split(",")
    ):
    if name in campaign.columns:
        print(f"{name} exists")
    else:
        print(campaign.columns)