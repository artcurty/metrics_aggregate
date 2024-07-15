from datetime import datetime, timedelta

def to_iso_utc(date_str: str, is_end_date: bool = False) -> str:
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    if is_end_date:
        dt += timedelta(hours=23, minutes=59, seconds=59)
    return dt.isoformat()