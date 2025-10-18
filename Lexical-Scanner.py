
"""
Kevin Madderom
kevin.madderom@ndus.edu
Program 2 CS365
"""

import sys


reservedWords = {"read", "write", "if", "else"}

def scan_identifier(content, i, row, col):
    token = ""
    startCol = col
    startRow = row
    while i < len(content) and content[i].isalnum():
        token += content[i]
        i += 1
        col += 1
    return token, i, col, startRow, startCol

def scan_num(content, i, row, col):
    token = ""
    startCol = col
    startRow = row
    float_found = False
    while i < len(content) and content[i].isdigit() or (content[i] == '.' and '.' not in token):
        if content[i] == ".":
            float_found = True
        token += content[i]
        i += 1
        col += 1
    return token, i, col, startRow, startCol

def scan_operators(content, i, row, col):
    ch = content[i]
    startCol = col
    startRow = row
    
    if ch == "=":
        expression = "<assign>"
    elif ch in "+-":
        expression = "<add_op>"
    elif ch in "*/%":
        expression = "<mult_op>"
    elif ch in "(":
        expression = "<lparen>"
    elif ch in ")":
        expression = "<rparen>"
    else:
        expression = "<error>"
        return -1, -1, startRow, startCol, expression
    
    return i + 1, col + 1, startRow, startCol, expression



def main():
    
    if len(sys.argv) < 2:
        print("prog2KMM.py sourcecode.txt")
        sys.exit(1)
    fileName = sys.argv[1]
   
    try:
        with open (fileName, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    
    row = 1
    col = 1
    i = 0
    
    while i < len(content):
        ch = content[i]  

        if ch == "#":
            while i < len(content) and content[i] != "\n":
                i += 1
            continue   
    
        if ch == "\n":
            row += 1
            col = 1
            i += 1
            continue
        if ch.isspace():
            i += 1
            col += 1
            continue

        
        if ch.isalpha():
            token, i, col, startRow, startCol = scan_identifier(content, i, row, col)
            if token in reservedWords:
                print(f"<{token}>, {token}, {startRow}, {startCol}")
            else:
                print(f"<id>, {token}, {startRow}, {startCol}")
                
        elif ch.isdigit():
            token, i, col, startRow, startCol = scan_num(content, i, row, col)
            print(f"<number>, {token}, {startRow}, {startCol}")
            
        else:
            i, col, startRow, startCol, expression = scan_operators(content, i, row, col)
            if i == -1:
                break
            print(f"{expression}, {ch}, {startRow}, {startCol}")
            
if __name__ == "__main__":
    main()
    
  
        
        

    