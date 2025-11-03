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

def de_casteljau_split(b: np.ndarray, t0: float):
    # Subdivizare De Casteljau la parametrul t0
    b01 = (1 - t0) * b[0] + t0 * b[1]
    b12 = (1 - t0) * b[1] + t0 * b[2]
    b23 = (1 - t0) * b[2] + t0 * b[3]

    b0112 = (1 - t0) * b01 + t0 * b12
    b1223 = (1 - t0) * b12 + t0 * b23

    p = (1 - t0) * b0112 + t0 * b1223  # punctul pe curba la t0

    left = np.vstack([b[0], b01, b0112, p])
    right = np.vstack([p, b1223, b23, b[3]])
    return left, right, p

def main():
    # Puncte de control (curba originala de grad 3) – aceleasi ca in pb1.py
    b = np.array([
        [-3.0, 1.0],   # b0
        [-4.0, 4.0],   # b1
        [ 4.0, 4.0],   # b2
        [ 3.0, 1.0],   # b3
    ], dtype=float)

    # Subdivizare la t0 = 1/3
    t0 = 1.0 / 3.0
    left_ctrl, right_ctrl, p_split = de_casteljau_split(b, t0)

    # Curbele pentru cele doua segmente (parametrizate pe [0, 1])
    s = np.linspace(0.0, 1.0, 300)
    curve_left = bezier_cubic(s, left_ctrl)
    curve_right = bezier_cubic(s, right_ctrl)

    plt.figure(figsize=(9, 7))

    # Cele două segmente de curba
    plt.plot(curve_left[:, 0], curve_left[:, 1], color='tab:red', linewidth=2.5, label='Segment stang (t ∈ [0, 1/3])')
    plt.plot(curve_right[:, 0], curve_right[:, 1], color='tab:green', linewidth=2.5, label='Segment drept (t ∈ [1/3, 1])')

    # Poligon + puncte de control (curba originala)
    plt.plot(b[:, 0], b[:, 1], '--', color='tab:blue', linewidth=1.5, label='Poligon control (curba originala)')
    plt.scatter(b[:, 0], b[:, 1], color='tab:blue', s=70, zorder=3, label='Puncte control (curba originala)')

    # Poligon + puncte de control pentru segmentele subdivizate
    plt.plot(left_ctrl[:, 0], left_ctrl[:, 1], '--', color='tab:orange', linewidth=1.5, label='Poligon control (segment stang)')
    plt.scatter(left_ctrl[:, 0], left_ctrl[:, 1], color='tab:orange', marker='s', s=70, zorder=3, label='Puncte control (segment stang)')

    plt.plot(right_ctrl[:, 0], right_ctrl[:, 1], '--', color='tab:purple', linewidth=1.5, label='Poligon control (segment drept)')
    plt.scatter(right_ctrl[:, 0], right_ctrl[:, 1], color='tab:purple', marker='^', s=70, zorder=3, label='Puncte control (segment drept)')

    # Marcheaza punctul de divizare
    plt.scatter([p_split[0]], [p_split[1]], color='black', marker='x', s=80, zorder=4, label='Punct la t = 1/3')

    plt.title('Subdivizarea curbei Bézier cubice la t = 1/3')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('pb2.png', dpi=150)
    plt.show()

if __name__ == '__main__':
    main()