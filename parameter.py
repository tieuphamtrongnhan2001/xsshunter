from urllib.parse import urlparse, parse_qs

def extract_params(url):
    # Phân tích cú pháp URL
    parsed_url = urlparse(url)
    
    # Lấy các tham số truy vấn từ URL
    query_params = parse_qs(parsed_url.query)
    
    # In ra các tham số
    for param, value in query_params.items():
        print(f"Parameter: {param}, Value: {value}")

# Ví dụ sử dụng
url = "https://huflit.edu.vn/new/sinh-vien-khoa-quan-he-quoc-te-tham-du-bao-cao-chuyen-de-american-government-and-democractic-principles-cung-giao-su-mark-tiller/?preview_id=2039&preview_nonce=4c13429dd3&preview=true"
extract_params(url)
