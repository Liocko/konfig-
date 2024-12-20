import struct
import xml.etree.ElementTree as ET
import sys

COMMANDS = {
    "LOAD_CONST": 0x1A,
    "LOAD_MEM": 0x35,
    "STORE": 0x05,
    "OR": 0x3C,
}

def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    binary_data = bytearray()
    log_root = ET.Element("log")

    for line in lines:
        line = line.split(';')[0].strip()
        if not line:
            continue

        parts = line.split()
        if not parts:
            continue

        command = parts[0]
        if command in COMMANDS:
            try:
                operand = int(parts[1]) if len(parts) > 1 else 0
            except ValueError:
                print(f"Ошибка: неверный операнд в строке '{line}'")
                continue

            opcode = COMMANDS[command]
            instruction_value = (opcode << 18) | (operand & 0x3FFFF)
            instruction = instruction_value.to_bytes(3, byteorder='big')
            binary_data.extend(instruction)

            entry = ET.SubElement(log_root, "instruction")
            entry.set("command", command)
            entry.set("operand", str(operand))
            entry.set("opcode", hex(opcode))
            entry.set("binary", instruction.hex())


    with open(output_file, 'wb') as f:
        f.write(binary_data)

    tree = ET.ElementTree(log_root)
    tree.write(log_file)

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    log_path = sys.argv[3]
    assemble(input_path, output_path, log_path)
