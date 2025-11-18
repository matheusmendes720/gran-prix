import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.investing.com/",
    "Origin": "https://www.investing.com",
    "domain-id": "www",
    "Accept": "application/json",
    "Sec-Ch-Ua": '"Chromium";v="130", "Not?A_Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "en-US,en;q=0.9",
}
url = "https://api.investing.com/api/financialdata/historical/940793"
params = {
    "start-date": "2021-01-01",
    "end-date": "2025-11-10",
    "time-frame": "Daily",
    "add-missing-rows": "false",
}
resp = requests.get(url, headers=headers, params=params, timeout=30)
print(resp.status_code)
print(resp.text[:200])

