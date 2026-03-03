import os
import json
import subprocess
import shutil
from pathlib import Path

from .distiller import PaperBeeDistiller

class PaperBeeIngestor:
    def __init__(self, repo_url, output_dir="/tmp/paperbee_clones"):
        self.repo_url = repo_url
        self.repo_name = repo_url.split("/")[-1].replace(".git", "")
        self.working_dir = Path(output_dir) / self.repo_name
        self.manifest_path = self.working_dir / "paperbee_manifest.json"
        self.distiller = None

    def clone_repo(self):
        """Perform a shallow clone of the target repository."""
        if self.working_dir.exists():
            shutil.rmtree(self.working_dir)
        
        print(f"[*] Cloning {self.repo_url} into {self.working_dir}...")
        subprocess.run(
            ["git", "clone", "--depth", "1", self.repo_url, str(self.working_dir)],
            check=True, capture_output=True
        )
        self.distiller = PaperBeeDistiller(self.working_dir)

    def filter_core_logic(self):
        """Identify critical files using importance scoring."""
        scored_files = []
        ignore_patterns = {".git", "node_modules", "tests", "docs", "venv", "__pycache__", ".github", "scripts", "build", "dist"}
        relevant_extensions = {".py", ".js", ".ts", ".go", ".rs", ".cpp"}

        print("[*] Scoring repository files for Research Relevance...")
        for root, dirs, files in os.walk(self.working_dir):
            dirs[:] = [d for d in dirs if d not in ignore_patterns]
            for file in files:
                if any(file.endswith(ext) for ext in relevant_extensions):
                    path = Path(root) / file
                    score = 0
                    
                    # Boost: Location
                    if "src" in str(path) or "main" in str(path):
                        score += 10
                    if root == str(self.working_dir):
                        score += 5
                    
                    # Boost: Content Indicators
                    try:
                        with open(path, 'r', errors='ignore') as f:
                            content = f.read(5000)
                            # Complexity markers
                            if "class " in content or "def " in content:
                                score += 5
                            if "import " in content:
                                score += 2
                            # Research markers (Algorithms, Data Flow, Logic)
                            research_markers = ["Algorithm", "Optimization", "Model", "Layer", "Logic", "Compute", "Process", "Engine"]
                            for marker in research_markers:
                                if marker.lower() in content.lower():
                                    score += 3
                    except:
                        pass
                    
                    scored_files.append((path, score))
        
        # Sort by score descending and take top 15
        scored_files.sort(key=lambda x: x[1], reverse=True)
        final_selection = [f[0] for f in scored_files[:15]]
        
        print(f"[+] Selected {len(final_selection)} core logic files for distillation.")
        return final_selection

    def generate_manifest(self, core_files):
        """Build the final manifest using the Distiller's semantic data."""
        print(f"[*] Post-processing {len(core_files)} files for Semantic Distillation...")
        distilled_data = self.distiller.distill_repo(core_files)
        
        # Convert distilled features into PaperBanana methodology items
        methodology_items = []
        for feat in distilled_data["features"]:
            if "classes" in feat:
                for cls in feat["classes"]:
                    methodology_items.append({
                        "feature": f"Class: {cls['name']}",
                        "logic": cls.get("doc") or "Core data structure implementation.",
                        "rationale": f"Implements methods: {', '.join(cls['methods'][:3])}"
                    })
            if "functions" in feat:
                for fn in feat["functions"]:
                    methodology_items.append({
                        "feature": f"Logic: {fn['name']}",
                        "logic": fn.get("doc") or "Algorithm implementation.",
                        "rationale": f"Complexity Score: {fn['complexity_score']}"
                    })

        manifest = {
            "research_title": f"Hardcard Research: {self.repo_name} Technical Brief",
            "hardcard_template_id": "hc_v2_academic",
            "source_logic_summary": f"Automated semantic distillation of {self.repo_url}",
            "visual_intent": "Holistic Architecture & Computational Flow",
            "reference_styles": ["Hardcard_Standard_v2.pdf"],
            "methodology": methodology_items[:10], # Keep it focused
            "architecture_nodes": [
                {"id": m["source"], "label": Path(m["source"]).stem, "type": "module"}
                for m in distilled_data["dependency_graph"]
            ],
            "dependency_graph": distilled_data["dependency_graph"]
        }
        
        with open(self.manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return self.manifest_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ingestor.py <repo_url>")
        sys.exit(1)
    
    repo = sys.argv[1]
    ingestor = PaperBeeIngestor(repo)
    ingestor.clone_repo()
    core = ingestor.filter_core_logic()
    path = ingestor.generate_manifest_draft(core)
    print(f"[+] Manifest draft generated at: {path}")
