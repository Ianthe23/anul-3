from typing import Dict, Optional, Set, Tuple

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
            raise ValueError(
                f"Starea inițială '{self.initial_state}' nu există în 'states'."
            )
        if not self.final_states.issubset(self.states):
            raise ValueError("Unele stări finale nu există în 'states'.")

    @staticmethod
    def _strip_comments(text: str) -> str:
        """
        Elimina comentariile din text.
        Comentariile sunt linii care incep cu # si pana la sfarsitul liniei.
        """
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
        """
        Parseaza o multime de forma {a,b,c} si returneaza setul {a, b, c}.
        """
        body = body.strip()
        if body.startswith("{") and body.endswith("}"):
            inner = body[1:-1].strip()
            if not inner:
                return set()
            # allow items separated by commas and optional spaces
            return set([item.strip() for item in inner.split(",") if item.strip()])
        raise ValueError(f"Set invalid: {body}")

    @staticmethod
    def _find_section(text: str, keyword: str) -> Optional[str]:
        """
        Cauta sectiunea cu keyword-ul dat in text.
        Returneaza continutul sectiunii sau None daca nu gaseste.
        """
        lines = text.split("\n")
        keyword_lower = keyword.lower()

        for i, line in enumerate(lines):
            line_stripped = line.strip().lower()
            if line_stripped.startswith(keyword_lower):
                # Extragem partea dupa keyword
                rest = line.strip()[len(keyword) :].strip()
                return rest
        return None

    @staticmethod
    def _parse_transitions(text: str) -> Dict[Tuple[str, str], Set[str]]:
        """
        Parseaza tranzitiile din text.
        Format: (src,sym)->dest; sau (src,sym)->dest
        """
        transitions: Dict[Tuple[str, str], Set[str]] = {}

        # Gasim linia cu "transitions"
        lines = text.split("\n")
        trans_start = -1
        for i, line in enumerate(lines):
            if line.strip().lower().startswith("transitions"):
                trans_start = i + 1
                break

        if trans_start == -1:
            raise ValueError("Nu s-a gasit sectiunea 'transitions'")

        # Parsam fiecare tranzitie
        for i in range(trans_start, len(lines)):
            line = lines[i].strip()
            if not line:
                continue

            # Cautam pattern (src,sym)->dest
            if "(" not in line or ")" not in line or "->" not in line:
                continue

            # Extragem sursa si simbolul
            paren_start = line.find("(")
            paren_end = line.find(")")
            if paren_start == -1 or paren_end == -1:
                continue

            inside_paren = line[paren_start + 1 : paren_end]
            parts = inside_paren.split(",")
            if len(parts) != 2:
                continue

            src = parts[0].strip()
            sym = parts[1].strip()

            # Extragem destinatia
            arrow_pos = line.find("->", paren_end)
            if arrow_pos == -1:
                continue

            after_arrow = line[arrow_pos + 2 :].strip()
            # Eliminam ; daca exista
            if after_arrow.endswith(";"):
                after_arrow = after_arrow[:-1].strip()

            dest = after_arrow

            if not src or not sym or not dest:
                continue

            # Adaugam tranzitia
            key = (src, sym)
            transitions.setdefault(key, set()).add(dest)

        return transitions

    @classmethod
    def from_text(cls, text: str) -> "Automaton":
        """
        Parseaza automatul din text folosind parsing manual (fara regex).
        """
        text = cls._strip_comments(text)

        # Gasim sectiunile
        states_str = cls._find_section(text, "states")
        alphabet_str = cls._find_section(text, "alphabet")
        initial_str = cls._find_section(text, "initial")
        final_str = cls._find_section(text, "final")

        if not (states_str and alphabet_str and initial_str and final_str):
            raise ValueError(
                "Fisier incomplet. Sectiuni necesare: states, alphabet, initial, final, transitions."
            )

        # Parse sections
        states = cls._parse_set(states_str)
        alphabet = cls._parse_set(alphabet_str)
        initial = initial_str.strip()
        final_states = cls._parse_set(final_str)

        # Parse transitions
        transitions = cls._parse_transitions(text)

        # Validam tranzitiile
        for (src, sym), dests in transitions.items():
            if src not in states:
                raise ValueError(f"Starea sursa '{src}' nu exista in 'states'")
            for dest in dests:
                if dest not in states:
                    raise ValueError(
                        f"Starea destinatie '{dest}' nu exista in 'states'"
                    )
            if sym != EPSILON and sym not in alphabet:
                raise ValueError(f"Simbolul '{sym}' nu exista in alfabet.")

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

        print(
            "Introduceti alfabetul, simboluri de 1 caracter sau 'epsilon', separate prin virgule (ex: 0,1,a,b):"
        )
        alpha_in = input("> ").strip()
        alphabet = set(
            s.strip() for s in alpha_in.split(",") if s.strip() and s.strip() != EPSILON
        )

        print("Introduceti starea initiala:")
        initial = input("> ").strip()
        if initial not in states:
            raise ValueError("Starea initiala nu exista in multimea de stari.")

        print(
            "Introduceti multimea de stari finale, separate prin virgule (ex: q1,q2):"
        )
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
        print(
            "Introduceti fiecare tranzitie pe o linie: <sursa> <simbol|epsilon> <destinatie>"
        )
        for i in range(n):
            line = input(f"t{i + 1}> ").strip()
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(
                    "Format tranzitie invalid. Asteptat: <sursa> <simbol|epsilon> <destinatie>"
                )
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

    # Pentru DFA, calculeaza starea urmatoare pentru o tranzitie.
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
            # determinist => o singura dest
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
