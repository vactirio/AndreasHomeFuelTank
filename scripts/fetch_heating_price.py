"""Append today's heating oil price (delivered, 7-day mean) for one nomarchy to heating_oil_prices.json."""
import html, json, os, re, sys, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

URL    = "https://www.fuelprices.gr/price_stats_ng.view?prodclass=7&nofdays=7&order_by=9"
REGION = os.environ.get("REGION", "ΝΟΜΑΡΧΙΑ ΑΝΑΤΟΛΙΚΗΣ ΑΤΤΙΚΗΣ")
FILE   = "heating_oil_prices.json"

req  = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (heating-price bot)"})
raw  = urllib.request.urlopen(req, timeout=60).read().decode("windows-1253", errors="replace")
text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))

# row: <region> <stations> <min> <mean> <max>
m = re.search(re.escape(REGION) + r" (\d+) ([\d,]+) ([\d,]+) ([\d,]+)", text)
if not m:
    sys.exit(f"Region not found (off-season?): {REGION}")

price = float(m.group(3).replace(",", "."))
today = datetime.now(ZoneInfo("Europe/Athens")).strftime("%Y-%m-%d")

data = json.load(open(FILE, encoding="utf-8")) if os.path.exists(FILE) else {}
data[today] = price
json.dump(dict(sorted(data.items())), open(FILE, "w", encoding="utf-8"), indent=2)
print(f"{today}: {price} €/L ({REGION})")
