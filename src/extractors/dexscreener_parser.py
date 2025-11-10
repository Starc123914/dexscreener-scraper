import logging
from typing import Any, Dict, Iterable, List, Optional, Set
import time
import requests

DEX_API_BASE = "https://api.dexscreener.com/latest/dex"

def _http_get_json(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()

def fetch_pairs_for_query(query: str, chains: Optional[List[str]] = None, all_pools: bool = False) -> List[Dict[str, Any]]:
    """
    Use DexScreener search endpoint. Returns 'pairs' list.
    """
    url = f"{DEX_API_BASE}/search"
    params = {"q": query}
    data = _http_get_json(url, params=params)
    pairs = data.get("pairs", []) or []

    if chains:
        chains_set = {c.lower() for c in chains}
        pairs = [p for p in pairs if str(p.get("chainId", "")).lower() in chains_set]

    if not all_pools:
        # keep best pool per baseToken address (heuristic by liquidityUsd)
        pairs = _best_pool_per_token(pairs)

    return pairs

def fetch_pairs_for_token_addresses(token_addresses: List[str], all_pools: bool = False) -> List[Dict[str, Any]]:
    """
    Use DexScreener tokens endpoint. Returns 'pairs' for each token address.
    """
    results: List[Dict[str, Any]] = []
    # Chunk token addresses to avoid very long URLs. DexScreener supports comma-separated.
    chunk_size = 20
    for i in range(0, len(token_addresses), chunk_size):
        chunk = ",".join(token_addresses[i : i + chunk_size])
        url = f"{DEX_API_BASE}/tokens/{chunk}"
        try:
            data = _http_get_json(url)
            pairs = data.get("pairs", []) or []
            if not all_pools:
                pairs = _best_pool_per_token(pairs)
            results.extend(pairs)
            # be gentle
            time.sleep(0.2)
        except Exception as e:
            logging.warning("Fetch token chunk failed: %s", e)
    return results

def _best_pool_per_token(pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    best_by_token: Dict[str, Dict[str, Any]] = {}
    for p in pairs:
        base = (p.get("baseToken") or {}).get("address") or ""
        # prefer higher liquidityUsd
        liq = float((p.get("liquidity") or {}).get("usd") or 0.0)
        existing = best_by_token.get(base)
        if not existing or float((existing.get("liquidity") or {}).get("usd") or 0.0) < liq:
            best_by_token[base] = p
    return list(best_by_token.values())

def _to_float(val: Any) -> Optional[float]:
    try:
        if val is None:
            return None
        return float(val)
    except Exception:
        return None

def normalize_pairs(pairs: Iterable[Dict[str, Any]], dedupe: bool = True) -> List[Dict[str, Any]]:
    """
    Map DexScreener pair shape into our normalized schema.
    """
    out: List[Dict[str, Any]] = []
    seen: Set[str] = set()

    for p in pairs:
        pair_address = str(p.get("pairAddress") or p.get("pair_address") or "").strip()
        if dedupe and pair_address and pair_address in seen:
            continue
        if pair_address:
            seen.add(pair_address)

        base_token = p.get("baseToken") or {}
        quote_token = p.get("quoteToken") or {}
        txns = p.get("txns") or {}
        volume = p.get("volume") or {}
        price_change = p.get("priceChange") or {}
        liquidity = p.get("liquidity") or {}
        info = p.get("info") or {}
        boosts = p.get("boosts") or {}

        item = {
            "chainId": p.get("chainId"),
            "dexId": p.get("dexId"),
            "url": p.get("url"),
            "pairAddress": pair_address,
            "baseToken": {
                "address": base_token.get("address"),
                "name": base_token.get("name"),
                "symbol": base_token.get("symbol"),
            },
            "quoteToken": {
                "address": quote_token.get("address"),
                "name": quote_token.get("name"),
                "symbol": quote_token.get("symbol"),
            },
            "priceNative": p.get("priceNative"),
            "priceUsd": p.get("priceUsd"),
            "txns": {
                "m5": (txns.get("m5") or {"buys": 0, "sells": 0}),
                "h1": (txns.get("h1") or {"buys": 0, "sells": 0}),
                "h6": (txns.get("h6") or {"buys": 0, "sells": 0}),
                "h24": (txns.get("h24") or {"buys": 0, "sells": 0}),
            },
            "volume": {
                "m5": _to_float(volume.get("m5")),
                "h1": _to_float(volume.get("h1")),
                "h6": _to_float(volume.get("h6")),
                "h24": _to_float(volume.get("h24")),
            },
            "priceChange": {
                "m5": _to_float(price_change.get("m5")),
                "h1": _to_float(price_change.get("h1")),
                "h6": _to_float(price_change.get("h6")),
                "h24": _to_float(price_change.get("h24")),
            },
            "liquidity": {
                "usd": _to_float(liquidity.get("usd")),
                "base": _to_float(liquidity.get("base")),
                "quote": _to_float(liquidity.get("quote")),
            },
            "fdv": _to_float(p.get("fdv")),
            "marketCap": _to_float(p.get("marketCap")),
            "pairCreatedAt": p.get("pairCreatedAt"),
            "info": {
                "imageUrl": info.get("imageUrl"),
                "websites": info.get("websites") or [],
                "socials": info.get("socials") or [],
            },
            "boosts": {"active": boosts.get("active")},
            # convenience fields for sorting
            "_trendingScore": _to_float(p.get("trendScore") or p.get("trendingScore")),
        }
        out.append(item)
    return out