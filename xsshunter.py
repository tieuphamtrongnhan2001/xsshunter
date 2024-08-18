import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import threading
from art import *
from termcolor import colored

# Thiết lập tùy chọn dòng lệnh
parser = argparse.ArgumentParser(description="XSS Fuzzing Tool Powerby @Nhan.tieu")

parser.add_argument('-u', '--url', type=str, required=True, help='Target URL')
parser.add_argument('-p', '--payload', type=str, default="payloads.txt", help='Payload file path (default: payloads.txt)')
parser.add_argument('-o', '--option', type=int, required=True, choices=[1, 2], help='Choose 1 for Reflected XSS check, 2 for Blind XSS check')
parser.add_argument('-r', '--result', type=str, default="results.txt", help='Result file path (default: results.txt)')

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
    fuzzed_url = urlunparse(parsed_url._replace(query=new_query))
    
    return fuzzed_url

def process_payload(payload, param):
    """Xử lý mỗi payload với tham số cụ thể."""
    fuzzed_url = fuzz_url(url, param, payload.strip())
    driver.get(fuzzed_url)
    try:
        if args.option == 1:
            try:
                # Kiểm tra nếu có cảnh báo hiện lên
                alert = driver.switch_to.alert
                alert.accept()
                result_file.write(f"Reflected XSS vulnerability found with payload:\n{fuzzed_url}\n")
                print(colored(f'Reflected XSS found with payload: {fuzzed_url}', 'red'))
            except:
                # Không làm gì nếu không có cảnh báo
                pass
        elif args.option == 2:
            try:
                time.sleep(5)  # Chờ để kiểm tra Blind XSS
                result_file.write(f"Blind XSS payload sent:\n{fuzzed_url}\n")
                print(colored(f"Blind XSS payload sent:\n {fuzzed_url}","red"))
                print("Payload delivery, check your server.")
            except:
                pass
    except Exception as e:
        # Không làm gì nếu có lỗi khác ngoài cảnh báo
        pass

def threaded_process(payload, params):
    """Hàm được chạy trong mỗi luồng để xử lý tất cả các tham số."""
    for param in params:
        process_payload(payload, param)

def main():
    result = text2art("XSS Hunter")
    print(result)
    print("FB: https://www.fb.com/profile.php?id=100090708972879")
    print("Linkedin: https://www.linkedin.com/in/nhan-tieu-pham-trong-5177382bb/")
    print("Wordfence Researcher: https://www.wordfence.com/threat-intel/vulnerabilities/researchers/tieu-nhan")
    
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    params = query_params.keys()
    threads = []
    try:
        for payload in payloads:
            # Tạo và bắt đầu một luồng cho mỗi payload
            thread = threading.Thread(target=threaded_process, args=(payload, params))
            thread.start()
            threads.append(thread)

        # Chờ tất cả các luồng hoàn thành
        for thread in threads:
            thread.join()

        driver.quit()
        result_file.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
