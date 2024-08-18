import argparse
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Thiết lập tùy chọn dòng lệnh
parser = argparse.ArgumentParser(description="XSS Fuzzing Tool Powerby @Nhan.tieu")

parser.add_argument('-u', '--url', type=str, required=True, help='Target URL')
parser.add_argument('-p', '--payload', type=str, default="payloads.txt", help='Payload file path (default: payloads.txt)')
parser.add_argument('-o', '--option', type=int, required=True, choices=[1, 2], help='Choose 1 for Reflected XSS check, 2 for Blind XSS check')
parser.add_argument('-r', '--result', type=str, default="results.txt", help='Result file path (default: results.txt)')
parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads (default: 10)')

args = parser.parse_args()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_argument("--silent")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)
url = args.url
payloads = open(args.payload, "r").readlines()
result_file = open(args.result, "w")

def fuzz_url(url, param, payload):
    """Chèn payload vào tham số cụ thể trong URL."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    query_params[param] = payload  # Chèn payload vào tham số cần fuzzing
    
    new_query = urlencode({k: v if isinstance(v, str) else v[0] for k, v in query_params.items()}, doseq=True)
    fuzzed_url = urlunparse(parsed_url._replace(query= new_query))
    
    return fuzzed_url

def process_payload(payload, param):
    """Xử lý mỗi payload với tham số cụ thể."""
    fuzzed_url = fuzz_url(url, param, payload.strip())
    driver.get(fuzzed_url)
    try:
        if args.option == 1:
            alert = driver.switch_to.alert
            alert.accept()
            result_file.write(f"Reflected XSS vulnerability found with payload:\n {fuzzed_url}\n")
            print(f"Reflected XSS vulnerability found with payload:\n {fuzzed_url}")
        elif args.option == 2:
            driver.get(fuzzed_url)
            time.sleep(5)
            result_file.write(f"Blind XSS payload sent:\n{fuzzed_url}\n")
            print(fuzzed_url)
            print("Payload delivery, check your server.")
    except:
        pass

def worker(payload):
    """Worker thread để xử lý payloads cho tất cả các tham số."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    params = query_params.keys()
    
    for param in params:
        process_payload(payload, param)

def main():
    print("-------------------------XSS HUNTER------------------------")
    print("FB: https://www.fb.com/profile.php?id=100090708972879")
    print("Linkedin: https://www.linkedin.com/in/nhan-tieu-pham-trong-5177382bb/")
    print("Wordfence Researcher: https://www.wordfence.com/threat-intel/vulnerabilities/researchers/tieu-nhan")
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(worker, payload) for payload in payloads]
        for future in futures:
            future.result()  # Đảm bảo tất cả các nhiệm vụ đã hoàn thành

    driver.quit()
    result_file.close()

if __name__ == "__main__":
    main()
