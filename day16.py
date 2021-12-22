from aocd.models import Puzzle
import operator
import functools

debug_logging_enabled = False

def puzzle_input_data():
    puzzle = Puzzle(year = 2021, day = 16)
    return puzzle.input_data

def convert_to_bitstr(hexcode):
    # convert hex string into binary array
    bitstr = ""
    for c in hexcode:
        hex = int(c, 16)
        nibble = "{:01b}".format(hex).zfill(4)
        bitstr += nibble
    assert (len(bitstr) % 4) == 0
    return bitstr

#print(convert_to_bin_array(test_input_data1))

def debug(str):
    if debug_logging_enabled:
        print("debug: " + str)

def lt_int_value(a, b):
    return a < b and 1 or 0

def gt_int_value(a, b):
    return a > b and 1 or 0

def eq_int_value(a, b):
    return a == b and 1 or 0

def get_operator_fn(packet_type):
    if packet_type == 0:
        debug("found +")
        return operator.add
    elif packet_type == 1:
        debug("found *")
        return operator.mul
    elif packet_type == 2:
        debug("found min")
        return min
    elif packet_type == 3:
        debug("found max")
        return max
    elif packet_type == 5:
        debug("found >")
        return gt_int_value
    elif packet_type == 6:
        debug("found <")
        return lt_int_value
    elif packet_type == 7:
        debug("found ==")
        return eq_int_value
    else:
        raise Exception(f"invalid operator packet type: {packet_type}")

def decode_subpacket(bitstr, start):
    # returns the final index it consumed, the total of the version
    # numbers, and the calculated value
    total_version = 0
    # bits 0-2 for version
    packet_version = int(bitstr[start:start + 3], 2)
    total_version += packet_version
    # bits 3-5 for type 
    packet_type = int(bitstr[start+3:start+6], 2)
    if packet_type == 4:
        # literal follows in groups of 5 bits
        offset = 6
        has_more = True
        literal = ""
        while has_more:
            literal += bitstr[start + offset +  1 : start + offset + 5]
            if int(bitstr[start + offset], 2) == 1:
                has_more = True
            else:
                has_more = False
            offset += 5
        value = int(literal, 2)
        debug(f"found literal {value}")
        return (start + offset - 1, total_version, value)
    else:
        # indicates an operator packet
        operator_fn = get_operator_fn(packet_type)
        sub_values = []
        length_type_id = int(bitstr[start+6], 2)
        if length_type_id == 0:
            # a 15 bit number follows containing the length of the *series*
            # of subpackets
            subpacket_series_length = int(bitstr[start+7 : start+7+15], 2)
            subpacket_series_start = start + 7 + 15
            # process each subpacket
            subpacket_start = subpacket_series_start
            while subpacket_start < subpacket_series_start + subpacket_series_length:
                assert subpacket_start < len(bitstr)
                (subpacket_end, sub_version, sub_value) = decode_subpacket(bitstr, subpacket_start)
                sub_values.append(sub_value)
                total_version += sub_version
                subpacket_start = subpacket_end + 1
            # should not read past the length if the packet is valid
            value = functools.reduce(operator_fn, sub_values)
            assert subpacket_start == subpacket_series_start + subpacket_series_length

            return (subpacket_series_start + subpacket_series_length - 1, total_version, value)
        else:
            # a 11 bit number follows containing the number of subpackets in the series
            num_subpackets = int(bitstr[start+7 : start+7+11], 2)
            subpacket_series_start = start + 7 + 11
            # process each subpacket
            subpacket_start = subpacket_series_start
            for subpacket_num in range(0, num_subpackets):
                assert subpacket_start < len(bitstr)
                (subpacket_end, sub_version, sub_value) = decode_subpacket(bitstr, subpacket_start)
                sub_values.append(sub_value)
                total_version += sub_version
                subpacket_start = subpacket_end + 1
            value = functools.reduce(operator_fn, sub_values)
            return (subpacket_start - 1, total_version, value)
    

def decode_packet(packet):
    print(f"Decoding packet: {packet}")
    bitstr = convert_to_bitstr(packet)
    (end, total_version, value) = decode_subpacket(bitstr, 0)
    if end < len(bitstr) - 1:
        # this is okay, there can be trailing bits
        debug(f"outer packet has {len(bitstr) - end - 1} trailing bits")
    return (total_version, value)

print(decode_packet("D2FE28"))
print(decode_packet("38006F45291200"))
print(decode_packet("EE00D40C823060"))

print(decode_packet("8A004A801A8002F478"))
print(decode_packet("620080001611562C8802118E34"))
print(decode_packet("C0015000016115A2E0802F182340"))
print(decode_packet("A0016C880162017C3686B18A3D4780"))

print("")
print("C200B40A82 finds the sum of 1 and 2, resulting in the value 3.")
print(decode_packet("C200B40A82"))
print("")

print("04005AC33890 finds the product of 6 and 9, resulting in the value 54.")
print(decode_packet("04005AC33890"))
print("")

print("880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.")
print(decode_packet("880086C3E88112"))
print("")

print("CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.")
print(decode_packet("CE00C43D881120"))
print("")

print("D8005AC2A8F0 produces 1, because 5 is less than 15.")
print(decode_packet("D8005AC2A8F0"))
print("")

print("F600BC2D8F produces 0, because 5 is not greater than 15.")
print(decode_packet("F600BC2D8F"))
print("")

print("9C005AC2F8F0 produces 0, because 5 is not equal to 15.")
print(decode_packet("9C005AC2F8F0"))
print("")

print("9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.")
print(decode_packet("9C0141080250320F1802104A08"))
print("")

print(decode_packet(puzzle_input_data()))
