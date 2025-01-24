"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerles un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months
    """

    import os
    import pandas as pd
    import zipfile

    # Crear carpeta de salida si no existe
    output_folder = "files/output"
    os.makedirs(output_folder, exist_ok=True)

    # Ruta de entrada
    input_zip_folder = "files/input"

    # Crear un DataFrame principal que consolide todos los datos
    all_data = pd.DataFrame()

    # Procesar cada archivo zip en la carpeta de entrada
    for zip_filename in os.listdir(input_zip_folder):
        if zip_filename.endswith(".zip"):
            zip_path = os.path.join(input_zip_folder, zip_filename)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_name in zip_ref.namelist():
                    if file_name.endswith(".csv"):
                        with zip_ref.open(file_name) as csv_file:
                            # Leer el CSV desde el archivo comprimido y concatenarlo con el DataFrame principal
                            data = pd.read_csv(csv_file)
                            all_data = pd.concat([all_data, data], ignore_index=True)

    # Procesar client.csv
    client_df = all_data[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()
    client_df["job"] = client_df["job"].str.replace(".", "", regex=False).str.replace("-", "_")
    client_df["education"] = client_df["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    client_df["credit_default"] = client_df["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    client_df["mortgage"] = client_df["mortgage"].apply(lambda x: 1 if x == "yes" else 0)
    client_csv_path = os.path.join(output_folder, "client.csv")
    client_df.to_csv(client_csv_path, index=False)

    # Procesar campaign.csv
    campaign_df = all_data[[
        "client_id", 
        "number_contacts", 
        "contact_duration", 
        "previous_campaign_contacts", 
        "previous_outcome", 
        "campaign_outcome", 
        "day", 
        "month"
    ]].copy()
    campaign_df["previous_outcome"] = campaign_df["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    campaign_df["campaign_outcome"] = campaign_df["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)
    campaign_df["last_contact_date"] = pd.to_datetime(
        campaign_df["day"].astype(str) + "-" + campaign_df["month"] + "-2022", 
        format="%d-%b-%Y"
    ).dt.strftime("%Y-%m-%d")
    campaign_df = campaign_df.drop(columns=["day", "month"], inplace=False)
    campaign_csv_path = os.path.join(output_folder, "campaign.csv")
    campaign_df.to_csv(campaign_csv_path, index=False)

    # Procesar economics.csv
    economics_df = all_data[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    economics_csv_path = os.path.join(output_folder, "economics.csv")
    economics_df.to_csv(economics_csv_path, index=False)

    print("Archivos 'client.csv', 'campaign.csv' y 'economics.csv' generados en la carpeta 'files/output'.")

    return


if __name__ == "__main__":
    clean_campaign_data()
