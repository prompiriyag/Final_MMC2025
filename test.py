from sympy import symbols, Eq, solve, simplify

B = symbols('B')

A = 15  # พื้นที่ปลูกไผ่
P_agri = 468622
P_bamboo = 70707000
C_forest = 52.9
C_agri = 2.97
P_carbon = 173
T = 99
C_mgmt = 19500
Y = 3
N = 20

lhs = (A + B) * P_agri

rhs = (
    P_bamboo +
    ((B * C_forest) - (C_agri * (T - A - B))) * P_carbon * N -
    (C_mgmt * B * Y)
)

equation = Eq(lhs, rhs)

solution = solve(equation, B)

solution_real = [s.evalf() for s in solution if s.is_real]

print(solution_real)