from datetime import timedelta, datetime


def parse_duration(duration_string):
    duration_string = duration_string.replace("P", "").replace("T", "")
    components = ["D", "H", "M", "S"]
    values = {"D": 0, "H": 0, "M": 0, "S": 0}
    for component in components:
        if component in duration_string:
            value, duration_string = duration_string.split(component, 1)
            values[component] = int(value)
    return timedelta(
        days=values["D"], hours=values["H"], minutes=values["M"], seconds=values["S"]
    )


def transform_data(row):
    duration_delta = parse_duration(row["duration"])
    row["duration"] = int(duration_delta.total_seconds())
    row["video_type"] = "shorts" if duration_delta.total_seconds() <= 60 else "normal"
    return row
