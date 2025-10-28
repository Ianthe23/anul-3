from typing import Dict, Set, Tuple, Optional
import re

EPSILON = "epsilon"


class Automaton:
    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[Tuple[str, str], Set[str]],
        initial_state: str,
        final_states: Set[str],
    ):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = {}
        # Normalize transitions to sets
        for (src, sym), dests in transitions.items():
            self.transitions[(src, sym)] = set(dests)
        self.initial_state = initial_state
        self.final_states = set(final_states)

        # Basic validation
        if self.initial_state not in self.states:
            raise ValueError(f"Starea inițială '{self.initial_state}' nu există în 'states'.")
        if not self.final_states.issubset(self.states):
            raise ValueError("Unele stări finale nu există în 'states'.")

    @staticmethod
    def _strip_comments(text: str) -> str:
        lines = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # strip inline comments after '#'
            idx = line.find("#")
            if idx != -1:
                line = line[:idx].strip()
            if line:
                lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def _parse_set(body: str) -> Set[str]:
        body = body.strip()
        if body.startswith("{") and body.endswith("}"):
            inner = body[1:-1].strip()
            if not inner:
                return set()
            # allow items separated by commas and optional spaces
            return set([item.strip() for item in inner.split(",") if item.strip()])
        raise ValueError(f"Set invalid: {body}")

    @classmethod
    def from_text(cls, text: str) -> "Automaton":
        """
        Așteapta formatul EBNF descris mai sus.
        Exemple tranzitii:
          (q0,0)->q1;
          (q1,epsilon)->q2;
        """
        text = cls._strip_comments(text)

        # Match sections with regex
        def search_section(name: str, pattern: str) -> Optional[re.Match]:
            return re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)

        m_states = search_section("states", r"states\s*({[^}]*})")
        m_alphabet = search_section("alphabet", r"alphabet\s*({[^}]*})")
        m_initial = search_section("initial", r"initial\s*([A-Za-z0-9_]+)")
        m_final = search_section("final", r"final\s*({[^}]*})")
        m_transitions = search_section("transitions", r"transitions\s*(.*)")

        if not (m_states and m_alphabet and m_initial and m_final and m_transitions):
            raise ValueError("Fisier incomplet. Sectiuni necesare: states, alphabet, initial, final, transitions.")

        states = cls._parse_set(m_states.group(1))
        alphabet = cls._parse_set(m_alphabet.group(1))
        initial = m_initial.group(1).strip()
        final_states = cls._parse_set(m_final.group(1))

        transitions_block = m_transitions.group(1)
        # Extract transition lines until end of string
        # Pattern: (src,sym)->dest;
        trans_pattern = re.compile(
            r"\(\s*([A-Za-z0-9_]+)\s*,\s*([A-Za-z0-9_]|epsilon)\s*\)\s*->\s*([A-Za-z0-9_]+)\s*;?",
            flags=re.IGNORECASE,
        )

        transitions: Dict[Tuple[str, str], Set[str]] = {}
        for match in trans_pattern.finditer(transitions_block):
            src = match.group(1)
            sym = match.group(2)
            dest = match.group(3)
            if src not in states or dest not in states:
                raise ValueError(f"Stari in tranzitie necunoscute: ({src}, {sym}) -> {dest}")

            # epsilon poate fi în NFA; pentru DFA nu trebuie sa apara
            if sym != EPSILON and sym not in alphabet:
                raise ValueError(f"Simbolul '{sym}' nu exista in alfabet.")

            key = (src, sym)
            transitions.setdefault(key, set()).add(dest)

        return cls(states, alphabet, transitions, initial, final_states)

    @classmethod
    def from_file(cls, path: str) -> "Automaton":
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return cls.from_text(content)

    @classmethod
    def from_keyboard(cls) -> "Automaton":
        """
        Varianta interactiva (prompturi separate). Accepta NFA via 'epsilon' in tranzitii.
        """
        print("Introduceti multimea de stari, separate prin virgule (ex: q0,q1,q2):")
        states_in = input("> ").strip()
        states = set(s.strip() for s in states_in.split(",") if s.strip())

        print("Introduceti alfabetul, simboluri de 1 caracter sau 'epsilon', separate prin virgule (ex: 0,1,a,b):")
        alpha_in = input("> ").strip()
        alphabet = set(s.strip() for s in alpha_in.split(",") if s.strip() and s.strip() != EPSILON)

        print("Introduceti starea initiala:")
        initial = input("> ").strip()
        if initial not in states:
            raise ValueError("Starea initiala nu exista in multimea de stari.")

        print("Introduceti multimea de stari finale, separate prin virgule (ex: q1,q2):")
        finals_in = input("> ").strip()
        finals = set(s.strip() for s in finals_in.split(",") if s.strip())
        if not finals.issubset(states):
            raise ValueError("Unele stari finale nu exista in multimea de stari.")

        print("Introduceti numarul de tranzitii:")
        try:
            n = int(input("> ").strip())
        except ValueError:
            raise ValueError("Număr de tranzitii invalid.")

        transitions: Dict[Tuple[str, str], Set[str]] = {}
        print("Introduceti fiecare tranzitie pe o linie: <sursa> <simbol|epsilon> <destinatie>")
        for i in range(n):
            line = input(f"t{i + 1}> ").strip()
            parts = line.split()
            if len(parts) != 3:
                raise ValueError("Format tranzitie invalid. Asteptat: <sursa> <simbol|epsilon> <destinatie>")
            src, sym, dest = parts
            if src not in states or dest not in states:
                raise ValueError("Stari necunoscute in tranzitie.")
            if sym != EPSILON and (len(sym) != 1 or sym not in alphabet):
                raise ValueError("Simbol invalid (nu e in alfabet) sau lungime != 1.")
            transitions.setdefault((src, sym), set()).add(dest)

        return cls(states, alphabet, transitions, initial, finals)

    def is_deterministic(self) -> bool:
        # Nu permite epsilon in DFA si toate tranzitiile au cel mult o destinatie.
        for (src, sym), dests in self.transitions.items():
            if sym == EPSILON:
                return False
            if len(dests) > 1:
                return False
        return True

    def next_states(self, state: str, symbol: str) -> Set[str]:
        return self.transitions.get((state, symbol), set())

    def accepts(self, sequence: str) -> bool:
        """
        Doar pentru DFA (altfel arunca ValueError). Lipsa tranzitiei => respinge.
        """
        if not self.is_deterministic():
            raise ValueError("Automatul nu este determinist.")
        current = self.initial_state
        for ch in sequence:
            if ch not in self.alphabet:
                return False
            dests = self.next_states(current, ch)
            if not dests:
                return False
            # determinist => un singur dest
            current = next(iter(dests))
        return current in self.final_states

    def longest_accepted_prefix(self, sequence: str) -> str:
        """
        Doar pentru DFA. Intoarce cel mai lung prefix al secventei care este acceptat.
        """
        if not self.is_deterministic():
            raise ValueError("Automatul nu este determinist.")
        current = self.initial_state
        last_accept_idx = -1
        for idx, ch in enumerate(sequence):
            if ch not in self.alphabet:
                break
            dests = self.next_states(current, ch)
            if not dests:
                break
            current = next(iter(dests))
            if current in self.final_states:
                last_accept_idx = idx
        if last_accept_idx >= 0:
            return sequence[: last_accept_idx + 1]
        return ""

    def pretty_states(self) -> str:
        return "{" + ", ".join(sorted(self.states)) + "}"

    def pretty_alphabet(self) -> str:
        return "{" + ", ".join(sorted(self.alphabet)) + "}"

    def pretty_finals(self) -> str:
        return "{" + ", ".join(sorted(self.final_states)) + "}"

    def pretty_transitions(self) -> str:
        items = []
        for (src, sym), dests in sorted(self.transitions.items()):
            for d in sorted(dests):
                items.append(f"({src},{sym})->{d}")
        return "\n".join(items)