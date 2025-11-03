import numpy as np
import matplotlib.pyplot as plt

def bezier_cubic(t: np.ndarray, b: np.ndarray) -> np.ndarray:
    # b are forma (4, 2): b0, b1, b2, b3
    B0 = (1 - t) ** 3
    B1 = 3 * t * (1 - t) ** 2
    B2 = 3 * t**2 * (1 - t)
    B3 = t**3
    return (
        B0[:, None] * b[0] +
        B1[:, None] * b[1] +
        B2[:, None] * b[2] +
        B3[:, None] * b[3]
    )

def main():
    # Puncte de control (grad 3)
    b = np.array([
        [-3.0, 1.0],   # b0
        [-4.0, 4.0],   # b1
        [ 4.0, 4.0],   # b2
        [ 3.0, 1.0],   # b3
    ], dtype=float)

    # Puncte de control (grad 4)
    c = np.array([
        [-3.0,     1.0    ],  # c0
        [-15/4.0,  13/4.0 ],  # c1
        [ 0.0,     4.0    ],  # c2
        [ 15/4.0,  13/4.0 ],  # c3
        [ 3.0,     1.0    ],  # c4
    ], dtype=float)

    # Curba Bezier (grad 3) – curba este aceeasi si cand o privim ca grad 4
    t = np.linspace(0.0, 1.0, 400)
    curve = bezier_cubic(t, b)

    plt.figure(figsize=(9, 7))

    # Curba
    plt.plot(curve[:, 0], curve[:, 1], color='black', linewidth=2.5, label='Curba Bézier (grad 3)')

    # Poligon + puncte de control (grad 3)
    plt.plot(b[:, 0], b[:, 1], '--', color='tab:blue', linewidth=1.5, label='Poligon control (grad 3)')
    plt.scatter(b[:, 0], b[:, 1], color='tab:blue', s=70, zorder=3, label='Puncte control (grad 3)')

    # Poligon + puncte de control (grad 4)
    plt.plot(c[:, 0], c[:, 1], '--', color='tab:orange', linewidth=1.5, label='Poligon control (grad 4)')
    plt.scatter(c[:, 0], c[:, 1], color='tab:orange', marker='s', s=70, zorder=3, label='Puncte control (grad 4)')

    plt.title('Curba Bezier cubica si poligoanele de control (gradele 3 si 4)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('pb1.png', dpi=150)
    plt.show()

if __name__ == '__main__':
    main()