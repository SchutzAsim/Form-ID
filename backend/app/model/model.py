def home_Entity(item) -> dict:
    return {
        "id": str(item["id"]),
        "Name": item["Name"],
        "Contact": item["Contact"],
        "Service": item["Service"],
        "Service_Type": item["Service_Type"],
        "Govt_Fee": item["Govt_Fee"],
        "Service_Charge": item["Service_Charge"],
        "Total_Amount": item["Total_Amount"],
        "Month": item["Month"],
        "Application_ID": item["Application_ID"],
        "Due": item["Due"]
    }


def home_Entitys(items) -> list:
    return [home_Entity(item) for item in items]