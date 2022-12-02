from utils import run

hex_to_bits = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}
test = """D2FE28
38006F45291200
EE00D40C823060
8A004A801A8002F478
620080001611562C8802118E34
C0015000016115A2E0802F182340
A0016C880162017C3686B18A3D4780"""


class Packet:
    __slots__ = (
        "line",
        "bits",
        "version",
        "type",
        "length_type",
        "value",
        "literal",
        "subpackets",
        "parent",
        "extra",
    )

    def __init__(self, line: str, *, hex: bool = True, parent: "Packet" = None):
        self.line = line
        self.bits = "".join(hex_to_bits[c] for c in line) if hex else line
        self.version = int(self.bits[:3], 2)
        self.type = int(self.bits[3:6], 2)
        self.length_type = None
        self.value = self.bits[6:]
        self.literal = None
        self.subpackets = []
        self.extra = ""
        self.parent = parent
        self.parse()

    def __repr__(self) -> str:
        attrs = ("type", "version", "length_type", "literal")
        inner = " ".join(f"{k}={getattr(self, k)!r}" for k in attrs if getattr(self, k) is not None)
        if self.parent:
            pass
            # inner += f" parent={self.parent.line!r}"
        return f"Packet(id={len(self.line)!r} {inner} subpackets={len(self.subpackets)!r})"

    def parse(self):
        # print("PP", self, self.value)
        if self.type != 4:
            self.parse_subpackets()
            return
        number_bits = []
        for i in range(0, len(self.value), 5):
            start = self.value[i]
            bits = self.value[i + 1:i + 5]
            number_bits.append(bits)
            if start == "0":
                if len(self.value) % 5 != 0:
                    self.extra = self.value[i + 5:]
                break
        self.literal = int("".join(number_bits), 2)

    def parse_subpackets(self):
        self.length_type = int(self.value[0])
        if self.length_type:
            num_subpackets = int(self.value[1:12], 2)
            value = self.value[12:]
            while len(self.subpackets) < num_subpackets:
                print("SP", end=" ")
                packet = Packet(value, hex=False, parent=self)
                self.subpackets.append(packet)
                value = packet.extra
                # print(num_subpackets, len(self.subpackets), value)
            self.extra = value
        else:
            bits_length = int(self.value[1:16], 2)
            print("BL:", bits_length)
            value = self.value[16:]
            self.extra = value[bits_length:]
            value = value[:bits_length]
            while value:
                print("BL", end=" ")
                packet = Packet(value, hex=False, parent=self)
                self.subpackets.append(packet)
                value = packet.extra
                print(self, len(self.subpackets))

    def version_sum(self):
        return self.version + sum(p.version_sum() for p in self.subpackets)


def print_subpackets(packet: Packet, header=""):
    print(header + str(packet))
    for p in packet.subpackets:
        print_subpackets(p, header + "  ")


@run(c=str)
def part1(data: list[str]) -> int:
    version_sum = 0
    for s in data:
        p = Packet(s)
        p_version_sum = p.version_sum()
        version_sum += p.version_sum()
        print("Version sum:", p_version_sum)
        print_subpackets(p)
    return version_sum
