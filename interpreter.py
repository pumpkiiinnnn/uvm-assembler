import sys
import xml.etree.ElementTree as ET

MEM_SIZE = 1024


def dump_memory_xml(memory, start, end, filename):
    root = ET.Element("memory")

    for addr in range(start, end + 1):
        cell = ET.SubElement(root, "cell")
        cell.set("address", str(addr))
        cell.text = str(memory[addr])

    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)


def main():
    if len(sys.argv) < 5:
        print("Usage: python interpreter.py program.bin dump.xml start end")
        return

    bin_file = sys.argv[1]
    dump_file = sys.argv[2]
    start_addr = int(sys.argv[3])
    end_addr = int(sys.argv[4])

    with open(bin_file, "rb") as f:
        binary = f.read()

    # Общая память (код + данные)
    memory = [0] * MEM_SIZE
    for i, b in enumerate(binary):
        memory[i] = b
    DATA_BASE = len(binary) + 16

    registers = [0] * 32
    pc = 0

    # -------- ОСНОВНОЙ ЦИКЛ ИНТЕРПРЕТАТОРА --------
    while pc < len(binary):

        # читаем код операции
        opcode = memory[pc] & 0b11111

        # ---------- load_const ----------
        if opcode == 7:
            instr = int.from_bytes(binary[pc:pc + 4], "little")
            B = (instr >> 5) & 0b111111
            C = (instr >> 11) & 0b111111
            registers[B] = C
            pc += 4

        # ---------- load_mem ----------
        elif opcode == 1:
            instr = int.from_bytes(binary[pc:pc + 5], "little")
            B = (instr >> 5) & 0b111111
            C = (instr >> 11) & 0b111111
            D = (instr >> 17)
            addr = DATA_BASE + registers[C] + D
            registers[B] = memory[addr]
            pc += 5

        # ---------- store_mem ----------
        elif opcode == 18:
            instr = int.from_bytes(binary[pc:pc + 5], "little")
            B = (instr >> 5) & 0b111111
            C = (instr >> 11) & 0b111111
            D = (instr >> 17)
            addr = DATA_BASE + registers[C] + D
            memory[addr] = registers[B]
            pc += 5

        # ---------- bitreverse ----------
        elif opcode == 19:
            instr = int.from_bytes(binary[pc:pc + 3], "little")
            B = (instr >> 5) & 0b111111
            C = (instr >> 11) & 0b111111
            value = registers[C]
            reversed_bits = int('{:08b}'.format(value)[::-1], 2)
            registers[B] = reversed_bits
            pc += 3

        else:
            print("Unknown opcode:", opcode)
            break

    dump_memory_xml(memory, start_addr, end_addr, dump_file)
    print("Execution finished.")


if __name__ == "__main__":
    main()