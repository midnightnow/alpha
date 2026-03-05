import json
import os

def create_report(results):
    report_path = "/Users/studio/ALPHA/validation_suite/report/VALIDATION_REPORT.json"
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"\n[REPORT] Detailed data written to {report_path}")

    # Terminal summary table
    print("\n" + "="*75)
    print(f"{'DOMAIN':<25} | {'PREDICTED':<12} | {'OBSERVED':<12} | {'ERROR':<10} | {'STATUS'}")
    print("-" * 75)
    
    for key, val in results.items():
        if isinstance(val, dict) and 'predicted' in val:
            status = "✅ PASS" if val['pass'] else "❌ FAIL"
            pred = f"{val['predicted']:.4f}"
            obs = f"{val['observed']:.4f}"
            err = f"{val['error']:.4f}"
            print(f"{key.upper():<25} | {pred:<12} | {obs:<12} | {err:<10} | {status}")
    print("="*75)
