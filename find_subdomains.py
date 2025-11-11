import argparse
import asyncio
import sys
import csv
import random
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import aiohttp
from aiohttp import ClientError, ClientResponseError, ClientTimeout


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat()

def parse_retry_after(value: str):
    """Return seconds to wait from a Retry-After header (int seconds or HTTP-date)."""
    if not value:
        return None
    value = value.strip()
    # seconds
    if value.isdigit():
        return int(value)
    # HTTP-date
    try:
        dt = parsedate_to_datetime(value)
        # convert to utc timestamp diff
        delta = (dt - datetime.now(dt.tzinfo)).total_seconds()
        return max(0, int(delta))
    except Exception:
        return None

async def fetch_one(sub, domain, session, sem, csv_lock, writer, min_delay, max_retries, http_fallback, user_agent, timeout):
    full = f"{sub}.{domain}"
    url_template = "https://{}"
    errors = None
    tries = 0

    async with sem:
            while True:
                    tries += 1
                    url = url_template.format(full)
                    try:
                            # Try HEAD first (lightweight)
                            async with session.head(url, timeout=timeout, allow_redirects=True) as resp:
                                    status = resp.status
                                    headers = resp.headers
                            # If server doesn't respond to HEAD it may return a 405 Method Not Allowed
                            if status == 405:
                                    # fallback to GET
                                    async with session.get(url, timeout=timeout, allow_redirects=True) as resp:
                                            status = resp.status
                                            headers = resp.headers

                    except (ClientResponseError,) as cre:
                            status = getattr(cre, 'status', 0) or 0
                            headers = getattr(cre, 'headers', {})
                            errors = str(cre)
                    except asyncio.TimeoutError:
                            status = 0
                            headers = {}
                            errors = "Timeout"
                    except ClientError as e:
                            # Network level error (e.g. connection rejected, host not found)
                            status = 0
                            headers = {}
                            errors = str(e)
                    except Exception as e:
                            status = 0
                            headers = {}
                            errors = str(e)

                    # If code is 429, check Retry-After and honor it
                    if status == 429:
                            ra = headers.get("Retry-After")
                            wait = parse_retry_after(ra)
                            if wait is None:
                                    # Default backoff if Retry-After is absent
                                    wait = 2 ** (tries - 1)
                                    # add a small amount of jitter
                                    wait = wait + random.uniform(0, 1.0)
                            print(f"{now_iso()} {full}: 429 -> honoring Retry-After {wait}s")
                            await asyncio.sleep(wait)
                    else:
                            # Handle success or other status codes
                            break

                    if tries >= max_retries:
                            print(f"{now_iso()} {full}: Giving up after {tries} tries (last status {status})")
                            break

            # If there were connection errors and http_fallback is set try http:// once
            if status == 0 and http_fallback and tries < max_retries:
                    tries += 1
                    url_template = "http://{}"
                    url = url_template.format(full)
                    try:
                            async with session.get(url, timeout=timeout, allow_redirects=True) as resp:
                                    status = resp.status
                                    headers = resp.headers
                                    errors = None
                    except Exception as e:
                            errors = str(e)

            # Record result
            timestamp = now_iso()
            row = {
                    "timestamp": timestamp,
                    "subdomain": full,
                    "status": status,
                    "tries": tries,
                    "error": errors or ""
}

            # write to CSV (guard with lock)
            async with csv_lock:
                    writer.writerow([row["timestamp"], row["subdomain"], row["status"], row["tries"], row["error"]])
                    # make sure it's on disk
                    try:
                            # Writer has underlying file as writer.writerows? can flush file
                            csvfile = writer._csv_writer # not standard - avoid. Instead pass file handle
                    except Exception:
                            pass

            # Console log concise
            print(f"{full}: status={status} (tries={tries})")

            # Rate-limit per worker with jitter
            delay = min_delay + random.uniform(0, min_delay)
            await asyncio.sleep(delay)

async def run(subdomains, domain, concurrency, min_delay, max_retries, output_file, http_fallback, user_agent, connect_timeout, total_timeout):
    # aiohttp timeout object
    timeout = ClientTimeout(total=total_timeout, connect=connect_timeout)

    sem = asyncio.Semaphore(concurrency)
    csv_lock = asyncio.Lock()

    # Open CSV file synchronously (safe) and create csv.writer
    # Pass the writer and file handle as closure for flush
    with open(output_file, "w", newline="", encoding="utf-8") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(["timestamp", "subdomain", "status", "tries", "error"])


            headers = {
                    "User-Agent": user_agent,
                    # add additional headers if needed
            }

            connector = aiohttp.TCPConnector(limit=None, ssl=True) # let semaphore control concurrency

            async with aiohttp.ClientSession(headers=headers, timeout=timeout, connector=connector) as session:
                    tasks = []
                    for sub in subdomains:
                            sub = sub.strip()
                            if not sub:
                                    continue
                            # Wrap fetch_one so it can acces csv_writer and file flush
                            # csv_writer is synchronous but small writes are fine; protected by csv_lock
                            task = asyncio.create_task(
                                    fetch_one(sub, domain, session, sem, csv_lock, csv_writer, min_delay, max_retries, http_fallback, user_agent, timeout)
                            )
                            tasks.append(task)

                    # Run tasks and waut fir completion (gather with return_exception=False will raise if any task errors out)
                    await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(description="Check subdomains for HTTP status codes (async, rate-limited).")
    parser.add_argument("subdomains_file", help="File with one subdomain per line (e.g. www, api, mail")
    parser.add_argument("domain", help="Root domain (e.g. example.com")
    parser.add_argument("--concurrency", "-c", type=int, default=5, help="Number of concurrent workers (default 5)")
    parser.add_argument("--min_delay", "-d", type=float, default=0.2, help="Minimum delay in seconds per worker between requests (default 0.2s)")
    parser.add_argument("--max_retries", "-r", type=int, default=4, help="Maximum retries Retry-After/backoff (default 4)")
    parser.add_argument("--output", "-o", default="results.csv", help="CSV output file (default results.csv)")
    parser.add_argument("--http_fallback", action="store_true", help="If HTTP fails, try HTTP once")
    parser.add_argument("--user_agent", default="SubdomainChecker/1.0 (+contact@example.com", help="User-Agent header (be polite!)")
    parser.add_argument("--connect_timeout", type=float, default=5.0, help="Connect timeout in seconds (default 5s)")
    parser.add_argument("--total_timeout", type=float, default=10.0, help="Total request timeout in seconds (default 10s")
    args = parser.parse_args()

    # read domain files
    try:
            with open(args.subdomains_file, "r", encoding="utf-8") as fh:
                    subs = [line.strip() for line in fh if line.strip()]
    except FileNotFoundError:
            print(f"Subdomains file not found: {args.subdomains_file}", file=sys.stderr)
            sys.exit(2)

    print(f"\n\t---------------------")
    print(f"{now_iso()} Starting: domain={args.domain}, subdomains={len(subs)}, concurrency={args.concurrency}")
    print(f"\t---------------------\n")
    asyncio.run(run(subs, args.domain, args.concurrency, args.min_delay, args.max_retries, args.output, args.http_fallback, args.user_agent, args.connect_timeout, args.total_timeout))
    print(f"\n\t---------------------")
    print(f"{now_iso()} Done. Results written to {args.output}")
    print(f"\t---------------------\n")

if __name__ == "__main__":
    main()