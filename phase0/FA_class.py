import json


class State:
    __counter = 0

    def __init__(self, id: None) -> None:
        if id is None:
            self.id = State._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, State] = {}

    def add_transition(self, symbol: str, state: 'State') -> None:
        self.transitions[symbol] = state

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id


class DFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list[State] = []
        self.alphabet: list[str] = []
        self.final_states: list[State] = []

    @staticmethod
    def deserialize_json(json_str: str) -> 'DFA':
        fa = DFA()
        json_fa = json.loads(json_str)

        fa.alphabet = json_fa["alphabet"]

        for state_str in json_fa["states"]:
            fa.add_state(int(state_str[2:]))

        fa.init_state = fa.get_state_by_id(int(json_fa["initial_state"][2:]))

        for final_str in json_fa["final_states"]:
            fa.add_final_state(fa.get_state_by_id(int(final_str[2:])))

        for state_str in json_fa["states"]:
            for symbol in fa.alphabet:
                fa.add_transition(fa.get_state_by_id(int(state_str[2:])), fa.get_state_by_id(int(json_fa[state_str][symbol][2:])), symbol)

        return fa

    def serialize_json(self) -> str:
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
            "alphabet": self.alphabet
        }

        for state in self.states:
            fa[f"q_{state.id}"] = {}
            for symbol in self.alphabet:
                fa[f"q_{state.id}"][symbol] = f"q_{state.transitions[symbol].id}"

        return json.dumps(fa)

    def add_state(self, id: int | None = None) -> None:
        self.states.append(State(id))

    def add_transition(self, from_state: State, to_state: State, input_symbol: str) -> None:
        from_state.add_transition(input_symbol, to_state)

    def assign_initial_state(self, state: State) -> None:
        self.init_state = state

    def add_final_state(self, state: State) -> None:
        self.final_states.append(state)

    def get_state_by_id(self, id: int) -> State:
        for state in self.states:
            if state.id == id:
                return state

    def is_final(self, state: State) -> bool:
        return state in self.final_states



class NFAState:
    __counter = 0

    def __init__(self, id: None) -> None:
        if id is None:
            self.id = NFAState._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, list(NFAState)] = {}

    def add_transition(self, symbol: str, state: 'NFAState') -> None:
        self.transitions[symbol].append(state)

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id


class NFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list[NFAState] = []
        self.alphabet: list[str] = []
        self.final_states: list[NFAState] = []

    @staticmethod
    def convert_DFA_instanse_to_NFA_instanse(dfa_machine: DFA) -> 'NFA':
        fa = NFA()
        fa.alphabet.append("λ")
        fa.alphabet = fa.alphabet + dfa_machine.alphabet
        for _ in range(dfa_machine.states.count):
            fa.states.append(NFAState(None))
        fa.init_state = fa.states[dfa_machine.states.index(dfa_machine.init_state)]
        for final_state in dfa_machine.final_states:
            fa.final_states.append(fa.states[dfa_machine.states.index(final_state)])
        for state in dfa_machine.states:
            for symbol in fa.alphabet:
                if symbol != "λ":
                    fa.states[dfa_machine.states.index(state)].add_transition(symbol, fa.states[dfa_machine.states.index(state.transitions[symbol])])
        return fa

    @staticmethod
    def union(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        fa = NFA()
        fa.alphabet = set(machine1.alphabet + machine2.alphabet)
        for _ in range(machine1.states.count + machine2.states.count + 2):
            fa.states.append(NFAState(None))
        i = 1
        for state in machine1.states:
            for symbol in state.transitions.keys():
                for to_state in state.transitions[symbol]:
                    fa.states[i].add_transition(symbol, fa.states[machine1.states.index(to_state) + 1])
            i += 1
        for state in machine2.states:
            for symbol in state.transitions.keys():
                for to_state in state.transitions[symbol]:
                    fa.states[i].add_transition(symbol, fa.states[machine2.states.index(to_state) + machine1.states.count + 1])
            i += 1
        fa.init_state = fa.states[0]
        fa.final_states.append(fa.states[machine1.states.count + machine2.states.count + 1])
        fa.states[0].add_transition("λ", fa.states[machine1.states.index(machine1.init_state) + 1])
        fa.states[0].add_transition("λ", fa.states[machine2.states.index(machine2.init_state) + machine1.states.count + 1])
        for final_state in machine1.final_states:
            fa.states[machine1.states.index(final_state) + 1].add_transition("λ", fa.states[machine1.states.count + machine2.states.count + 1])
        for final_state in machine2.final_states:
            fa.states[machine2.states.index(final_state) + machine1.states.count + 1].add_transition("λ", fa.states[machine1.states.count + machine2.states.count + 1])
        return fa

    @staticmethod
    def concat(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        fa = NFA()
        fa.alphabet = set(machine1.alphabet + machine2.alphabet)
        for _ in range(machine1.states.count + machine2.states.count + 1):
            fa.states.append(NFAState(None))
        i = 0
        for state in machine1.states:
            for symbol in state.transitions.keys():
                for to_state in state.transitions[symbol]:
                    fa.states[i].add_transition(symbol, fa.states[machine1.states.index(to_state)])
            i += 1
        for state in machine2.states:
            for symbol in state.transitions.keys():
                for to_state in state.transitions[symbol]:
                    fa.states[i].add_transition(symbol, fa.states[machine2.states.index(to_state) + machine1.states.count])
            i += 1
        fa.init_state = fa.states[machine1.states.index(machine1.init_state)]
        fa.final_states.append(fa.states[machine1.states.count + machine2.states.count])
        for final_state in machine1.final_states:
            fa.states[machine1.states.index(final_state)].add_transition("λ", fa.states[machine2.states.index(machine2.init_state) + machine1.states.count])
        for final_state in machine2.final_states:
            fa.states[machine2.states.index(final_state) + machine1.states.count].add_transition("λ", fa.states[machine1.states.count + machine2.states.count])
        return fa

    @staticmethod
    def star(machine: 'NFA') -> 'NFA':
        fa = NFA()
        fa.alphabet = machine.alphabet
        for _ in range(machine.states.count + 2):
            fa.states.append(NFAState(None))
        i = 1
        for state in machine.states:
            for symbol in state.transitions.keys():
                for to_state in state.transitions[symbol]:
                    fa.states[i].add_transition(symbol, fa.states[machine.states.index(to_state) + 1])
            i += 1
        fa.init_state = fa.states[0]
        fa.final_states.append(fa.states[machine.states.count + 1])
        fa.states[0].add_transition("λ", fa.states[machine.states.index(machine.init_state) + 1])
        fa.states[0].add_transition("λ", fa.states[machine.states.count + 1])
        fa.states[machine.states.count + 1].add_transition("λ", fa.states[0])
        for final_state in machine.final_states:
            fa.states[machine.states.index(final_state) + 1].add_transition("λ", fa.states[machine.states.count + 1])
        return fa

    def serialize_to_json(self) -> str:
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
            "alphabet": self.alphabet
        }

        for state in self.states:
            if state.transitions:
                fa[f"q_{state.id}"] = {}
                for symbol in state.transitions.keys():
                    for to_state in state.transitions[symbol]:
                        fa[f"q_{state.id}"][symbol] = f"q_{to_state.id}"

        return json.dumps(fa)
