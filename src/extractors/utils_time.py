from typing import Optional
import time

def pair_age_hours(timestamp_ms: Optional[int]) -> Optional[float]:
    """
    Given a millisecond timestamp, return hours since then.
    """
    if not timestamp_ms:
        return None
    try:
        now_ms = int(time.time() * 1000)
        delta_ms = max(0, now_ms - int(timestamp_ms))