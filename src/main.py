import argparse
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

# Allow running this file directly without installing the package
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from extractors.dexscreener_parser import (
    fetch_pairs_for_query,
    fetch_pairs_for_token_addresses,
    normalize_pairs,
)
from extractors.token_filters import apply_filters, sort_items
from outputs.exporter_json import export_json
from outputs.exporter_csv import export_csv

def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_lines(path: str) -> List[str]:
    if not path or not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="DexScreener Crypto Token Scraper - fetch, filter, and export DEX pair data."
    )
    p.add_argument(
        "--config",
        default=os.path.join(PROJECT_ROOT, "data", "input_config.json"),
        help="Path to configuration JSON file.",
    )
    p.add_argument(
        "--output",
        default=None,
        help="Override output path (file). If omitted uses config's outputPath.",
    )
    p.add_argument(
        "--format",
        choices=["json", "csv"],
        default=None,
        help="Override output format.",
    )
    p.add_argument(
        "--all-pools",
        action="store_true",
        help="If set, include all pools, not only the top one per token.",
    )
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity.",
    )
    return p

def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

def main() -> None:
    args = build_arg_parser().parse_args()
    setup_logging(args.log_level)

    cfg = load_json(args.config)
    output_format = (args.format or cfg.get("outputFormat") or "json").lower()
    output_path = args.output or cfg.get("outputPath") or os.path.join(PROJECT_ROOT, "data", f"output.{output_format}")
    all_pools = args.all_pools or bool(cfg.get("allPools", False))

    # Inputs
    chains: Optional[List[str]] = cfg.get("chains") or None
    query: Optional[str] = cfg.get("query") or None
    token_file: Optional[str] = cfg.get("tokenAddressesFile")
    if token_file and not os.path.isabs(token_file):
        token_file = os.path.join(PROJECT_ROOT, token_file)
    token_addresses = load_lines(token_file) if token_file else []

    # Fetch
    raw_pairs: List[Dict[str, Any]] = []

    try:
        if query:
            logging.info("Fetching pairs by search query: %s", query)
            raw_pairs.extend(fetch_pairs_for_query(query=query, chains=chains, all_pools=all_pools))
    except Exception as e:
        logging.warning("Search query fetch failed: %s", e)

    try:
        if token_addresses:
            logging.info("Fetching pairs by token addresses (%d)", len(token_addresses))
            raw_pairs.extend(
                fetch_pairs_for_token_addresses(token_addresses=token_addresses, all_pools=all_pools)
            )
    except Exception as e:
        logging.warning("Token address fetch failed: %s", e)

    # If nothing came back, try loading sample data to keep flow runnable.
    if not raw_pairs:
        sample_path = os.path.join(PROJECT_ROOT, "data", "sample_output.json")
        if os.path.exists(sample_path):
            logging.warning("No live data fetched; falling back to sample_output.json")
            sample = load_json(sample_path)
            if isinstance(sample, dict) and "data" in sample:
                raw_pairs = sample["data"]
            elif isinstance(sample, list):
                raw_pairs = sample
        else:
            logging.error("No data fetched and sample_output.json not found. Exiting.")
            sys.exit(1)

    # Normalize, de-duplicate
    logging.info("Normalizing %d raw pairs", len(raw_pairs))
    items = normalize_pairs(raw_pairs, dedupe=True)

    # Filtering
    filters = cfg.get("filters", {})
    limit = int(cfg.get("limit", 150))
    sort_by = cfg.get("sortBy", "volumeH24")

    logging.info("Applying filters: %s", json.dumps(filters))
    items = apply_filters(items, filters)

    logging.info("Sorting by %s", sort_by)
    items = sort_items(items, sort_by=sort_by)

    if limit and limit > 0:
        items = items[:limit]

    # Ensure output dir exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Export
    if output_format == "json":
        export_json(items, output_path)
    elif output_format == "csv":
        export_csv(items, output_path)
    else:
        logging.error("Unsupported format: %s", output_format)
        sys.exit(2)

    logging.info("Done. Wrote %d records to %s", len(items), output_path)

if __name__ == "__main__":
    main()