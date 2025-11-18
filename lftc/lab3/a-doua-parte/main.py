#!/usr/bin/env python3
"""
Program de analiza lexicala folosind automate finite deterministe (AFD)

Acest program foloseste automate finite pentru recunoasterea atomilor lexicali:
- AFD pentru identificatori
- AFD pentru constante intregi (bazat pe literalele C/C++)
- AFD pentru constante numere reale

Rezultate:
- FIP (Forma Interna a Programului)
- TS (Tabela de Simboluri)
- Raportarea erorilor lexicale

Observatii:
- NU se folosesc expresii regulare
- Spatiile NU sunt obligatorii pentru separare (ca in limbajele reale)
"""

import sys

from lexical_analyzer import LexicalAnalyzer


def print_menu():
    """Afiseaza meniul principal"""
    print("\n" + "=" * 60)
    print("ANALIZOR LEXICAL BAZAT PE AUTOMATE FINITE")
    print("=" * 60)
    print("1. Analizeaza fisier")
    print("2. Analizeaza text introdus de la tastatura")
    print("3. Afiseaza informatii despre automate")
    print("0. Iesire")
    print("=" * 60)


def analyze_file(analyzer: LexicalAnalyzer):
    """Analizeaza continutul unui fisier"""
    file_path = input("Introduceti calea fisierului: ").strip()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        print(f"\n>>> Analizam fisierul: {file_path}")
        print(f">>> Continut ({len(text)} caractere):")
        print("-" * 60)
        print(text)
        print("-" * 60)

        tokens, symbol_table, errors = analyzer.analyze(text)

        # Afisam rezultatele
        analyzer.print_tokens(tokens)
        analyzer.print_fip()
        analyzer.print_symbol_table()
        analyzer.print_errors()

        # Salvam rezultatele in fisiere
        base_name = file_path.rsplit(".", 1)[0]
        save_results(base_name, analyzer, tokens)

    except FileNotFoundError:
        print(f"Eroare: Fisierul '{file_path}' nu a fost gasit!")
    except Exception as e:
        print(f"Eroare la citirea fisierului: {e}")


def analyze_keyboard(analyzer: LexicalAnalyzer):
    """Analizeaza text introdus de la tastatura"""
    print("\nIntroduceti textul de analizat (terminati cu o linie vida):")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    text = "\n".join(lines)

    print("\n>>> Analizam textul introdus:")
    print("-" * 60)
    print(text)
    print("-" * 60)

    tokens, symbol_table, errors = analyzer.analyze(text)

    # Afisam rezultatele
    analyzer.print_tokens(tokens)
    analyzer.print_fip()
    analyzer.print_symbol_table()
    analyzer.print_errors()


def show_automata_info(analyzer: LexicalAnalyzer):
    """Afiseaza informatii despre automatele folosite"""
    print("\n=== INFORMATII DESPRE AUTOMATE ===\n")

    print("1. AFD pentru IDENTIFICATORI:")
    print(f"   - Stari: {analyzer.afd_identifier.pretty_states()}")
    print(f"   - Stare initiala: {analyzer.afd_identifier.initial_state}")
    print(f"   - Stari finale: {analyzer.afd_identifier.pretty_finals()}")
    print(
        f"   - Determinist: {'DA' if analyzer.afd_identifier.is_deterministic() else 'NU'}"
    )
    print(f"   - Pattern: [a-zA-Z_][a-zA-Z0-9_]*")

    print("\n2. AFD pentru CONSTANTE INTREGI:")
    print(f"   - Stari: {analyzer.afd_integer.pretty_states()}")
    print(f"   - Stare initiala: {analyzer.afd_integer.initial_state}")
    print(f"   - Stari finale: {analyzer.afd_integer.pretty_finals()}")
    print(
        f"   - Determinist: {'DA' if analyzer.afd_integer.is_deterministic() else 'NU'}"
    )
    print(f"   - Accepta: literale intregi C/C++ (decimal, octal, hex, binar)")
    print(f"   - Sursa: https://en.cppreference.com/w/cpp/language/integer_literal")

    print("\n3. AFD pentru CONSTANTE REALE:")
    print(f"   - Stari: {analyzer.afd_real.pretty_states()}")
    print(f"   - Stare initiala: {analyzer.afd_real.initial_state}")
    print(f"   - Stari finale: {analyzer.afd_real.pretty_finals()}")
    print(f"   - Determinist: {'DA' if analyzer.afd_real.is_deterministic() else 'NU'}")
    print(f"   - Pattern: [0-9]+\\.[0-9]+([eE][+-]?[0-9]+)?[fFlL]?")

    print("\n4. CUVINTE CHEIE:")
    print(f"   {', '.join(sorted(analyzer.keywords))}")

    print("\n5. OPERATORI:")
    print(f"   {', '.join(sorted(analyzer.operators))}")

    print("\n6. DELIMITATORI:")
    print(f"   {', '.join(sorted(analyzer.delimiters))}")


def save_results(base_name: str, analyzer: LexicalAnalyzer, tokens):
    """Salveaza rezultatele in fisiere"""
    # Salvam FIP
    fip_file = f"{base_name}_fip.txt"
    with open(fip_file, "w", encoding="utf-8") as f:
        f.write("FIP (Forma Interna a Programului)\n")
        f.write("=" * 40 + "\n")
        f.write(f"{'Cod Token':<15} {'Pozitie TS':<15}\n")
        f.write("-" * 30 + "\n")
        for code, ts_pos in analyzer.fip:
            ts_str = str(ts_pos) if ts_pos >= 0 else "-"
            f.write(f"{code:<15} {ts_str:<15}\n")
    print(f"\n>>> FIP salvat in: {fip_file}")

    # Salvam TS
    ts_file = f"{base_name}_ts.txt"
    with open(ts_file, "w", encoding="utf-8") as f:
        f.write("Tabela de Simboluri (TS)\n")
        f.write("=" * 40 + "\n")
        f.write(f"{'Pozitie':<10} {'Simbol':<30}\n")
        f.write("-" * 40 + "\n")
        if analyzer.symbol_table.root is not None:
            f.write(str(analyzer.symbol_table) + "\n")
        else:
            f.write("(vida)\n")
    print(f">>> TS salvata in: {ts_file}")

    # Salvam tokenii
    tokens_file = f"{base_name}_tokens.txt"
    with open(tokens_file, "w", encoding="utf-8") as f:
        f.write("Lista de Tokeni\n")
        f.write("=" * 65 + "\n")
        f.write(f"{'Tip':<20} {'Valoare':<30} {'Linie:Coloana':<15}\n")
        f.write("-" * 65 + "\n")
        for token in tokens:
            f.write(
                f"{token.token_type:<20} {token.value:<30} {token.line}:{token.column}\n"
            )
    print(f">>> Tokeni salvati in: {tokens_file}")

    # Salvam erorile (daca exista)
    if analyzer.errors:
        errors_file = f"{base_name}_errors.txt"
        with open(errors_file, "w", encoding="utf-8") as f:
            f.write("Erori Lexicale\n")
            f.write("=" * 60 + "\n")
            for error in analyzer.errors:
                f.write(error + "\n")
        print(f">>> Erori salvate in: {errors_file}")


def main():
    """Functia principala"""
    print("\n" + "=" * 60)
    print("Incarcare automate finite...")
    print("=" * 60)

    try:
        analyzer = LexicalAnalyzer()
        print("✓ AFD pentru identificatori incarcata")
        print("✓ AFD pentru constante intregi incarcata")
        print("✓ AFD pentru constante reale incarcata")
    except Exception as e:
        print(f"\nEroare la incarcarea automatelor: {e}")
        print("\nAsigurati-va ca fisierele urmatoare exista:")
        print("  - afd_identifier.txt")
        print("  - afd_integer.txt")
        print("  - afd_real.txt")
        sys.exit(1)

    while True:
        print_menu()
        choice = input("\nAlege optiunea: ").strip()

        if choice == "0":
            print("\nLa revedere!")
            break
        elif choice == "1":
            analyze_file(analyzer)
        elif choice == "2":
            analyze_keyboard(analyzer)
        elif choice == "3":
            show_automata_info(analyzer)
        else:
            print("Optiune invalida! Te rog alege 0, 1, 2 sau 3.")


if __name__ == "__main__":
    main()
