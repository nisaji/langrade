import sys
from pathlib import Path
import re
import tomli


def get_version_from_file(file_path: Path, pattern: str) -> str:
    content = file_path.read_text()
    match = re.search(pattern, content)
    if not match:
        raise ValueError(f"Version not found in {file_path}")
    return match.group(1)


def validate_version_format(version: str) -> bool:
    pattern = r"^\d+\.\d+\.\d+$"
    return bool(re.match(pattern, version))


def compare_versions(old_version: str, new_version: str) -> bool:
    old_parts = [int(x) for x in old_version.split(".")]
    new_parts = [int(x) for x in new_version.split(".")]

    if new_parts <= old_parts:
        return False

    if new_parts[0] > old_parts[0] + 1:
        return False

    return True


def main():
    root_dir = Path(__file__).parent.parent

    with open(root_dir / "pyproject.toml", "rb") as f:
        version = tomli.load(f)["tool"]["poetry"]["version"]

    if not validate_version_format(version):
        print(f"Invalid version format: {version}")
        sys.exit(1)

    if len(sys.argv) > 1:
        old_version = sys.argv[1].lstrip("v")
        if not compare_versions(old_version, version):
            print(f"Invalid version increment: {old_version} -> {version}")
            sys.exit(1)

    print(f"Version validation successful: {version}")
    sys.exit(0)


if __name__ == "__main__":
    main()
