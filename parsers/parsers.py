import ast

def extract_functions_from_code(code: str):
    try:
        tree = ast.parse(code)
        return {
            node.name: ast.get_source_segment(code, node)
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        }
    except:
        return {}

def extract_call_graph(code: str):
    call_graph = {}
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                callers = []
                for child in ast.walk(node):
                    if isinstance(child, ast.Call) and hasattr(child.func, "id"):
                        callers.append(child.func.id)
                call_graph[node.name] = list(set(callers))
    except:
        pass
    return call_graph

def extract_class_hierarchy(code: str):
    class_map = {}
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                class_map[node.name] = methods
    except:
        pass
    return class_map
