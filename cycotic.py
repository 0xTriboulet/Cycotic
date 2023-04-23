import os
import re
import random
import sys

def insert_asm_before_vars(file_contents, instructions):
    return_pattern = re.compile(r"^\s*(?P<type>\w+)\s+(?P<var_name>\w+)\s*=\s*(?P<value>[^;]+)\s*;", re.MULTILINE)

    def insert_asm(match):
        num_statements = random.randint(0, 3)
        asm_statements = "\n".join(
            "//remove me\nasm(\"{}\");".format(random.choice(instructions)) for _ in range(num_statements)
        )
        return asm_statements + "\n" + match.group(0)

    modified_contents = return_pattern.sub(insert_asm, file_contents)

    return modified_contents

def insert_asm_statements(file_contents, instructions):
    modified_contents = insert_asm_before_vars(file_contents, instructions)

    function_pattern = re.compile(
        r"(?P<return_type>[\w\s\*]+)\s+(?P<func_name>\w+)\s*\((?P<params>[^\)]*)\)\s*\{",
        re.MULTILINE
    )

    def insert_asm(match):
        num_statements = random.randint(1, 10)
        asm_statements = "\n".join(
            "//remove me\nasm(\"{}\");".format(random.choice(instructions)) for _ in range(num_statements)
        )
        return match.group(0) + "\n" + asm_statements

    modified_contents = function_pattern.sub(insert_asm, modified_contents)

    return modified_contents

def remove_asm_statements(file_contents):
    # Regex pattern to match and remove lines after "//remove me" comments
    remove_pattern = re.compile(r"//remove me\n.*;\n?", re.MULTILINE)
    modified_contents = remove_pattern.sub("", file_contents)
    return modified_contents

def insert_string_declarations(file_contents, eula):
    function_pattern = re.compile(
        r"(?P<return_type>[\w\s\*]+)\s+(?P<func_name>\w+)\s*\((?P<params>[^\)]*)\)\s*\{",
        re.MULTILINE
    )

    def insert_string(match):
        num_statements = random.randint(1, 50)
        string_statements = "\n".join(
            "//remove me\nchar *str{} = \"{}\";".format(random.randint(10000, 99999), random.choice(eula)) for _ in range(num_statements)
        )
        return match.group(0) + "\n" + string_statements

    modified_contents = function_pattern.sub(insert_string, file_contents)

    return modified_contents

def remove_string_declarations(file_contents):
    # Regex pattern to match and remove lines after "//remove me" comments
    remove_pattern = re.compile(r"//remove me\nchar \*str\d+ = \".*?\";\n?", re.MULTILINE)
    modified_contents = remove_pattern.sub("", file_contents)
    return modified_contents

def process_c_file(file_path, instructions, eula, remove=False):
    with open(file_path, 'r') as input_file:
        file_contents = input_file.read()

    if remove:
        modified_contents = remove_asm_statements(file_contents)
        modified_contents = remove_string_declarations(modified_contents)
    else:
        modified_contents = insert_asm_statements(file_contents, instructions)
        modified_contents = insert_string_declarations(modified_contents, eula)

    with open(file_path, 'w') as output_file:
        output_file.write(modified_contents)

def process_directory(directory_path, instructions, eula, remove=False):
    for filename in os.listdir(directory_path):
        if filename.endswith('.c'):
            file_path = os.path.join(directory_path, filename)
            process_c_file(file_path, instructions, eula, remove)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_directory> [--remove]")
        sys.exit(1)

    directory_path = sys.argv[1]
    remove = "--remove" in sys.argv

    # List of sample assembly instructions
    instructions = [
        "nop",
        "dec rax",
        "inc rax",
        "xor rax, rax",
        "xor eax, eax",
        ''"xor eax, eax;" \
        "xor eax, eax;" \
        "xor ecx, ecx;" \
        "xor edx, edx;" \
        "xor r8d, r8d;"''
    ]
    
    eula = ["MICROSOFT SOFTWARE LICENSE TERMS",\
            "(MVLTECHNOLOGIES1.0 – STABLE CHANNEL)",\
            "MICROSOFT VISUAL STUDIO COMMUNITY 2019",\
            "These license terms are an agreement between",\
            "Microsoft Corporation (or based on where you live,",\
            "one of its affiliates) and you. Please read them.",\
            "They apply to the software named above, which",\
            "includes the media on which you received it, if",\
            "any. The terms also apply to any Microsoft",\
            "updates,", "supplements,", "Internet-based services,",\
            "and support services", "for", "this software, unless",\
            "other terms accompany those items. If so, those",\
            "terms apply.", "BY USING THE SOFTWARE, YOU ACCEPT",\
            "THESE TERMS. IF YOU DO NOT ACCEPT THEM, DO NOT",\
            "USE THE SOFTWARE. INSTEAD, RETURN IT TO THE",\
            "RESELLER FOR A REFUND OR CREDIT.", "As described",\
            "below,", "using the software also operates as your",\
            "consent", "to the transmission of certain",\
            "computer", "information", "for Internet-based",\
            "services,", "as", "described", "in the privacy",\
            "statement", "described in Section 3. If you",\
            "comply with these license terms, you have the",\
            "rights below.", "1. INSTALLATION AND USE RIGHTS.",\
            "a. Individual license. If you are an individual",\
            "working on your own applications to sell or for",\
            "any other purpose,", "you may use the software to",\
            "develop", "and test", "those applications."]


    process_directory(directory_path, instructions, eula, remove)
