from typing import List, Optional, Tuple

from automaton import Automaton


class Token:
    """Reprezinta un token (atom lexical)"""

    def __init__(self, token_type: str, value: str, line: int, column: int):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.token_type}, '{self.value}', L{self.line}:C{self.column})"


class BSTNode:
    """Nod pentru arborele binar de cautare"""

    def __init__(self, symbol: str, position: int):
        self.symbol = symbol
        self.position = position
        self.left: Optional["BSTNode"] = None
        self.right: Optional["BSTNode"] = None


class SymbolTable:
    """Tabela de simboluri pentru identificatori si constante - implementare cu BST"""

    def __init__(self):
        self.root: Optional[BSTNode] = None
        self.next_pos = 0

    def add(self, symbol: str) -> int:
        """Adauga un simbol in tabela si returneaza pozitia lui"""
        if self.root is None:
            self.root = BSTNode(symbol, self.next_pos)
            self.next_pos += 1
            return self.root.position

        return self._add_recursive(self.root, symbol)

    def _add_recursive(self, node: BSTNode, symbol: str) -> int:
        """Adauga recursiv un simbol in BST"""
        if symbol == node.symbol:
            # Simbolul exista deja
            return node.position
        elif symbol < node.symbol:
            if node.left is None:
                node.left = BSTNode(symbol, self.next_pos)
                self.next_pos += 1
                return node.left.position
            else:
                return self._add_recursive(node.left, symbol)
        else:  # symbol > node.symbol
            if node.right is None:
                node.right = BSTNode(symbol, self.next_pos)
                self.next_pos += 1
                return node.right.position
            else:
                return self._add_recursive(node.right, symbol)

    def get_position(self, symbol: str) -> Optional[int]:
        """Returneaza pozitia unui simbol din tabela"""
        return self._search(self.root, symbol)

    def _search(self, node: Optional[BSTNode], symbol: str) -> Optional[int]:
        """Cauta recursiv un simbol in BST"""
        if node is None:
            return None
        if symbol == node.symbol:
            return node.position
        elif symbol < node.symbol:
            return self._search(node.left, symbol)
        else:
            return self._search(node.right, symbol)

    def _inorder_traversal(
        self, node: Optional[BSTNode], result: List[Tuple[str, int]]
    ):
        """Parcurgere inorder pentru a obtine simbolurile sortate"""
        if node is not None:
            self._inorder_traversal(node.left, result)
            result.append((node.symbol, node.position))
            self._inorder_traversal(node.right, result)

    def get_all_symbols(self) -> List[Tuple[str, int]]:
        """Returneaza toate simbolurile sortate alfabetic"""
        result: List[Tuple[str, int]] = []
        self._inorder_traversal(self.root, result)
        return result

    def __repr__(self):
        """Afiseaza simbolurile sortate dupa pozitie"""
        symbols = self.get_all_symbols()
        # Sortam dupa pozitie pentru afisare
        symbols_sorted = sorted(symbols, key=lambda x: x[1])
        return "\n".join(f"{pos}: {symbol}" for symbol, pos in symbols_sorted)


class LexicalAnalyzer:
    """Analizor lexical bazat pe automate finite"""

    def __init__(self):
        # Incarcam automatele finite
        self.afd_identifier = Automaton.from_file("afd_identifier.txt")
        self.afd_integer = Automaton.from_file("afd_integer.txt")
        self.afd_real = Automaton.from_file("afd_real.txt")

        # Tabele de simboluri
        self.symbol_table = SymbolTable()

        # Cuvinte cheie (specifice limbajului MLP)
        self.keywords = {
            "int",
            "float",
            "char",
            "string",
            "bool",
            "if",
            "else",
            "while",
            "for",
            "read",
            "write",
            "return",
            "void",
            "true",
            "false",
        }

        # Operatori si delimitatori
        self.operators = {
            "+",
            "-",
            "*",
            "/",
            "%",
            "=",
            "==",
            "!=",
            "<",
            ">",
            "<=",
            ">=",
            "&&",
            "||",
            "!",
        }

        self.delimiters = {
            "(",
            ")",
            "{",
            "}",
            "[",
            "]",
            ";",
            ",",
            ":",
        }

        # Coduri pentru FIP
        self.token_codes = {
            "KEYWORD": 1,
            "IDENTIFIER": 2,
            "CONSTANT_INT": 3,
            "CONSTANT_REAL": 4,
            "OPERATOR": 5,
            "DELIMITER": 6,
        }

        # FIP (Forma Interna a Programului)
        self.fip: List[Tuple[int, int]] = []

        # Erori
        self.errors: List[str] = []

    def is_whitespace(self, ch: str) -> bool:
        """Verifica daca caracterul este spatiu alb"""
        return ch in [" ", "\t", "\n", "\r"]

    def skip_whitespace(self, text: str, pos: int) -> int:
        """Sare peste spatiile albe"""
        while pos < len(text) and self.is_whitespace(text[pos]):
            pos += 1
        return pos

    def try_match_operator_or_delimiter(
        self, text: str, pos: int
    ) -> Optional[Tuple[str, int]]:
        """Incearca sa potriveasca un operator sau delimitator"""
        # Incercam operatori cu 2 caractere
        if pos + 1 < len(text):
            two_char = text[pos : pos + 2]
            if two_char in self.operators:
                return (two_char, pos + 2)

        # Incercam operatori/delimitatori cu 1 caracter
        if pos < len(text):
            one_char = text[pos]
            if one_char in self.operators or one_char in self.delimiters:
                return (one_char, pos + 1)

        return None

    def try_match_string_literal(
        self, text: str, pos: int
    ) -> Optional[Tuple[str, int]]:
        """Incearca sa potriveasca un string literal (intre ghilimele)"""
        if pos >= len(text) or text[pos] != '"':
            return None

        end_pos = pos + 1
        while end_pos < len(text):
            if text[end_pos] == '"':
                # Am gasit sfarsitul string-ului
                string_value = text[pos : end_pos + 1]
                return (string_value, end_pos + 1)
            elif text[end_pos] == "\\":
                # Escape sequence
                end_pos += 2
            else:
                end_pos += 1

        # String neterminat
        return None

    def try_match_char_literal(self, text: str, pos: int) -> Optional[Tuple[str, int]]:
        """Incearca sa potriveasca un char literal (intre apostroafe)"""
        if pos >= len(text) or text[pos] != "'":
            return None

        end_pos = pos + 1
        if end_pos >= len(text):
            return None

        # Escape sequence
        if text[end_pos] == "\\":
            end_pos += 1
            if end_pos >= len(text):
                return None

        end_pos += 1
        if end_pos < len(text) and text[end_pos] == "'":
            char_value = text[pos : end_pos + 1]
            return (char_value, end_pos + 1)

        return None

    def get_line_column(self, text: str, pos: int) -> Tuple[int, int]:
        """Calculeaza linia si coloana pentru o pozitie din text"""
        line = 1
        column = 1
        for i in range(pos):
            if text[i] == "\n":
                line += 1
                column = 1
            else:
                column += 1
        return (line, column)

    def analyze(self, text: str) -> Tuple[List[Token], SymbolTable, List[str]]:
        """
        Analizeaza textul si returneaza lista de tokeni, tabela de simboluri si erorile.
        """
        self.fip = []
        self.errors = []
        self.symbol_table = SymbolTable()
        tokens: List[Token] = []

        pos = 0
        while pos < len(text):
            # Sarim peste spatiile albe
            pos = self.skip_whitespace(text, pos)
            if pos >= len(text):
                break

            line, column = self.get_line_column(text, pos)

            # Incercam sa potrivim string literal
            string_match = self.try_match_string_literal(text, pos)
            if string_match:
                value, new_pos = string_match
                ts_pos = self.symbol_table.add(value)
                tokens.append(Token("CONSTANT_STRING", value, line, column))
                self.fip.append((self.token_codes["CONSTANT_INT"], ts_pos))
                pos = new_pos
                continue

            # Incercam sa potrivim char literal
            char_match = self.try_match_char_literal(text, pos)
            if char_match:
                value, new_pos = char_match
                ts_pos = self.symbol_table.add(value)
                tokens.append(Token("CONSTANT_CHAR", value, line, column))
                self.fip.append((self.token_codes["CONSTANT_INT"], ts_pos))
                pos = new_pos
                continue

            # Incercam sa potrivim operator sau delimitator
            op_delim_match = self.try_match_operator_or_delimiter(text, pos)
            if op_delim_match:
                value, new_pos = op_delim_match
                if value in self.operators:
                    tokens.append(Token("OPERATOR", value, line, column))
                    self.fip.append((self.token_codes["OPERATOR"], -1))
                else:
                    tokens.append(Token("DELIMITER", value, line, column))
                    self.fip.append((self.token_codes["DELIMITER"], -1))
                pos = new_pos
                continue

            # Incercam sa potrivim un numar real (trebuie inainte de integer!)
            real_prefix = self.afd_real.longest_accepted_prefix(text[pos:])
            if real_prefix:
                ts_pos = self.symbol_table.add(real_prefix)
                tokens.append(Token("CONSTANT_REAL", real_prefix, line, column))
                self.fip.append((self.token_codes["CONSTANT_REAL"], ts_pos))
                pos += len(real_prefix)
                continue

            # Incercam sa potrivim un numar intreg
            int_prefix = self.afd_integer.longest_accepted_prefix(text[pos:])
            if int_prefix:
                ts_pos = self.symbol_table.add(int_prefix)
                tokens.append(Token("CONSTANT_INT", int_prefix, line, column))
                self.fip.append((self.token_codes["CONSTANT_INT"], ts_pos))
                pos += len(int_prefix)
                continue

            # Incercam sa potrivim un identificator
            id_prefix = self.afd_identifier.longest_accepted_prefix(text[pos:])
            if id_prefix:
                # Verificam daca e cuvant cheie
                if id_prefix in self.keywords:
                    tokens.append(Token("KEYWORD", id_prefix, line, column))
                    self.fip.append((self.token_codes["KEYWORD"], -1))
                else:
                    ts_pos = self.symbol_table.add(id_prefix)
                    tokens.append(Token("IDENTIFIER", id_prefix, line, column))
                    self.fip.append((self.token_codes["IDENTIFIER"], ts_pos))
                pos += len(id_prefix)
                continue

            # Daca nu am potrivit nimic, avem o eroare lexicala
            error_msg = f"Eroare lexicala la linia {line}, coloana {column}: caracter invalid '{text[pos]}'"
            self.errors.append(error_msg)
            pos += 1

        return tokens, self.symbol_table, self.errors

    def print_fip(self):
        """Afiseaza FIP (Forma Interna a Programului)"""
        print("\n=== FIP (Forma Interna a Programului) ===")
        print(f"{'Cod Token':<15} {'Pozitie TS':<15}")
        print("-" * 30)
        for code, ts_pos in self.fip:
            ts_str = str(ts_pos) if ts_pos >= 0 else "-"
            print(f"{code:<15} {ts_str:<15}")

    def print_symbol_table(self):
        """Afiseaza tabela de simboluri"""
        print("\n=== Tabela de Simboluri (TS) ===")
        print(f"{'Pozitie':<10} {'Simbol':<30}")
        print("-" * 40)
        if self.symbol_table.root is not None:
            print(self.symbol_table)
        else:
            print("(vida)")

    def print_errors(self):
        """Afiseaza erorile lexicale"""
        if self.errors:
            print("\n=== ERORI LEXICALE ===")
            for error in self.errors:
                print(f"  {error}")
        else:
            print("\n=== Analiza lexicala reusita (fara erori) ===")

    def print_tokens(self, tokens: List[Token]):
        """Afiseaza lista de tokeni"""
        print("\n=== Lista de Tokeni ===")
        print(f"{'Tip':<20} {'Valoare':<30} {'Linie:Coloana':<15}")
        print("-" * 65)
        for token in tokens:
            print(
                f"{token.token_type:<20} {token.value:<30} {token.line}:{token.column}"
            )
