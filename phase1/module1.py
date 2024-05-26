import sys
sys.path.append('C:/Users/pc/Desktop/Project-Template-Nazarih')
from phase0.FA_class import DFA, State
from visualization import visualizer
from utils import utils
from utils.utils import imageType



def check_one_or_zero(matrix: imageType) -> int:
    x = matrix[0][0]
    for line in matrix:
        for col in line:
            if(col != x):
                return -1
    return x


def solve(image: imageType) -> DFA:
    fa = DFA()
    fa.alphabet = ["0", "1", "2", "3"]
    i = 0
    j = 0
    trap = State(None)
    final = State(None)
    for c in range(4):
        trap.add_transition(f"{c}", trap)
        final.add_transition(f"{c}", final)
    flag = True
    state_image: dict[State, list[list[int]]] = {}
    fa.states.append(State(None))
    state_image.update({fa.states[0]: image})
    check = check_one_or_zero(image)
    if check == 0:
        fa.states.remove(fa.states[0])
        fa.states.append(final)
        fa.init_state = final
        fa.add_final_state(final)
        flag = False
    elif check == 1:
        fa.states.remove(fa.states[0])
        fa.states.append(trap)
        fa.init_state = trap
        flag = False
    while(flag):
        for state in fa.states:
            for k in range(4):
                image_arr: list[list[int]] = []
                if k == 0:
                    length = len(state_image[state])
                    l = 0
                    m = 0
                    while(l < length / 2):
                        image_arr.append([])
                        while(m < length / 2):
                            image_arr[len(image_arr) - 1].append(state_image[state][l][m])
                            m += 1
                        l += 1
                        m = 0
                if k == 1:
                    length = len(state_image[state])
                    l = 0
                    m = int(length / 2)
                    while(l < length / 2):
                        image_arr.append([])
                        while(m < length):
                            image_arr[len(image_arr) - 1].append(state_image[state][l][m])
                            m += 1
                        l += 1
                        m = int(length / 2)
                if k == 2:
                    length = len(state_image[state])
                    l = int(length / 2)
                    m = 0
                    while(l < length):
                        image_arr.append([])
                        while(m < length / 2):
                            image_arr[len(image_arr) - 1].append(state_image[state][l][m])
                            m += 1
                        l += 1
                        m = 0
                if k == 3:
                    length = len(state_image[state])
                    l = int(length / 2)
                    m = int(length / 2)
                    while(l < length):
                        image_arr.append([])
                        while(m < length):
                            image_arr[len(image_arr) - 1].append(state_image[state][l][m])
                            m += 1
                        l += 1
                        m = int(length / 2)
                check = check_one_or_zero(image_arr)
                if check == 1:
                    state.add_transition(f"{k}", trap)
                elif check == 0:
                    state.add_transition(f"{k}", final)
                else:
                    j += 1
                    fa.states.append(State(None))
                    state_image.update({fa.states[len(fa.states) - 1]: image_arr})
                    state.add_transition(f"{k}", fa.states[len(fa.states) - 1])
            if i == j:
                break
            else:
                i += 1
        flag = False
    fa.states.append(trap)
    fa.states.append(final)
    fa.init_state = fa.states[0]
    fa.final_states.append(final)
    return fa


if __name__ == "__main__":
    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]

    utils.save_image(image)
    fa = solve(image)
    print(fa.serialize_json())
    visualizer.visualize(fa.serialize_json())
