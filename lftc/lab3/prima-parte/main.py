import sys
from automaton import Automaton

MENU = """
Meniu:
  1. Afișează multimea starilor
  2. Afișeaza alfabetul
  3. Afiseaza tranzitiile
  4. Afiseaza multimea starilor finale
  5. Verifica daca o secventa este acceptata (AFD)
  6. Determina cel mai lung prefix acceptat (AFD)
  7. Citeste automat din fisier
  8. Citeste automat de la tastatura (interactiv)
  0. Iesire
"""

def main() -> None:
    af = None  # Automaton

    while True:
        print(MENU)
        choice = input("Alege optiunea: ").strip()

        if choice == "0":
            print("La revedere!")
            return

        if choice == "7":
            path = input("Introduceti calea fișierului: ").strip()
            try:
                af = Automaton.from_file(path)
                print("Automat încarcat cu succes din fișier.")
                print(f"Determinist? {'DA' if af.is_deterministic() else 'NU'}")
            except Exception as e:
                print(f"Eroare la citire fișier: {e}")
            continue

        if choice == "8":
            try:
                af = Automaton.from_keyboard()
                print("Automat construit cu succes de la tastatura.")
                print(f"Determinist? {'DA' if af.is_deterministic() else 'NU'}")
            except Exception as e:
                print(f"Eroare la construcție: {e}")
            continue

        if af is None:
            print("Nu există un automat încărcat. Folosiți opțiunile 7 sau 8.")
            continue

        if choice == "1":
            print("Stari:", af.pretty_states())
        elif choice == "2":
            print("Alfabet:", af.pretty_alphabet())
        elif choice == "3":
            print("Tranzitii:\n" + af.pretty_transitions())
        elif choice == "4":
            print("Stari finale:", af.pretty_finals())
        elif choice == "5":
            seq = input("Introduceti secventa: ").strip()
            try:
                ok = af.accepts(seq)
                print(f"Secventa {'este' if ok else 'NU este'} acceptata.")
            except Exception as e:
                print(f"Eroare: {e}")
        elif choice == "6":
            seq = input("Introduceti secventa: ").strip()
            try:
                lp = af.longest_accepted_prefix(seq)
                if lp:
                    print(f"Cel mai lung prefix acceptat: '{lp}'")
                else:
                    print("Niciun prefix acceptat.")
            except Exception as e:
                print(f"Eroare: {e}")
        else:
            print("Optiune invalida. Reincercati.")


if __name__ == "__main__":
    main()