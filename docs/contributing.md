# Contributing to Langrade

We welcome contributions to Langrade! Here's how you can help:

## Setting Up the Development Environment

1. Fork the repository
2. Clone your fork:

```bash
git clone https://github.com/yourusername/langrade.git
cd langrade
```

3. Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4. Install dependencies:

```bash
pip install -e ".[dev]"
```

## Running Tests

Run tests using pytest:

```bash
poetry run test
```

## Coding Standards

We use Black for code formatting and flake8 for linting:

```bash
black .
flake8
```

## Submitting Changes

Create a new branch:

`git checkout -b your-branch-name`

Make your changes and commit them:

`git commit -m "Your detailed commit message"`

Push to your fork:

`git push origin your-branch-name`

Submit a pull request

Please ensure your code adheres to our coding standards and is well-documented.

Thank you for contributing to Langrade!
