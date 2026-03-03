import ast
import os
from pathlib import Path

class PaperBeeDistiller:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.dependencies = {}
        self.features = []

    def analyze_python_file(self, file_path):
        """Parse Python file using AST to extract classes, functions, and docstrings."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
        except Exception as e:
            return {"error": str(e)}

        file_distillation = {
            "path": str(file_path.relative_to(self.root_dir)),
            "classes": [],
            "functions": [],
            "imports": []
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                doc = ast.get_docstring(node)
                file_distillation["classes"].append({
                    "name": node.name,
                    "doc": doc,
                    "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                })
            elif isinstance(node, ast.FunctionDef) and not isinstance(getattr(node, 'parent', None), ast.ClassDef):
                # Simple logic: if it has a docstring or is "complex" (has loops/ifs), it's a feature
                doc = ast.get_docstring(node)
                complexity = sum(1 for n in ast.walk(node) if isinstance(n, (ast.If, ast.For, ast.While, ast.With)))
                if doc or complexity > 2:
                    file_distillation["functions"].append({
                        "name": node.name,
                        "doc": doc,
                        "complexity_score": complexity
                    })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        file_distillation["imports"].append(alias.name)
                else:
                    file_distillation["imports"].append(node.module)

        return file_distillation

    def build_dependency_graph(self, distilled_files):
        """Crude mapping of internal module dependencies."""
        internal_modules = {Path(f["path"]).stem for f in distilled_files}
        graph = []
        
        for f in distilled_files:
            for imp in f.get("imports", []):
                if imp in internal_modules:
                    graph.append({"source": f["path"], "target": imp, "type": "dependency"})
        
        return graph

    def distill_repo(self, core_files):
        """Orchestrate the distillation of multiple files."""
        results = []
        for file in core_files:
            if file.suffix == ".py":
                results.append(self.analyze_python_file(file))
            else:
                # Heuristic for non-python: just look for function-like patterns or keywords
                results.append({"path": str(file.relative_to(self.root_dir)), "note": "Non-Python heuristic scan pending."})
        
        self.features = results
        dep_graph = self.build_dependency_graph(results)
        
        return {
            "features": self.features,
            "dependency_graph": dep_graph
        }

if __name__ == "__main__":
    # Test logic
    distiller = PaperBeeDistiller(".")
    # Dummy run if called directly
    pass
