# ActiveTrail SDK Tests

This directory contains tests for the ActiveTrail SDK. The tests are organized by module, corresponding to the structure of the SDK itself.

## Test Structure

- `test_client.py`: Tests for the core client functionality
- `test_base_api.py`: Tests for the base API classes
- `test_groups.py`: Tests for the Groups API
- `test_two_way_sms.py`: Tests for the Two-Way SMS API
- `test_sms_reports.py`: Tests for the SMS Reports API
- `run_all_tests.py`: Script to run all tests with coverage reporting

## Running the Tests

### Run All Tests

To run all tests with coverage report:

```bash
python tests/run_all_tests.py
```

### Run Specific Test File

To run tests from a specific file:

```bash
python -m unittest tests/test_client.py
```

### Run with pytest

You can also use pytest to run the tests:

```bash
pytest tests/
```

For coverage report with pytest:

```bash
pytest --cov=active_trail tests/
```

## Adding New Tests

When adding new functionality to the SDK, please add corresponding tests. Each test file should contain test cases for the corresponding module in the SDK.

Test files should follow these conventions:

1. Name the test file `test_<module_name>.py`
2. Create a test class named `Test<ModuleName>`
3. Add test methods prefixed with `test_`
4. Include docstrings for test classes and methods
5. Use `unittest.mock` for mocking external dependencies

## Test Coverage Requirements

The goal is to maintain at least 80% test coverage for the SDK. This includes:

- Unit tests for all public methods
- Tests for error handling scenarios
- Tests for edge cases

## Dependencies

The test suite requires the packages listed in `requirements-dev.txt`. Install them using:

```bash
pip install -r requirements-dev.txt
``` 