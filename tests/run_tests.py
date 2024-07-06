import sys
import pytest


def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    pytest.main(args)


if __name__ == "__main__":
    main()
