# @title
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse, parse_qsl, urlencode
import json

INPUT_FILE = "satu.txt"
OUTPUT_FILE = "get_params.txt"
CONCURRENCY = 30

results = set()
lock = asyncio.Lock()


# 🔧 normalize URL
def normalize_url(url):
    if not url.startswith("http"):
        return "https://" + url
    return url


# 🔥 ambil domain utama dari satu.txt
def get_allowed_domains():
    domains = set()

    with open(INPUT_FILE, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            line = normalize_url(line)

            parsed = urlparse(line)
            host = parsed.hostname or ""

            if host.startswith("www."):
                host = host[4:]

            domains.add(host)

    return domains


ALLOWED_DOMAINS = get_allowed_domains()


# 🔒 hanya domain utama / subdomain
def is_same_or_subdomain(hostname):
    if not hostname:
        return False

    hostname = hostname.lower()

    if hostname.startswith("www."):
        hostname = hostname[4:]

    for domain in ALLOWED_DOMAINS:
        if hostname == domain:
            return True

        if hostname.endswith("." + domain):
            return True

    return False


# 🔁 safe navigation
async def safe_goto(page, url):
    try:
        await page.goto(url, timeout=15000)
        return True

    except:
        if url.startswith("https://"):
            try:
                fallback = url.replace("https://", "http://")
                await page.goto(fallback, timeout=15000)
                return True
            except:
                return False

        return False


# 🔥 trigger action
async def trigger_actions(page):
    try:

        # isi input
        await page.evaluate("""
            () => {
                document.querySelectorAll('input, textarea').forEach(el => {
                    el.value = "test";
                    el.dispatchEvent(new Event('input'));
                    el.dispatchEvent(new Event('change'));
                });
            }
        """)

        # submit form
        forms = await page.query_selector_all("form")

        for form in forms:
            try:
                await form.evaluate("form => form.submit()")
            except:
                pass

        # klik button
        buttons = await page.query_selector_all("button")

        for btn in buttons[:10]:
            try:
                await btn.click(timeout=2000)
            except:
                pass

        # klik link
        links = await page.query_selector_all("a")

        for link in links[:5]:
            try:
                await link.click(timeout=2000)
            except:
                pass

        # manual GET trigger
        await page.evaluate("""
            fetch('/api/test?test=1')
                .catch(()=>{})
        """)

        await page.wait_for_timeout(5000)

    except:
        pass


# 🎯 worker
async def worker(context, url):
    page = await context.new_page()

    url = normalize_url(url)

    ok = await safe_goto(page, url)

    if not ok:
        await page.close()
        return

    await trigger_actions(page)

    await page.close()


def is_valid_url(url):
    blacklist = [
        "cdn-cgi",
        "challenge-platform",
        "cloudflare",
    ]

    return not any(x in url for x in blacklist)


# 🔍 extract GET params
def extract_get_params(url):
    parsed = urlparse(url)

    params = {}

    for k, v in parse_qsl(parsed.query):
        params[k] = ""

    if not params:
        return None

    base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    return base + "?" + urlencode(params)


async def main():
    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )

        context = await browser.new_context()

        # 🎯 intercept GET request
        async def handle_request(request):

            if request.method != "GET":
                return

            parsed = urlparse(request.url)
            hostname = parsed.hostname or ""

            # 🔒 filter domain target
            if not is_same_or_subdomain(hostname):
                return

            clean_url = extract_get_params(request.url)

            if not clean_url:
                return

            if not is_valid_url(clean_url):
                return

            async with lock:

                if clean_url not in results:
                    results.add(clean_url)

                    # print(clean_url)

                    with open(OUTPUT_FILE, "a") as f:
                        f.write(clean_url + "\n")

        context.on("request", handle_request)

        # 📥 load target
        with open(INPUT_FILE, "r") as f:
            urls = [line.strip() for line in f if line.strip()]

        sem = asyncio.Semaphore(CONCURRENCY)

        async def sem_worker(url):
            async with sem:
                await worker(context, url)

        await asyncio.gather(*[
            sem_worker(u) for u in urls
        ])

        await browser.close()


await main()
