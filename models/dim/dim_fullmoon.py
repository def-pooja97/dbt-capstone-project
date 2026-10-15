import holidays

def is_holiday(date_val):
    german_holidays = holidays.Germany()
    return date_val in german_holidays

def model(dbt, session):
    dbt.config(
        materialized = "table",
        packages = ["holidays"]
    )

    # Get the input Snowpark DataFrame
    orders_df = dbt.ref("seed_full_moon_dates")

    # Collect rows into Python memory as dictionaries
    rows = orders_df.collect()
    
    data = []
    for row in rows:
        row_dict = row.as_dict()
        # Calculate IS_HOLIDAY column
        row_dict["IS_HOLIDAY"] = is_holiday(row_dict["FULL_MOON_DATE"])
        data.append(row_dict)

    # Pass the Python list of dicts directly to session.create_dataframe
    return session.create_dataframe(data)