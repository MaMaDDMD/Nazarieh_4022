import sys
sys.path.append('C:/Users/pc/Desktop/Project-Template-Nazarih')
from math import log2
from phase0.FA_class import DFA, State
from utils.utils import imageType


def create_bit_addresses(index: int, bit_addresses: list[str]) -> None:
    global bit_address
    if index > 0:
        for i in range(4):
            bit_address += f"{i}"
            create_bit_addresses(index - 1, bit_addresses)
        bit_address = bit_address[:-1]
    else:
        bit_addresses.append(bit_address)
        bit_address = bit_address[:-1]


def find_j_indexes(k: int, resolution: int, j_indexes: list[int]) -> list[int]:
    if k == 0 or k == 2:
        temp: list[int] = []
        j = 0
        while j < resolution / 2:
            temp.append(j_indexes[j])
            j += 1
        return temp
    else:
        temp: list[int] = []
        j = int(resolution / 2)
        while j < resolution:
            temp.append(j_indexes[j])
            j += 1
        return temp


def find_i_indexes(k: int, resolution: int, i_indexes: list[int]) -> list[int]:
    if k == 0 or k == 1:
        temp: list[int] = []
        i = 0
        while i < resolution / 2:
            temp.append(i_indexes[i])
            i += 1
        return temp
    else:
        temp: list[int] = []
        i = int(resolution / 2)
        while i < resolution:
            temp.append(i_indexes[i])
            i += 1
        return temp


def find_indexes(bit_addresses: list[str], resolution: int, address_index: dict[str, list[int]]) -> dict[str, list[int]]:
    for address in bit_addresses:
        i_indexes: list[int] = []
        j_indexes: list[int] = []
        i = 0
        while i < resolution:
            i_indexes.append(i)
            j_indexes.append(i)
            i += 1
        address_index.update({f"{address}": []})
        for char in address:
            i_indexes = find_i_indexes(int(char), len(i_indexes), i_indexes)
            j_indexes = find_j_indexes(int(char), len(j_indexes), j_indexes)
        address_index[address].append(i_indexes[0])
        address_index[address].append(j_indexes[0])
    return address_index


def solve(json_str: str, resolution: int) -> imageType:
    bit_addresses: list[str] = []
    address_index: dict[str, list[list[int]]] = {}
    pic_arr:list[list[int]] = []
    fa = DFA.deserialize_json(json_str)
    global bit_address
    bit_address = ""
    create_bit_addresses(log2(resolution), bit_addresses)
    address_index = find_indexes(bit_addresses, resolution, address_index)
    for i in range(resolution):
        pic_arr.append([])
        for j in range(resolution):
            pic_arr[i].append(0)
    for address in address_index:
        state = fa.init_state
        for char in address:
            state = state.transitions[char]
        if fa.is_final(state):
            pic_arr[address_index[address][0]][address_index[address][1]] = 1
    return pic_arr


if __name__ == "__main__":
    pic_arr = solve(
        '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
        '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
        '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
        '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
        '"3": "q_4"}}',
        4
    )
    print(pic_arr)
