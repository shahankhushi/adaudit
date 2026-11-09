import argparse
import sys
import json
from pathlib import Path
from .auditor import parse_csv_export, audit_account, render_audit_markdown
from . import __version__

def main():
    parser = argparse.ArgumentParser(
        prog="adaudit",
        description="Zero-login ad account auditor for Meta and Google Ads CSV exports."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze an ad account CSV export")
    analyze_parser.add_argument("file", help="Path to CSV export file")
    analyze_parser.add_argument("--target-cpa", "-t", type=float, default=None, help="Target CPA benchmark (USD)")
    analyze_parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if not args.command:
        # Default behavior: if user passed a file directly
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
            args.command = "analyze"
            args.file = sys.argv[1]
            args.target_cpa = None
            args.json = False
        else:
            parser.print_help()
            sys.exit(1)

    if args.command == "analyze":
        csv_path = Path(args.file)
        if not csv_path.exists():
            sys.stderr.write(f"Error: CSV export file not found: {csv_path}\n")
            sys.exit(1)

        rows = parse_csv_export(str(csv_path))
        if not rows:
            sys.stderr.write("Error: No valid ad data rows found in CSV.\n")
            sys.exit(1)

        results = audit_account(rows, target_cpa=args.target_cpa)

        if args.json:
            # Prepare serializable dict
            serializable = {
                "summary": results["summary"],
                "wasted_count": len(results["wasted_ads"]),
                "fatigued_count": len(results["fatigued_ads"]),
                "winners_count": len(results["top_winners"])
            }
            print(json.dumps(serializable, indent=2))
        else:
            print(render_audit_markdown(results))

if __name__ == "__main__":
    main()
