from pwn import *
import base64
import sys
import re
from pprint import pprint
from z3 import *

if len(sys.argv) < 3:
    conn = remote("localhost", 1488)
else:
    conn = remote(sys.argv[1], sys.argv[2])

equation_regex = r'(\d+)\*([a-z])(?: \+ )?| = (\d+)'

# List of variables (a-z)
variables = 'abcdefghijklmnopqrstuvwxyz'
z3_vars = {var: Int(var) for var in variables}

def solve_equations(equations):
    solver = Solver()
    
    for eq in equations:
        matches = re.findall(equation_regex, eq)
        
        # Build the equation for Z3
        lhs = 0
        for match in matches:
            if match[0]:  # coefficient and variable
                coeff = int(match[0])
                var = match[1]
                lhs += coeff * z3_vars[var]
            if match[2]:  # constant
                rhs = int(match[2])
        
        # Add the equation to the solver
        solver.add(lhs == rhs)

    # Check satisfiability and get the model
    if solver.check() == sat:
        m = solver.model()
        solution = sorted([(d, m[d].as_long()) for d in m], key = lambda x: str(x[0]))
        solution = [ans[1] for ans in solution]
        return solution
    else:
        print("No solution found.")

rnd = 1
conn.recvuntil(b"Solutions (in alphabetical order of variables):")
data = conn.recvuntil(b"Solutions (in alphabetical order of variables):").decode().split("\n")
equations = data[3:-1]

conn.sendline(str(solve_equations(equations)).encode())

while rnd <= 500:
    try:
        data = conn.recvuntil(b"Solutions (in alphabetical order of variables):")
    except:
        data = conn.recvall()
        conn.close()
        print(data)
    data = data.decode().split("\n")
    equations = data[1:-1]
    
    answers = solve_equations(equations)
    stroke = ''.join([chr(ans) for ans in answers])
    
    print(stroke)
                     
    if "goctf" in stroke:
        print("\n\n\n\nFLAG FOUND!!!\n\n\n\n")
        
    conn.sendline(str(solve_equations(equations)).encode())





                
        
