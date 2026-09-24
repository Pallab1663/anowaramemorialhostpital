import os
from datetime import datetime
from zoneinfo import ZoneInfo

def today_iso(tz: str | None = None) -> str:
    zone = tz or os.environ.get("APP_TZ", "Asia/Dhaka")
    return datetime.now(ZoneInfo(zone)).strftime("%Y-%m-%d")
