import struct
import sys
import xml.etree.ElementTree as ET

MEMORY = [0] * 256  # Простая память на 256 ячеек
STACK = []

def execute(input_file, result_file, memory_range):
    with open(input_file, 'rb') as f:
        code = f.read()

    i = 0
    while i < len(code):
        opcode = code[i] >> 2
        operand = struct.unpack(">H", code[i:i+2])[0] & 0xFFFF
        i += 3

        if opcode == 0x1A:  # LOAD_CONST
            STACK.append(operand)
        elif opcode == 0x35:  # LOAD_MEM
            STACK.append(MEMORY[operand])
        elif opcode == 0x05:  # STORE
            addr = STACK.pop()
            value = STACK.pop()
            MEMORY[addr] = value
        elif opcode == 0x3C:  # OR
            addr = operand
            value = STACK.pop()
            MEMORY[addr] |= value

    # Сохранение результата
    result_root = ET.Element("memory")
    start, end = map(int, memory_range.split(":"))
    for i in range(start, end + 1):
        cell = ET.SubElement(result_root, "cell")
        cell.set("address", str(i))
        cell.set("value", str(MEMORY[i]))

    tree = ET.ElementTree(result_root)
    tree.write(result_file)

if __name__ == "__main__":
    input_path = sys.argv[1]
    result_path = sys.argv[2]
    memory_range = sys.argv[3]
    execute(input_path, result_path, memory_range)
