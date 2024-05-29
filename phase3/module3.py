import sys
sys.path.append('C:/Users/pc/Desktop/Project-Template-Nazarih')
from utils.utils import imageType
from phase0.FA_class import DFA
from phase2 import module2


def solve(json_fa_list: list[str], images: list[imageType]) -> list[int]:
    similar_dfa_index_list: list[int] = []
    similar_dfa_percentage_list: list[int] = []
    for image in images:
        similar_dfa_percentage_list.append(0)
        similar_dfa_index_list.append(0)
    for image in images:
        index = images.index(image)
        for dfa in json_fa_list:
            flag = module2.solve(dfa, image)
            if module2.percentage > similar_dfa_percentage_list[index]:
                similar_dfa_percentage_list[index] = module2.percentage
                similar_dfa_index_list[index] = json_fa_list.index(dfa)
    return similar_dfa_index_list


if __name__ == "__main__":
    print(
        solve(
            ['{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
            '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
            '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
            '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
            '"3": "q_4"}}'],
            [[[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]]
        )
    )
