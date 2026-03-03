import argparse
import sys
import os
from src.ingestor import PaperBeeIngestor

def main():
    parser = argparse.ArgumentParser(description="PaperBee: Research Engineer for PaperBanana & Hardcard Research")
    parser.add_argument("repo_url", help="URL of the GitHub repository to analyze")
    parser.add_argument("--output", help="Output directory for the manifest", default="output")
    parser.add_argument("--hardcard", action="store_true", help="Enforce Hardcard Research rigor standards")

    args = parser.parse_args()

    print("--- 🐝 PaperBee: Initializing Extraction ---")
    
    try:
        ingestor = PaperBeeIngestor(args.repo_url)
        
        # 1. Extraction
        ingestor.clone_repo()
        
        # 2. Semantic Distillation
        core_files = ingestor.filter_core_logic()
        
        # 3. Manifest Generation
        manifest_path = ingestor.generate_manifest(core_files)
        
        print(f"\n[+] Extraction Complete.")
        print(f"[+] Handoff Bundle: {manifest_path}")
        print("\n--- 🍌 Ready for PaperBanana Synthesis ---")
        print("Next step: Feed this manifest to the PaperBanana Planner Agent.")

    except Exception as e:
        print(f"\n[!] Error during distillation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
