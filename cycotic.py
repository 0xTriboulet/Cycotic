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

def process_c_file(file_path, instructions, remove=False):
    with open(file_path, 'r') as input_file:
        file_contents = input_file.read()

    if remove:
        modified_contents = remove_asm_statements(file_contents)
    else:
        modified_contents = insert_asm_statements(file_contents, instructions)

    with open(file_path, 'w') as output_file:
        output_file.write(modified_contents)

def process_directory(directory_path, instructions, remove=False):
    for filename in os.listdir(directory_path):
        if filename.endswith('.c'):
            file_path = os.path.join(directory_path, filename)
            process_c_file(file_path, instructions, remove)

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

    process_directory(directory_path, instructions, remove)
