import json
import re
import os

def parse_caostables(content):
    tables = {}
    # Find all table definitions
    table_pattern = re.compile(r'OpSpec\s+(\w+)\[\]\s*=\s*\{(.*?)\}\s*;', re.DOTALL)
    
    # Version 1 (Sub-tables): OpSpec( opcode, name, args, arg_names, category, desc )
    # Version 2 (Main tables): OpSpec( name, handler, args, arg_names, category, desc )
    # Note: Description can contain escaped quotes
    opspec_pattern = re.compile(r'OpSpec\s*\((.*?)\)', re.DOTALL)
    
    for match in table_pattern.finditer(content):
        table_name = match.group(1)
        table_content = match.group(2)
        
        commands = []
        for cmd_match in opspec_pattern.finditer(table_content):
            args_str = cmd_match.group(1)
            # Split by comma but respect quotes
            parts = []
            current_part = []
            in_quote = False
            for char in args_str:
                if char == '"' and (not current_part or current_part[-1] != '\\'):
                    in_quote = not in_quote
                if char == ',' and not in_quote:
                    parts.append(''.join(current_part).strip())
                    current_part = []
                else:
                    current_part.append(char)
            parts.append(''.join(current_part).strip())
            
            if len(parts) >= 6:
                # Determine if first part is opcode or name
                first = parts[0].strip('"')
                if parts[0].startswith('"'):
                    name = first
                    args = parts[2].strip('"')
                    arg_names = parts[3].strip('"')
                    category = parts[4]
                    desc = parts[5].strip('"')
                else:
                    name = parts[1].strip('"')
                    args = parts[2].strip('"')
                    arg_names = parts[3].strip('"')
                    category = parts[4]
                    desc = parts[5].strip('"')
                
                commands.append({
                    'name': name,
                    'args': args,
                    'arg_names': arg_names,
                    'category': category,
                    'description': desc
                })
        tables[table_name] = commands
    return tables

def get_full_name(table_name, cmd_name):
    prefix_map = {
        'HIST': 'HIST:',
        'FILE': 'FILE:',
        'GENE': 'GENE:',
        'PRAY': 'PRAY:',
        'NEW': 'NEW:',
        'MESG': 'MESG:',
        'STIM': 'STIM:',
        'URGE': 'URGE:',
        'SWAY': 'SWAY:',
        'ORDR': 'ORDR:',
        'GIDS': 'GIDS:',
        'PRT': 'PRT:',
        'PAT': 'PAT:',
        'BRN': 'BRN:',
        'DBG': 'DBG:',
    }
    for sub, pref in prefix_map.items():
        if sub in table_name:
            # openc2e uses ": " for namespaces in names
            return f"{pref} {cmd_name}"
    
    # Handle the cases where the name itself ends with a colon in C3
    if cmd_name.endswith(':'):
        return cmd_name + ' '
        
    return cmd_name

def audit():
    repo_path = 'c:/Users/cyril/projects/openc2e'
    json_path = os.path.join(repo_path, 'build/generated/commandinfo.json')
    cpp_path = os.path.join(repo_path, 'CAOSTables.cpp')
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return
    if not os.path.exists(cpp_path):
        print(f"Error: {cpp_path} not found")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        openc2e_cmds = json.load(f)
        
    with open(cpp_path, 'r', encoding='latin-1') as f:
        cpp_content = f.read()
        
    c3_tables = parse_caostables(cpp_content)
    
    # Map openc2e commands by name
    openc2e_map = {}
    for cmd in openc2e_cmds:
        name = cmd['name']
        if name not in openc2e_map:
            openc2e_map[name] = []
        openc2e_map[name].append(cmd)
        
    report = {
        'matched': [],
        'stub': [],
        'missing': [],
        'extra': []
    }
    
    # Iterate over C3 commands
    all_c3_names = set()
    missing_by_cat = {}
    stubs_by_cat = {}
    
    for table_name, cmds in c3_tables.items():
        if table_name == 'ourCategoryText':
            continue
        for cmd in cmds:
            if cmd['name'] == 'X' and cmd['category'] == 'categoryNoNeedToDocument':
                continue
            full_name = get_full_name(table_name, cmd['name'])
            all_c3_names.add(full_name)
            cat = cmd['category'].replace('category', '')
            
            if full_name in openc2e_map:
                impls = openc2e_map[full_name]
                is_stub = all(c.get('status') == 'stub' for c in impls)
                if is_stub:
                    report['stub'].append(full_name)
                    if cat not in stubs_by_cat: stubs_by_cat[cat] = []
                    stubs_by_cat[cat].append(full_name)
                else:
                    report['matched'].append(full_name)
            else:
                report['missing'].append(full_name)
                if cat not in missing_by_cat: missing_by_cat[cat] = []
                missing_by_cat[cat].append(full_name)
                
    # Extra commands in openc2e
    for full_name in openc2e_map:
        if full_name not in all_c3_names:
            report['extra'].append(full_name)
            
    # Output report
    print(f"CAOS Command Table Audit Report")
    print(f"==============================")
    print(f"Total C3 Commands Found: {len(all_c3_names)}")
    print(f"Matched (Implemented): {len(report['matched'])}")
    print(f"Stubs (Not fully implemented): {len(report['stub'])}")
    print(f"Missing in openc2e: {len(report['missing'])}")
    print(f"Extra in openc2e: {len(report['extra'])}")
    print()
    
    print("### Missing Commands by Category ###")
    for cat in sorted(missing_by_cat.keys()):
        print(f"#### {cat}")
        for name in sorted(set(missing_by_cat[cat])):
            print(f"- {name}")
    print()
    
    print("### Stub Commands by Category ###")
    for cat in sorted(stubs_by_cat.keys()):
        print(f"#### {cat}")
        for name in sorted(set(stubs_by_cat[cat])):
            print(f"- {name}")

if __name__ == '__main__':
    audit()

if __name__ == '__main__':
    audit()
