from dataclasses import dataclass
import math
from typing import Tuple, Optional, List

Matrix4 = List[List[float]]

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
                print("Vectorul normal (a,b,c) nu poate fi nul. Reincercați.")
                continue
            plane = Plane(a, b, c, d).normalized()
            return plane

        else:
            px, py, pz = read_floats("Introduceti coordonatele punctului P0 (x y z): ", 3)
            nx, ny, nz = read_floats("Introduceti componentele vectorului normal n (nx ny nz): ", 3)
            norm_n = (nx**2 + ny**2 + nz**2) ** 0.5
            if norm_n < EPS:
                print("Vectorul normal n nu poate fi nul. Reincercați.")
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

    # Ar trebui să fie imposibil pentru un plan valid să nu intersecteze nicio axă
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
        print("- Planul trece deja prin origine; translația NU este necesară.")
    else:
        tx, ty, tz = -point[0], -point[1], -point[2]
        T = mat4_translation(tx, ty, tz)
        print("- Matricea translației T (vector = (-x*, -y*, -z*)) unde P* este punctul ales pe plan:")
        print(format_mat4(T)) 

    # -------- PASUL 3 --------
    print("\n=== Pasul 3: rotatie astfel incat normala sa fie paralela cu un plan de coordonate ===")
    par = plane.parallel_to_coordinate_plane()
    if par:
        R_y = mat4_identity()
        print(f"- Planul este paralel cu planul de coordonate {par}; rotatia NU este necesară.")
    elif abs(plane.c) < EPS:
        R_y = mat4_identity()
        print("- Normala este deja paralela cu planul XY (c~0); rotatia NU este necesara.")
    else:
        theta = math.atan2(plane.c, plane.a)
        R_y = mat4_rotation_y(theta)
        print(f"- Rotatie in jurul axei Y cu unghi θ = atan2(c, a) = {theta:.2f} rad.")
        print(format_mat4(R_y))
        a1 = (plane.a**2 + plane.c**2) ** 0.5
        b1 = plane.b
        print(f"- Normala dupa rotatie (a', b', c'): ({a1:.2f}, {b1:.2f}, {0.0:.2f})  → paralela cu XY.")

    # -------- PASUL 4 --------
    print("\n=== Pasul 4: rotatie astfel incat planul sa coincida cu un plan de coordonate ===")
    

if __name__ == "__main__":
    main()
