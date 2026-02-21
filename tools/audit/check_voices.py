
import os

def check_voices():
    path = r'C:\Program Files (x86)\Steam\steamapps\common\Creatures Docking Station\Docking Station\Catalogue\voices.catalogue'
    if not os.path.exists(path):
        print("File not found")
        return

    with open(path, 'r', encoding='latin-1') as f:
        lines = f.readlines()

    current_tag = ""
    tag_data = []
    
    def process_tag(name, data):
        if not name: return
        print(f"Tag '{name}' has {len(data)} values")
        if name == 'DefaultLanguage':
            for i, val in enumerate(data):
                try:
                    int(val, 16)
                except ValueError:
                    print(f"Invalid hex value in DefaultLanguage at index {i}: '{val}'")
        else:
            # Voice tag
            if len(data) < 1: return
            # data[0] is language tag
            for i in range(1, len(data) - 1, 2):
                name_val = data[i]
                delay_val = data[i+1]
                try:
                    int(delay_val)
                except ValueError:
                    print(f"Invalid integer delay in '{name}' at index {i+1}: '{delay_val}' (name was '{name_val}')")

    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('TAG '):
            process_tag(current_tag, tag_data)
            current_tag = line[4:].strip('"')
            tag_data = []
            continue
        if line.startswith('"') and line.endswith('"'):
            tag_data.append(line.strip('"'))
        elif line.startswith('"') and line.endswith('""'): # accidental double quotes?
             tag_data.append(line.strip('"'))
             
    process_tag(current_tag, tag_data)
    print("Check complete")

if __name__ == '__main__':
    check_voices()

if __name__ == '__main__':
    check_voices()
