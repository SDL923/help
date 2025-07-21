import ast
import os

def convert_py_to_ast(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
    
    try:
        tree = ast.parse(source, filename=filename)
        ast_str = ast.dump(tree, indent=4)
    except SyntaxError as e:
        print(f"SyntaxError in file {filename}: {e}")
        return

    ast_filename = os.path.splitext(filename)[0] + '.ast'
    with open(ast_filename, 'w', encoding='utf-8') as f:
        f.write(ast_str)
    print(f"Converted {filename} to {ast_filename}")

def convert_all_py_in_folder():
    current_dir = os.getcwd()
    for file in os.listdir(current_dir):
        if file.endswith('.py') and file != os.path.basename(__file__):  # exclude self
            convert_py_to_ast(file)

if __name__ == "__main__":
    convert_all_py_in_folder()
