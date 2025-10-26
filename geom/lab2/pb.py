from dataclasses import dataclass
import math
from typing import Tuple, Optional, List
import builtins
import atexit
_log_file = None

def setup_output_file(path="pb_output.txt"):
    global _log_file
    try:
        _log_file = open(path, "w", encoding="utf-8")
    except Exception:
        _log_file = None

def close_output_file():
    global _log_file
    if _log_file:
        _log_file.close()
        _log_file = None

# print “tee”: si in consola, si in fisier (fara conversii)
def print(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")
    text = sep.join(str(a) for a in args)
    if _log_file:
        _log_file.write(text + end)
        _log_file.flush()
    builtins.print(*args, **kwargs)

def input(prompt=""):
    if _log_file:
        _log_file.write(str(prompt))
        _log_file.flush()
    return builtins.input(prompt)

atexit.register(close_output_file)


Matrix4 = List[List[float]]

# functii utilitare pentru inmultirea 4x4
def mat4_mul(A: Matrix4, B: Matrix4) -> Matrix4:
    C = [[0.0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(4))
    return C

def mat4_chain(mats: List[Matrix4]) -> Matrix4:
    M = mat4_identity()
    for X in mats:
        M = mat4_mul(M, X)
    return M

def mat4_identity() -> Matrix4:
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]

def mat4_translation(tx: float, ty: float, tz: float) -> Matrix4:
    return [
        [1.0, 0.0, 0.0, tx],
        [0.0, 1.0, 0.0, ty],
        [0.0, 0.0, 1.0, tz],
        [0.0, 0.0, 0.0, 1.0],
    ]

def mat4_rotation_y(theta: float) -> Matrix4:
    cos_a = math.cos(theta)
    sin_a = math.sin(theta)
    return [
        [cos_a, 0.0, sin_a, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [-sin_a, 0.0, cos_a, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]

def mat4_rotation_z(theta: float) -> Matrix4:
    cos_a = math.cos(theta)
    sin_a = math.sin(theta)
    return [
        [cos_a, -sin_a, 0.0, 0.0],
        [sin_a, cos_a, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]

def mat4_reflection_yz() -> Matrix4:
    # Reflexie fata de planul YZ (x -> -x)
    return [
        [-1.0, 0.0, 0.0, 0.0],
        [ 0.0, 1.0, 0.0, 0.0],
        [ 0.0, 0.0, 1.0, 0.0],
        [ 0.0, 0.0, 0.0, 1.0],
    ]

def format_mat4(M: Matrix4) -> str:
    return "\n".join("  " + " ".join(f"{v:10.2f}" for v in row) for row in M)

EPS = 1e-12

@dataclass
class Plane:
    a: float
    b: float
    c: float
    d: float

    def normalized(self) -> "Plane":
        norm = (self.a**2 + self.b**2 + self.c**2)**0.5
        if norm < EPS:
            raise ValueError("Vectorul normal al planului nu poate fi zero.")
        return Plane(self.a / norm, self.b / norm, self.c / norm, self.d / norm)

    def passes_through_origin(self) -> bool:
        return abs(self.d) < EPS

    def parallel_to_coordinate_plane(self) -> Optional[str]:
        a0 = abs(self.a) < EPS
        b0 = abs(self.b) < EPS
        c0 = abs(self.c) < EPS
        if a0 and b0 and not c0:
            return "XY"
        elif a0 and not b0 and c0:
            return "XZ"
        elif not a0 and b0 and c0:
            return "YZ"
        else:
            return None

    def is_coordinate_plane(self) -> Optional[str]:
        kind = self.parallel_to_coordinate_plane()
        if kind and self.passes_through_origin():
            return kind
        else:
            return None

def read_floats(prompt: str, expected_count:int) -> Tuple[float, ...]:
    while True:
        try:
            parts = input(prompt).strip().split()
            if len(parts) != expected_count:
                print(f"Introduceti exact {expected_count} numere reale, separate prin spatiu.")
                continue
            return tuple(float(x) for x in parts)
        except ValueError:
            print("Valori invalide. Reincercati.")

def read_plane() -> Plane:
    while True:
        mode = input("Planul se da prin (1=ecuatia generala, 2=punct si vector normal): ").strip()
        if mode not in {"1", "2"}:
            print("Alegeti 1 sau 2.")
            continue

        if mode == "1":
            a, b, c, d = read_floats("Introduceti a b c d: ", 4)
            if abs(a) < EPS and abs(b) < EPS and abs(c) < EPS:
                print("Vectorul normal (a,b,c) nu poate fi nul. Reincercati.")
                continue
            plane = Plane(a, b, c, d).normalized()
            return plane

        else:
            px, py, pz = read_floats("Introduceti coordonatele punctului P0 (x y z): ", 3)
            nx, ny, nz = read_floats("Introduceti componentele vectorului normal n (nx ny nz): ", 3)
            norm_n = (nx**2 + ny**2 + nz**2) ** 0.5
            if norm_n < EPS:
                print("Vectorul normal n nu poate fi nul. Reincercati.")
                continue
            # Versorul normal
            ax, by, cz = nx / norm_n, ny / norm_n, nz / norm_n
            # d = -n · P0
            d = -(ax * px + by * py + cz * pz)
            plane = Plane(ax, by, cz, d)
            return plane

def axis_intersection(plane: Plane) -> Tuple[str, Tuple[float, float, float], str]:
    """Determina un punct de intersectie cu o axa (X/Y/Z) si mesajul descriptiv."""
    p = plane.normalized()

    # X-axis: y=0, z=0 -> a*x + d = 0
    if abs(p.a) > EPS:
        x = -p.d / p.a
        return "X", (x, 0.0, 0.0), "intersectie unica cu axa X"
    elif p.passes_through_origin():
        return "X", (0.0, 0.0, 0.0), "axa X este continuta in plan (infinit de puncte)"

    # Y-axis: x=0, z=0 -> b*y + d = 0
    if abs(p.b) > EPS:
        y = -p.d / p.b
        return "Y", (0.0, y, 0.0), "intersectie unica cu axa Y"
    elif p.passes_through_origin():
        return "Y", (0.0, 0.0, 0.0), "axa Y este continuta in plan (infinit de puncte)"

    # Z-axis: x=0, y=0 -> c*z + d = 0
    if abs(p.c) > EPS:
        z = -p.d / p.c
        return "Z", (0.0, 0.0, z), "intersectie unica cu axa Z"
    elif p.passes_through_origin():
        return "Z", (0.0, 0.0, 0.0), "axa Z este continuta in plan (infinit de puncte)"

    # Ar trebui sa fie imposibil pentru un plan valid sa nu intersecteze nicio axa
    raise RuntimeError("Plan invalid: nu intersecteaza nicio axa de coordonate.")

def main():
    # -------- PASUL 1 --------
    print("=== Pasul 1: determinarea punctului de intersectie dintre plan si o axa ===")
    plane = read_plane()
    axis, point, msg = axis_intersection(plane)

    par = plane.parallel_to_coordinate_plane()
    coord_plane = plane.is_coordinate_plane()

    print("\nRezultate:")
    print(f"- Ecuația planului normalizata: {plane.a:.2f} x + {plane.b:.2f} y + {plane.c:.2f} z + {plane.d:.2f} = 0")
    print(f"- Punct de intersectie ales (axa {axis}): ({point[0]:.2f}, {point[1]:.2f}, {point[2]:.2f})")
    print(f"- Detaliu: {msg}")
    print(f"- Planul trece prin origine: {'DA' if plane.passes_through_origin() else 'NU'}")
    if par:
        print(f"- Planul este paralel cu planul de coordonate {par}.")
    if coord_plane:
        print(f"- Planul ESTE chiar planul de coordonate {coord_plane} (d=0).")

    # -------- PASUL 2 --------
    print("\n=== Pasul 2: matricea translatiei care aduce planul prin origine ===")
    if plane.passes_through_origin():
        T = mat4_identity()
        translation_needed = False
        tx = ty = tz = 0.0
        print("- Planul trece deja prin origine; translatia NU este necesară.")
    else:
        tx, ty, tz = -point[0], -point[1], -point[2]
        translation_needed = True
        T = mat4_translation(tx, ty, tz)
        print("- Matricea translatiei T (vector = (-x*, -y*, -z*)) unde P* este punctul ales pe plan:")
        print(format_mat4(T)) 
    # -------- PASUL 3 --------
    print("\n=== Pasul 3: rotatie astfel incat normala sa fie paralela cu un plan de coordonate ===")
    theta = 0.0
    rot_y_needed = False
    par = plane.parallel_to_coordinate_plane()
    if par:
        R_y = mat4_identity()
        print(f"- Planul este paralel cu planul de coordonate {par}; rotatia NU este necesara.")
    elif abs(plane.c) < EPS:
        R_y = mat4_identity()
        print("- Normala este deja paralela cu planul XY (c~0); rotatia NU este necesara.")
    else:
        theta = math.atan2(plane.c, plane.a)
        rot_y_needed = True
        R_y = mat4_rotation_y(theta)
        print(f"- Rotatie in jurul axei Y cu unghi theta = atan2(c, a) = {theta:.2f} rad.")
        print(format_mat4(R_y))
        a1 = (plane.a**2 + plane.c**2) ** 0.5
        b1 = plane.b
        print(f"- Normala dupa rotatie (a', b', c'): ({a1:.2f}, {b1:.2f}, {0.0:.2f})  → paralela cu XY.")

    # -------- PASUL 4 --------
    print("\n=== Pasul 4: rotatie astfel incat planul sa coincida cu un plan de coordonate ===")
    A = math.sqrt(plane.a**2 + plane.c**2)
    B = plane.b
    phi = 0.0
    rot_z_needed = False
    if abs(B) < EPS:
        R_z = mat4_identity()
        print("- Dupa Pasul 3, componenta pe Y a normalei este ~ 0; rotatia in jurul Z NU este necesara.")
    else:
        phi = -math.atan2(B, A)
        rot_z_needed = True
        R_z = mat4_rotation_z(phi)
        print(f"- Rotatie in jurul axei Z cu unghi phi = -atan2(b, sqrt(a^2+c^2)) = {phi:.2f} rad.")
        print(format_mat4(R_z))
        x2 = math.sqrt(A*A + B*B)  # ~ 1 pentru plan normalizat
        print(f"- Normala dupa rotirea Z: ({x2:.2f}, {0.0:.2f}, {0.0:.2f}) -> aliniata pe Ox, planul coincide cu YZ.")

    # -------- PASUL 5 --------
    print("\n=== Pasul 5: matricea reflexiei fata de planul YZ ===")
    Ref = mat4_reflection_yz()
    print("- Matricea reflexiei F (fata de YZ: x -> -x):")
    print(format_mat4(Ref))
    
    # -------- PASUL 6 --------
    print("\n=== Pasul 6: matricea rotatiei inverse fata de rotatia din Pasul 4 ===")
    if rot_z_needed:
        R_z_inv = mat4_rotation_z(-phi)
        print(f"- Rotatia inversa in jurul Z cu unghi -phi = {(-phi):.2f} rad.")
        print(format_mat4(R_z_inv))
    else:
        R_z_inv = mat4_identity()
        print("- Pasul 4 nu a necesitat rotatie; matricea inversa este identitatea.")
    
    # -------- PASUL 7 --------
    print("\n=== Pasul 7: matricea rotatiei inverse fata de rotatia din Pasul 3 ===")
    if rot_y_needed:
        R_y_inv = mat4_rotation_y(-theta)
        print(f"- Rotatia inversa in jurul Y cu unghi -theta = {(-theta):.2f} rad.")
        print(format_mat4(R_y_inv))
    else:
        R_y_inv = mat4_identity()
        print("- Pasul 3 nu a necesitat rotatie; matricea inversa este identitatea.")

    # -------- PASUL 8 --------
    print("\n=== Pasul 8: matricea translatiei inverse celei de la Pasul 2 ===")
    if translation_needed:
        T_inv = mat4_translation(-tx, -ty, -tz)  # = mat4_translation(x*, y*, z*)
        print("- Translatie inversa T_inv (vector = (x*, y*, z*)):")
        print(format_mat4(T_inv))
    else:
        T_inv = mat4_identity()
        print("- Planul trece prin origine; translatia inversa NU este necesara (identitate).")

    # -------- PASUL 9: matricea transformarii compuse --------
    print("\n=== Pasul 9: matricea transformarii compuse ===")
    M = mat4_chain([T_inv, R_y_inv, R_z_inv, Ref, R_z, R_y, T])
    print("- Matricea compusa M = T_inv · R_y_inv · R_z_inv · F · R_z · R_y · T:")
    print(format_mat4(M))

    # -------- PASUL 10 --------
    print("\n=== Pasul 10: citirea varfurilor poliedrului ===")
    while True:
        try:
            n_vertices = int(input("Introduceti numarul de varfuri ale poliedrului (>=1): "))
            if n_vertices >= 1:
                break
            else:
                print("Numarul de varfuri trebuie sa fie cel putin 1.")
        except ValueError:
            print("Introduceti un numar intreg valid.")
    
    vertices = []
    for i in range(n_vertices):
        x, y, z = read_floats(f"Introduceti coordonatele varfului {i+1} (x y z): ", 3)
        vertices.append([x, y, z, 1.0])  # coordonate omogene
    
    print(f"- S-au citit {n_vertices} varfuri ale poliedrului.")

    # -------- PASUL 11 --------
    print("\n=== Pasul 11: matricea omogena a coordonatelor varfurilor transformate ===")
    transformed_vertices = []
    for vertex in vertices:
        # Aplicam transformarea M asupra fiecarui varf (vector coloana)
        transformed = [sum(M[i][j] * vertex[j] for j in range(4)) for i in range(4)]
        transformed_vertices.append(transformed)
    
    print("- Matricea coordonatelor omogene ale varfurilor imaginii poliedrului:")
    print("  [Varf 1] [Varf 2] ... [Varf n]")
    for i in range(4):
        row_str = "  "
        for j in range(n_vertices):
            row_str += f"{transformed_vertices[j][i]:10.6f} "
        print(row_str)
    
    print("\n- Coordonatele carteziene ale varfurilor transformate:")
    for i, tv in enumerate(transformed_vertices):
        if abs(tv[3]) > EPS:  # normalizare omogena
            x, y, z = tv[0]/tv[3], tv[1]/tv[3], tv[2]/tv[3]
        else:
            x, y, z = tv[0], tv[1], tv[2]  # punct la infinit
        print(f"  Varf {i+1}: ({x:.6f}, {y:.6f}, {z:.6f})")

def run_tests():
    """Ruleaza teste automate pentru diferite cazuri speciale"""
    print("=== TESTE AUTOMATE ===\n")
    
    test_cases = [
        {
            "name": "Plan paralel cu XY (z = 2)",
            "plane": Plane(0, 0, 1, -2),
            "vertices": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "description": "Planul este paralel cu XY -> nu sunt necesare rotatii"
        },
        {
            "name": "Plan paralel cu YZ (x = 3)", 
            "plane": Plane(1, 0, 0, -3),
            "vertices": [[0, 1, 0], [0, 0, 1], [1, 1, 1]],
            "description": "Planul este paralel cu YZ -> nu sunt necesare rotatii"
        },
        {
            "name": "Plan de coordonate XY (z = 0)",
            "plane": Plane(0, 0, 1, 0),
            "vertices": [[1, 0, 0], [0, 1, 0], [1, 1, 0]],
            "description": "Plan de coordonate -> nu sunt necesare nici rotatii, nici translatii"
        },
        {
            "name": "Plan oblic prin origine",
            "plane": Plane(1, 1, 1, 0).normalized(),
            "vertices": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "description": "Planul trece prin origine -> nu este necesara translatia"
        },
        {
            "name": "Plan oblic general",
            "plane": Plane(1, 2, 3, -6).normalized(),
            "vertices": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            "description": "Plan general -> toate transformarile sunt necesare"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"--- TEST {i}: {test['name']} ---")
        print(f"Descriere: {test['description']}")
        print(f"Ecuatia planului: {test['plane'].a:.3f}x + {test['plane'].b:.3f}y + {test['plane'].c:.3f}z + {test['plane'].d:.3f} = 0")
        
        # Verificări cazuri speciale
        par = test['plane'].parallel_to_coordinate_plane()
        coord_plane = test['plane'].is_coordinate_plane()
        passes_origin = test['plane'].passes_through_origin()
        
        print(f"- Paralel cu plan de coordonate: {par if par else 'NU'}")
        print(f"- Este plan de coordonate: {coord_plane if coord_plane else 'NU'}")
        print(f"- Trece prin origine: {'DA' if passes_origin else 'NU'}")
        
        # Simulare transformari
        axis, point, _ = axis_intersection(test['plane'])
        print(f"- Intersectie cu axa {axis}: ({point[0]:.3f}, {point[1]:.3f}, {point[2]:.3f})")
        
        # Verificare necesitate transformari
        need_translation = not passes_origin
        need_rot_y = not par and abs(test['plane'].c) >= EPS
        A = math.sqrt(test['plane'].a**2 + test['plane'].c**2)
        B = test['plane'].b
        need_rot_z = abs(B) >= EPS
        
        print(f"- Translatie necesara: {'DA' if need_translation else 'NU'}")
        print(f"- Rotatie Y necesara: {'DA' if need_rot_y else 'NU'}")
        print(f"- Rotatie Z necesara: {'DA' if need_rot_z else 'NU'}")
        
        # Calculare matrice compusa (versiune simplificata pentru test)
        T = mat4_translation(-point[0], -point[1], -point[2]) if need_translation else mat4_identity()
        R_y = mat4_rotation_y(math.atan2(test['plane'].c, test['plane'].a)) if need_rot_y else mat4_identity()
        R_z = mat4_rotation_z(-math.atan2(B, A)) if need_rot_z else mat4_identity()
        Ref = mat4_reflection_yz()
        R_z_inv = mat4_rotation_z(math.atan2(B, A)) if need_rot_z else mat4_identity()
        R_y_inv = mat4_rotation_y(-math.atan2(test['plane'].c, test['plane'].a)) if need_rot_y else mat4_identity()
        T_inv = mat4_translation(point[0], point[1], point[2]) if need_translation else mat4_identity()
        
        M = mat4_chain([T_inv, R_y_inv, R_z_inv, Ref, R_z, R_y, T])
        
        # Aplicare pe primul varf ca exemplu
        vertex = test['vertices'][0] + [1.0]  # coordonate omogene
        transformed = [sum(M[i][j] * vertex[j] for j in range(4)) for i in range(4)]
        
        if abs(transformed[3]) > EPS:
            x, y, z = transformed[0]/transformed[3], transformed[1]/transformed[3], transformed[2]/transformed[3]
        else:
            x, y, z = transformed[0], transformed[1], transformed[2]
            
        print(f"- Primul varf {test['vertices'][0]} → ({x:.3f}, {y:.3f}, {z:.3f})")
        print()

def main_interactive():
    """Ruleaza programul in mod interactiv."""
    main()

if __name__ == "__main__":
    import sys
    setup_output_file("pb_output.txt")
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        print("Pentru teste automate, rulati: python pb.py --test")
        print("Pentru mod interactiv, apasati Enter...")
        input()
        main_interactive()


