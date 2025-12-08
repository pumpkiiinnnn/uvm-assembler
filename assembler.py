import json
import sys

# ---------- функции кодирования ----------

def encode_load_const(B, C):
    A = 7
    value = A | (B << 5) | (C << 11)
    return value.to_bytes(4, "little")


def encode_load_mem(B, C, D):
    A = 1
    value = A | (B << 5) | (C << 11) | (D << 17)
    return value.to_bytes(5, "little")


def encode_store_mem(B, C, D):
    A = 18
    value = A | (B << 5) | (C << 11) | (D << 17)
    return value.to_bytes(5, "little")


def encode_bitreverse(B, C):
    A = 19
    value = A | (B << 5) | (C << 11)
    return value.to_bytes(3, "little")


# ---------- главная часть ----------

def main():
    if len(sys.argv) < 3:
        print("Usage: python assembler.py input.json output.bin [--test]")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    test_mode = "--test" in sys.argv

    with open(input_file, "r", encoding="utf-8") as f:
        program = json.load(f)

    binary = bytearray()

    for cmd in program:
        op = cmd["op"]

        if op == "load_const":
            data = encode_load_const(cmd["B"], cmd["C"])

        elif op == "load_mem":
            data = encode_load_mem(cmd["B"], cmd["C"], cmd["D"])

        elif op == "store_mem":
            data = encode_store_mem(cmd["B"], cmd["C"], cmd["D"])

        elif op == "bitreverse":
            data = encode_bitreverse(cmd["B"], cmd["C"])

        else:
            print("Unknown operation:", op)
            return

        if test_mode:
            print(op, cmd)
            print([hex(b) for b in data])

        binary.extend(data)

    with open(output_file, "wb") as f:
        f.write(binary)
    print("assembled commands: ", len(program))
    print("Done.")


if __name__ == "__main__":
    main()