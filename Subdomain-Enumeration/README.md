# Subdomain Enumeration

## Overview
The following Python script with example subdomain files can be used to ethically enumerate a domain address such as ```example.com``` to find ```www.example.com``` and ```app.example.com```

## Usage
Only in an ethical motive and written approval from the owner of the site being enumerated

## Dependancies
For proper usage ensure the Python environment is up to date and the package "aiohttp" is installed into the python environment.
To install the "aiohttp" module one can use ```pip install aiohttp```

## Parameters
```
REQUIRED - subdomains_file, File with one subdomain per line (e.g. www, api, mail)
REQUIRED - domain, Root domain (e.g. example.com)
--concurrency, "-c", Number of concurrent workers (default 5)
--min_delay, "-d", Minimum delay in seconds per worker between requests (default 0.2s)
--max_retries, "-r", Maximum retries Retry-After/backoff (default 4)
--output, "-o", CSV output file (default results.csv)
--http_fallback, If HTTPS fails, try HTTP once
--user_agent, User-Agent header (be polite!) (default "SubdomainChecker/1.0 (+contact@example.com)")
--connect_timeout, Connect timeout in seconds (default 5s)
--total_timeout, Total request timeout in seconds (default 10s)
```
## Help
Display a help screen for optional parameters and minimum input
```bash
>python3 find_subdomains.py -h

usage: find_subdomains.py [-h] [--concurrency CONCURRENCY] [--min_delay MIN_DELAY] [--max_retries MAX_RETRIES] [--output OUTPUT]
                          [--http_fallback] [--user_agent USER_AGENT] [--connect_timeout CONNECT_TIMEOUT]
                          [--total_timeout TOTAL_TIMEOUT]
                          subdomains_file domain

Check subdomains for HTTP status codes (async, rate-limited).

positional arguments:
  subdomains_file       File with one subdomain per line (e.g. www, api, mail
  domain                Root domain (e.g. example.com

options:
  -h, --help            Show this help message and exit
  --concurrency, -c CONCURRENCY
                        Number of concurrent workers (default 5)
  --min_delay, -d MIN_DELAY
                        Minimum delay in seconds per worker between requests (default 0.2s)
  --max_retries, -r MAX_RETRIES
                        Maximum retries Retry-After/backoff (default 4)
  --output, -o OUTPUT   CSV output file (default results.csv)
  --http_fallback       If HTTP fails, try HTTP once
  --user_agent USER_AGENT
                        User-Agent header (be polite!)
  --connect_timeout CONNECT_TIMEOUT
                        Connect timeout in seconds (default 5s)
  --total_timeout TOTAL_TIMEOUT
                        Total request timeout in seconds (default 10s)
```
## Examples
Template usage with the default parameters
```bash
>python3 find_subdomains.py <subdomain_file_list> <domain>
```
Using the script with default parameters sends the output to ```results.csv```
```bash
>python3 find_subdomains.py small_list_subdomain.txt example.com

        ---------------------
2025-11-11T21:57:40.821296+09:00 Starting: domain=example.com, subdomains=17, concurrency=5
        ---------------------

mail.example.com: status=0 (tries=1)
support.example.com: status=0 (tries=1)
www.example.com: status=200 (tries=1)
help.example.com: status=0 (tries=1)
m.example.com: status=0 (tries=1)
login.example.com: status=0 (tries=1)
ftp.example.com: status=0 (tries=1)
admin.example.com: status=0 (tries=1)
lists.example.com: status=0 (tries=1)
mobile.example.com: status=0 (tries=1)
shop.example.com: status=0 (tries=1)
email.example.com: status=0 (tries=1)
api.example.com: status=0 (tries=1)
info.example.com: status=0 (tries=1)
app.example.com: status=0 (tries=1)
store.example.com: status=0 (tries=1)
live.example.com: status=0 (tries=1)

        ---------------------
2025-11-11T21:57:42.321024+09:00 Done. Results written to results.csv
        ---------------------

```
From the findings only ```www.example.com``` was found to give a HTTP 200 code. To further analyze one can look at the CSV file.
The CSV file contains the timestamp, subdomain, status code, attempts to connect, and error messages if any. This can be useful for longer subdomain lists. 
```bash
>cat results.csv

timestamp,subdomain,status,tries,error
2025-11-11T21:57:40.847760+09:00,mail.example.com,0,1,Cannot connect to host mail.example.com:443 ssl:default [getaddrinfo failed]    
2025-11-11T21:57:40.847966+09:00,support.example.com,0,1,Cannot connect to host support.example.com:443 ssl:default [getaddrinfo failed]
2025-11-11T21:57:40.893212+09:00,www.example.com,200,1,
2025-11-11T21:57:40.981773+09:00,help.example.com,0,1,Cannot connect to host help.example.com:443 ssl:default [getaddrinfo failed]    
2025-11-11T21:57:40.984248+09:00,m.example.com,0,1,Cannot connect to host m.example.com:443 ssl:default [getaddrinfo failed]
2025-11-11T21:57:41.267715+09:00,login.example.com,0,1,Cannot connect to host login.example.com:443 ssl:default [getaddrinfo failed]  
2025-11-11T21:57:41.359159+09:00,ftp.example.com,0,1,Cannot connect to host ftp.example.com:443 ssl:default [getaddrinfo failed]      
2025-11-11T21:57:41.367577+09:00,admin.example.com,0,1,Cannot connect to host admin.example.com:443 ssl:default [getaddrinfo failed]  
2025-11-11T21:57:41.451091+09:00,lists.example.com,0,1,Cannot connect to host lists.example.com:443 ssl:default [getaddrinfo failed]  
2025-11-11T21:57:41.492111+09:00,mobile.example.com,0,1,Cannot connect to host mobile.example.com:443 ssl:default [getaddrinfo failed]
2025-11-11T21:57:41.528376+09:00,shop.example.com,0,1,Cannot connect to host shop.example.com:443 ssl:default [getaddrinfo failed]    
2025-11-11T21:57:41.650392+09:00,email.example.com,0,1,Cannot connect to host email.example.com:443 ssl:default [getaddrinfo failed]  
2025-11-11T21:57:41.696119+09:00,api.example.com,0,1,Cannot connect to host api.example.com:443 ssl:default [getaddrinfo failed]      
2025-11-11T21:57:41.710036+09:00,info.example.com,0,1,Cannot connect to host info.example.com:443 ssl:default [getaddrinfo failed]    
2025-11-11T21:57:41.816941+09:00,app.example.com,0,1,Cannot connect to host app.example.com:443 ssl:default [getaddrinfo failed]      
2025-11-11T21:57:41.936098+09:00,store.example.com,0,1,Cannot connect to host store.example.com:443 ssl:default [getaddrinfo failed]  
2025-11-11T21:57:42.079123+09:00,live.example.com,0,1,Cannot connect to host live.example.com:443 ssl:default [getaddrinfo failed]
```
Then to clean up the results use a set of commands like to clean up or use for further scripts ```grep | awk```
```bash
>grep -Eo '[^,]+,[2-5][0-9]{2}' results.csv | awk -F , '{ print $1, $2 }'

www.example.com 200
```
