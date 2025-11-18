# Analizor Lexical Bazat pe Automate Finite

## Descriere

Acest program implementează un analizor lexical complet pentru un Mini Limbaj de Programare (MLP) folosind **automate finite deterministe (AFD)** pentru recunoașterea atomilor lexicali.

## Caracteristici

- **NU folosește expresii regulare** - toată recunoașterea se face prin automate finite
- **Spațiile nu sunt obligatorii** pentru separare (ca în limbajele de programare reale)
- Generează **FIP** (Forma Internă a Programului)
- Generează **TS** (Tabela de Simboluri)
- **Raportează erori lexicale** cu linie și coloană

## Automate Finite Implementate

### 1. AFD pentru Identificatori (`afd_identifier.txt`)
- **Pattern**: `[a-zA-Z_][a-zA-Z0-9_]*`
- Începe cu literă sau underscore
- Continuă cu litere, cifre sau underscore
- **Stări**: 2 (q0 - start, q1 - acceptare)

### 2. AFD pentru Constante Întregi (`afd_integer.txt`)
- **Sursă documentație**: [C++ Integer Literals](https://en.cppreference.com/w/cpp/language/integer_literal)
- Acceptă următoarele formate:
  - **Decimal**: `123`, `456`
  - **Hexazecimal**: `0xFF`, `0xDEADBEEF`
  - **Octal**: `0755`, `0644`
  - **Binar**: `0b1010`, `0b11010110`
  - **Cu sufixe**: `123u`, `456L`, `789ULL`, etc.
- **Stări**: 13 (pentru diferite baze și sufixe)

### 3. AFD pentru Constante Reale (`afd_real.txt`)
- **Pattern**: `[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?[fFlL]?`
- Acceptă următoarele formate:
  - **Simple**: `3.14`, `2.718`
  - **Științifice**: `1.23e-4`, `5.67E+8`
  - **Cu sufixe**: `3.14f`, `2.5L`
- **Stări**: 8 (pentru parte întreagă, fracționară, exponent, sufix)

## Structura Proiectului

```
a-doua-parte/
├── automaton.py           # Clasa Automaton (fără regex!)
├── lexical_analyzer.py    # Analizorul lexical principal
├── main.py               # Program principal cu meniu
├── afd_identifier.txt    # AFD pentru identificatori
├── afd_integer.txt       # AFD pentru constante întregi
├── afd_real.txt          # AFD pentru constante reale
├── test_program.txt      # Program de test simplu
├── test_complex.txt      # Program de test complex
├── test_errors.txt       # Program cu erori lexicale
└── README.md             # Acest fișier
```

## Utilizare

### 1. Rulare Program

```bash
python3 main.py
```

### 2. Meniu Principal

```
1. Analizeaza fisier
2. Analizeaza text introdus de la tastatura
3. Afiseaza informatii despre automate
0. Iesire
```

### 3. Exemplu Analiză Fișier

```bash
$ python3 main.py
# Alegeți opțiunea 1
# Introduceți: test_program.txt
```

### 4. Rezultate Generate

Pentru fișierul `test_program.txt`, se generează:
- `test_program_fip.txt` - Forma Internă a Programului
- `test_program_ts.txt` - Tabela de Simboluri
- `test_program_tokens.txt` - Lista completă de tokeni
- `test_program_errors.txt` - Erori (dacă există)

## Format FIP (Forma Internă a Programului)

FIP conține perechi `(cod_token, pozitie_ts)`:

| Cod Token | Semnificație | Poziție TS |
|-----------|--------------|------------|
| 1 | KEYWORD | -1 (nu se pune în TS) |
| 2 | IDENTIFIER | poziția în TS |
| 3 | CONSTANT_INT | poziția în TS |
| 4 | CONSTANT_REAL | poziția în TS |
| 5 | OPERATOR | -1 |
| 6 | DELIMITER | -1 |

## Format Tabela de Simboluri (TS)

TS conține identificatori și constante cu poziții unice:

```
Pozitie    Simbol
0          x
1          123
2          y
3          3.14
...
```

## Cuvinte Cheie Recunoscute

```
int, float, char, string, bool, if, else, while, for, 
read, write, return, void, true, false
```

## Operatori Recunoscuți

```
+, -, *, /, %, =, ==, !=, <, >, <=, >=, &&, ||, !
```

## Delimitatori Recunoscuți

```
(, ), {, }, [, ], ;, ,, :
```

## Exemple de Utilizare

### Exemplu 1: Program Simplu

**Input** (`test_program.txt`):
```c
int main() {
    int x = 123;
    float y = 3.14;
    return 0;
}
```

**Output**:
- 27 tokeni identificați
- 6 simboluri în TS
- 0 erori

### Exemplu 2: Program Complex

**Input** (`test_complex.txt`):
- Funcții
- Literale în toate bazele (decimal, hex, octal, binar)
- Numere reale cu notație științifică
- String-uri și caractere
- Structuri de control

### Exemplu 3: Detectare Erori

**Input** (`test_errors.txt`):
```c
int x = 5;
@ invalid character
int #bad = 10;
```

**Output**:
- Eroare: `@ invalid character` la linia X, coloana Y
- Eroare: `# invalid character` la linia X, coloana Y

## Implementare Tehnică

### Eliminarea Regex

Clasa `Automaton` a fost complet rescrisă pentru a **NU folosi** expresii regulare:

**Înainte** (cu regex):
```python
import re
m = re.search(r"states\s*({[^}]*})", text)
```

**Acum** (fără regex):
```python
def _find_section(text: str, keyword: str) -> Optional[str]:
    lines = text.split("\n")
    for line in lines:
        if line.strip().lower().startswith(keyword.lower()):
            return line.strip()[len(keyword):].strip()
    return None
```

### Algoritm de Recunoaștere

```python
def analyze(text: str):
    pos = 0
    while pos < len(text):
        # 1. Skip whitespace
        # 2. Try match string literals
        # 3. Try match char literals
        # 4. Try match operators/delimiters
        # 5. Try match real numbers (înainte de întregi!)
        # 6. Try match integers
        # 7. Try match identifiers
        # 8. Report error if nothing matches
```

### Longest Prefix Matching

Folosim metoda `longest_accepted_prefix()` din AFD pentru a găsi cel mai lung prefix acceptat:

```python
real_prefix = self.afd_real.longest_accepted_prefix(text[pos:])
if real_prefix:
    # Am găsit un număr real
    pos += len(real_prefix)
```

## Testare

### Test 1: Identificatori
```
a, _var, myVar123, __internal, CamelCase
```

### Test 2: Constante Întregi
```
0, 123, 0xFF, 0b1010, 0755, 42u, 100ULL
```

### Test 3: Constante Reale
```
3.14, 2.5e-3, 1.0E+10, 0.001f, 123.456L
```

### Test 4: Fără Spații
```
int x=5;if(x>0){x=x+1;}
```
✓ Trebuie să funcționeze corect!

## Diferențe față de Lab 1

Lab 1 (Prima Parte):
- Implementează automate finite generice
- Verifică secvențe acceptate
- Calculează longest prefix

Lab 3 (A Doua Parte):
- **Folosește** automatele din Lab 1
- Implementează analizor lexical complet
- Generează FIP și TS
- Raportează erori cu poziții

## Cerințe Îndeplinite

✅ Folosește **cel puțin 3 automate finite**:
   - Identificatori
   - Constante întregi
   - Constante reale

✅ **NU folosește expresii regulare** integrate

✅ **NU folosește spații** obligatoriu pentru separare

✅ Generează **FIP**, **TS** și **raportare erori**

✅ AFD pentru constante întregi bazat pe **documentația C++**:
   - Sursă: https://en.cppreference.com/w/cpp/language/integer_literal

## Concluzii

Acest analizor lexical demonstrează:
1. Puterea automatelor finite în recunoașterea pattern-urilor
2. Posibilitatea implementării unui analizor lexical complet **fără regex**
3. Importanța ordinii de verificare (reale înainte de întregi!)
4. Gestionarea corectă a erorilor lexicale

## Autor

Laborator 3 - LFTC (Limbaje Formale și Tehnici de Compilare)
Facultate - Anul 3