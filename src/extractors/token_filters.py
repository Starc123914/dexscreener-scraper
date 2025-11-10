from typing import Any, Dict, List
from .utils_time import pair_age_hours

def _get_num(d: Dict[str, Any], *path, default=None):
    cur = d
    for k in path:
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            return default
    try:
        return float(cur) if cur is not None else default
    except Exception:
        return default

def apply_filters(items: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not items:
        return []

    min_liq = float(filters.get("minLiquidityUsd", 0) or 0)
    min_vol_h24 = float(filters.get("minVolumeH24", 0) or 0)
    min_fdv = float(filters.get("minFdV", 0) or 0)
    min_mcap = float(filters.get("minMarketCap", 0) or 0)
    min_txns_h24 = float(filters.get("minTxnsH24", 0) or 0)
    max_age_hours = filters.get("maxAgeHours", None)

    out: List[Dict[str, Any]] = []
    for it in items:
        liq = _get_num(it, "liquidity", "usd", default=0)
        vol24 = _get_num(it, "volume", "h24", default=0)
        fdv = _get_num(it, "fdv", default=0)
        mcap = _get_num(it, "marketCap", default=0)
        tx_h24 = _get_num(it, "txns", "h24", "buys", default=0) + _get_num(it, "txns", "h24", "sells", default=0)

        if liq < min_liq:
            continue
        if vol24 < min_vol_h24:
            continue
        if fdv < min_fdv:
            continue
        if mcap < min_mcap:
            continue
        if tx_h24 < min_txns_h24:
            continue
        if max_age_hours is not None:
            age = pair_age_hours(it.get("pairCreatedAt"))
            if age is not None and age > float(max_age_hours):
                continue

        out.append(it)

    return out

def sort_items(items: List[Dict[str, Any]], sort_by: str = "volumeH24") -> List[Dict[str, Any]]:
    key = sort_by.lower()
    if key == "volumeh24":
        return sorted(items, key=lambda x: _get_num(x, "volume", "h24", default=0.0), reverse=True)
    if key == "txnsh24":
        return sorted(
            items,
            key=lambda x: (_get_num(x, "txns", "h24", "buys", default=0.0) + _get_num(x, "txns", "h24", "sells", default=0.0)),
            reverse=True,
        )
    if key == "trending" or key == "trendingscore":
        return sorted(items, key=lambda x: _get_num(x, "_trendingScore", default=0.0), reverse=True)
    if key == "liquidity":
        return sorted(items, key=lambda x: _get_num(x, "liquidity", "usd", default=0.0), reverse=True)
    if key == "pricechangeh24":
        return sorted(items, key=lambda x: _get_num(x, "priceChange", "h24", default=0.0), reverse=True)
    # default
    return items