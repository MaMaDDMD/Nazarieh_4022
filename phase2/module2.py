import sys
sys.path.append('C:/Users/pc/Desktop/Project-Template-Nazarih')
from phase0.FA_class import DFA
from phase1 import module1
from utils import utils
from utils.utils import imageType
import math


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


def solve(json_str: str, image: imageType) -> bool:
    flag = True
    fa1 = DFA.deserialize_json(json_str)
    fa2 = module1.solve(image)
    bit_addresses: list[str] = []
    global bit_address
    bit_address = ""
    create_bit_addresses(math.log(len(image), 2), bit_addresses)
    counter = 0
    for address in bit_addresses:
        state1 = fa1.init_state
        state2 = fa2.init_state
        for char in address:
            state1 = state1.transitions[char]
            state2 = state2.transitions[char]
        if fa1.is_final(state1) == fa2.is_final(state2):
            counter += 1
        else:
            flag = False
    global percentage
    percentage = int(counter * 100.0 / len(bit_addresses))
    return flag


if __name__ == "__main__":
    print(
        solve(
            '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
            '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
            '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
            '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
            '"3": "q_4"}}',
            [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]
        )
    )
