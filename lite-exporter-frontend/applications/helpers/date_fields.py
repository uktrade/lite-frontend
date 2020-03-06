def format_date(data, date_field):
    year = data.get(date_field + "year", "")
    month = data.get(date_field + "month", "")
    if len(month) == 1:
        month = "0" + month
    day = data.get(date_field + "day", "")
    if len(day) == 1:
        day = "0" + day
    return f"{year}-{month}-{day}"


def format_date_fields(data):
    # Convert date
    date_fields = ["first_exhibition_date", "required_by_date"]
    for date_field in date_fields:
        data[date_field] = format_date(data, date_field)
    return data
