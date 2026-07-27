from __future__ import annotations

import json
import platform
import shutil
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[2]

    required_directories = [
        "qa/python",
        "qa/bash",
        "qa/robot/tests",
        "qa/sql",
        "infrastructure",
        "docs",
    ]

    required_tools = ["git", "dotnet", "bash", "python3"]

    directories = {
        path: (project_root / path).is_dir()
        for path in required_directories
    }

    tools = {
        tool: shutil.which(tool)
        for tool in required_tools
    }

    report = {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "project_root": str(project_root),
        "directories": directories,
        "tools": tools,
    }

    report_directory = project_root / "qa" / "reports"
    report_directory.mkdir(parents=True, exist_ok=True)

    report_path = report_directory / "environment-check.json"
    report_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))
    print(f"\nReport: {report_path}")

    directories_ok = all(directories.values())
    tools_ok = all(tools.values())

    return 0 if directories_ok and tools_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
