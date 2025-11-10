import csv
from typing import Any, Dict, Iterable, List, Set

def _flatten_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flatten nested fields to a CSV-friendly row.
    """
    base = rec.copy()
    # baseToken
    bt = base.pop("baseToken", {}) or {}
    qt = base.pop("quoteToken", {}) or {}
    tx = base.pop("txns", {}) or {}
    vol = base.pop("volume", {}) or {}
    chg = base.pop("priceChange", {}) or {}
    liq = base.pop("liquidity", {}) or {}
    info = base.pop("info", {}) or {}
    boosts = base.pop("boosts", {}) or {}

    flat = {
        **base,
        "baseToken.address": bt.get("address"),
        "baseToken.name": bt.get("name"),
        "baseToken.symbol": bt.get("symbol"),
        "quoteToken.address": qt.get("address"),
        "quoteToken.name": qt.get("name"),
        "quoteToken.symbol": qt.get("symbol"),
        "txns.m5.buys": (tx.get("m5") or {}).get("buys"),
        "txns.m5.sells": (tx.get("m5") or {}).get("sells"),
        "txns.h1.buys": (tx.get("h1") or {}).get("buys"),
        "txns.h1.sells": (tx.get("h1") or {}).get("sells"),
        "txns.h6.buys": (tx.get("h6") or {}).get("buys"),
        "txns.h6.sells": (tx.get("h6") or {}).get("sells"),
        "txns.h24.buys": (tx.get("h24") or {}).get("buys"),
        "txns.h24.sells": (tx.get("h24") or {}).get("sells"),
        "volume.m5": vol.get("m5"),
        "volume.h1": vol.get("h1"),
        "volume.h6": vol.get("h6"),
        "volume.h24": vol.get("h24"),
        "priceChange.m5": chg.get("m5"),
        "priceChange.h1": chg.get("h1"),
        "priceChange.h6": chg.get("h6"),
        "priceChange.h24": chg.get("h24"),
        "liquidity.usd": liq.get("usd"),
        "liquidity.base": liq.get("base"),
        "liquidity.quote": liq.get("quote"),
        "info.imageUrl": info.get("imageUrl"),
        "info.websites": ";".join([w.get("url") for w in (info.get("websites") or []) if w.get("url")]),
        "info.socials": ";".join([s.get("url") for s in (info.get("socials") or []) if s.get("url")]),
        "boosts.active": boosts.get("active"),
    }
    return flat

def export_csv(items: List[Dict[str, Any]], path: str) -> None:
    rows = [_flatten_record(it) for it in items]
    # gather all headers to avoid missing columns
    headers: Set[str] = set()
    for r in rows:
        headers.update(r.keys())
    headers_list = sorted(headers)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers_list)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)