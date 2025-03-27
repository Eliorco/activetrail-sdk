# Contributing to ActiveTrail SDK

Thank you for your interest in contributing to the ActiveTrail SDK! This document provides guidelines and instructions to help you get started with contributing to the project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. Harassment or abusive behavior will not be tolerated.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork to your local machine
3. Create a new branch for your feature or bug fix
4. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### Code Style

We follow PEP 8 guidelines for Python code style. Additionally:

- Use descriptive variable names
- Add docstrings to all functions and classes following Google style
- Keep lines at 88 characters or less
- Use type annotations where possible

You can use the following tools to check and format your code:

```bash
# Format code with Black
black active_trail/

# Check imports with isort
isort active_trail/

# Check code with flake8
flake8 active_trail/

# Check type hints with mypy
mypy active_trail/
```

### Testing

Always add tests for new features or bug fixes. Run the tests locally before submitting a pull request:

```bash
# Run all tests
python tests/run_all_tests.py

# Run specific tests
python -m unittest tests/test_client.py

# Run with pytest
pytest tests/
```

Aim for high test coverage and make sure all tests pass before submitting your PR.

### Pull Request Process

1. Update the README.md or documentation with details of changes if needed
2. Run all tests and ensure they pass
3. Make sure your code follows the style guidelines
4. Submit a pull request to the main branch
5. The maintainers will review your PR as soon as possible

### Commit Messages

Use clear and meaningful commit messages that explain what changes you've made and why. Format your commit messages like this:

```
[Component] Short summary of changes

More detailed explanation if necessary
```

For example:
```
[Client] Add error handling for rate limiting

Added proper retry mechanism with exponential backoff
for handling API rate limits to prevent request failures.
```

## Adding New Features

When adding new features to the SDK:

1. Check if the feature aligns with the project's goals
2. Discuss major changes by opening an issue first
3. Follow the existing patterns and architecture
4. Add comprehensive tests
5. Update documentation

## Reporting Bugs

If you find a bug, please create an issue on GitHub with:

1. A clear description of the bug
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Screenshots or code examples if applicable
6. Environment details (Python version, OS, etc.)

## Feature Requests

For feature requests, create an issue on GitHub with:

1. A clear description of the feature
2. The motivation behind the feature
3. Examples of how the feature would be used
4. Any additional context or information

## Documentation

Good documentation is crucial. When contributing:

1. Update the docstrings for any modified code
2. Update the README.md if needed
3. Add examples for new features
4. Keep the documentation clear and concise

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License. 