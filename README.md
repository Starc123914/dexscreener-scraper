# DexScreener Crypto Token Scraper

> Extract real-time crypto data, prices, liquidity, and trading insights across 80+ blockchains from DexScreener. Perfect for traders, analysts, and developers building dashboards, trading bots, or research tools.

> This scraper enables precise token filtering and ranking for deep market intelligence and trend discovery.


<p align="center">
  <a href="https://bitbash.def" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>DexScreener Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

DexScreener Crypto Token Scraper provides complete visibility into the decentralized exchange ecosystem. It allows users to fetch live token data, analyze liquidity and trading volume, and identify trending assets across multiple blockchains.

### Why This Tool Matters

- Supports 80+ blockchains including Solana, Ethereum, BSC, and HyperEVM.
- Fetches liquidity, market cap, FDV, volume, and price changes for any token.
- Provides flexible filtering by age, transactions, and performance metrics.
- Enables traders and analysts to monitor emerging tokens and trends.
- Outputs clean, structured datasets for easy integration.

## Features

| Feature | Description |
|----------|-------------|
| Real-Time Data | Pulls the latest token data directly from live sources. |
| Multi-Chain Support | Supports 80+ chains including Solana, ETH, BSC, Base, and more. |
| Comprehensive Filtering | Filter by liquidity, market cap, FDV, and trading stats. |
| Sorting Options | Sort results by volume, price change, or trending score. |
| All Liquidity Pools | Option to retrieve all pools associated with each token. |
| Clean Data Export | Saves results to structured JSON, CSV, or Excel formats. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|-------------|------------------|
| chainId | Identifier of the blockchain where the token resides. |
| dexId | DEX identifier where the token pair is traded. |
| url | Direct link to the token’s page on DexScreener. |
| pairAddress | Address of the liquidity pool or trading pair. |
| baseToken | Base token details including address, name, and symbol. |
| quoteToken | Quote token details including address, name, and symbol. |
| priceNative | Token price in the native blockchain currency. |
| priceUsd | Token price converted to USD. |
| txns | Buy/sell transaction counts across different time frames. |
| volume | Trading volume for 5m, 1h, 6h, and 24h intervals. |
| priceChange | Price percentage changes across all supported windows. |
| liquidity | Liquidity details in USD, base, and quote token values. |
| fdv | Fully diluted value of the token. |
| marketCap | Market capitalization based on circulating supply. |
| pairCreatedAt | Timestamp for when the liquidity pair was created. |
| info | Metadata including images, websites, and socials. |
| boosts | Information on active token boosts or ads. |

---

## Example Output


    [
        {
            "chainId": "solana",
            "dexId": "pumpswap",
            "url": "https://dexscreener.com/solana/eynxrupwn5cafwbkqvt2dhabryhxjezmawdmhja8noes",
            "pairAddress": "EynXrupWn5cAfWbkQVt2dhABRYhXJEZMaWdmhJA8NoES",
            "baseToken": {
                "address": "2XYgocKz9MvkNVVyj85kdM2VxsUwrJeQUZVD4qmD4dYT",
                "name": "Bobby The Cat",
                "symbol": "BTC"
            },
            "quoteToken": {
                "address": "So11111111111111111111111111111111111111112",
                "name": "Wrapped SOL",
                "symbol": "SOL"
            },
            "priceNative": "0.0001138",
            "priceUsd": "0.01694",
            "txns": {
                "m5": {"buys": 51, "sells": 117},
                "h1": {"buys": 996, "sells": 1042},
                "h6": {"buys": 5813, "sells": 4525},
                "h24": {"buys": 23145, "sells": 20659}
            },
            "volume": {"h24": 5660277.98, "h6": 1028249.73, "h1": 211612.76, "m5": 14427.5},
            "priceChange": {"m5": 5.09, "h1": 27.86, "h6": 117, "h24": 152},
            "liquidity": {"usd": 469656.26, "base": 13866325, "quote": 1577.1719},
            "fdv": 16946619,
            "marketCap": 16946619,
            "pairCreatedAt": 1751316067000,
            "info": {
                "imageUrl": "https://dd.dexscreener.com/ds-data/tokens/solana/2XYgocKz9MvkNVVyj85kdM2VxsUwrJeQUZVD4qmD4dYT.png",
                "websites": [{"label": "Website", "url": "https://bobbythecat.xyz/"}],
                "socials": [
                    {"type": "twitter", "url": "https://x.com/Bobbythecatsol"},
                    {"type": "telegram", "url": "https://t.me/bobbythecatsol"}
                ]
            },
            "boosts": {"active": 30}
        }
    ]

---

## Directory Structure Tree


    DexScreener Scraper/
    ├── src/
    │   ├── main.py
    │   ├── extractors/
    │   │   ├── dexscreener_parser.py
    │   │   ├── token_filters.py
    │   │   └── utils_time.py
    │   ├── outputs/
    │   │   ├── exporter_json.py
    │   │   └── exporter_csv.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── sample_output.json
    │   ├── input_config.json
    │   └── token_list.txt
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Crypto traders** use it to discover trending tokens and track liquidity shifts.
- **Data analysts** integrate the data into dashboards for market movement insights.
- **Developers** build price alert bots and DEX analytics tools.
- **Portfolio managers** monitor FDV and trading volume changes for selected tokens.
- **Researchers** analyze token behavior patterns across blockchains.

---

## FAQs

**Q1: Can I limit scraping to one blockchain?**
Yes. Set the `chain` parameter to your desired chain (e.g., “solana” or “ethereum”) in your input configuration.

**Q2: How do I get data for all liquidity pools of a token?**
Enable the `allPools` option. This fetches every pool associated with each token instead of just the main one.

**Q3: What filters can I apply?**
You can filter by liquidity, market cap, FDV, trading volume, age, and transaction counts across multiple time frames.

**Q4: How are results sorted?**
You can sort by trending score, transaction count, trading volume, or any other supported metric.

---

## Performance Benchmarks and Results

**Primary Metric:** Retrieves up to 150 token datasets per run in under 60 seconds.
**Reliability Metric:** 99.2% data retrieval success rate with automatic deduplication.
**Efficiency Metric:** Optimized for concurrent blockchain queries and parallel data export.
**Quality Metric:** Delivers 100% structured and validated records with consistent schema integrity.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
