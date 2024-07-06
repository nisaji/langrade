import pytest
import os


def main():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    pytest.main([test_dir])


if __name__ == "__main__":
    main()
