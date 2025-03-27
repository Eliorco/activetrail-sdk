#!/usr/bin/env python
"""
Test runner for the ActiveTrail SDK - runs all tests with coverage report.
"""

import unittest
import sys
import coverage

cov = coverage.Coverage(
    source=["active_trail"],
    omit=["*/__pycache__/*", "*/tests/*", "*/site-packages/*"]
)
cov.start()

# Import all test modules
from test_client import TestActiveTrailClient
from test_base_api import (
    TestBaseAPI, 
    TestCrudAPI, 
    TestNestedResourceAPI, 
    TestCampaignBaseAPI
)
from test_groups import TestGroupsAPI
from test_contacts import TestContactsAPI
from test_utils import TestUtils


def create_test_suite():
    """Create and return a test suite of all tests."""
    # Initialize the test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests to the suite
    suite.addTests(loader.loadTestsFromTestCase(TestActiveTrailClient))
    suite.addTests(loader.loadTestsFromTestCase(TestBaseAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestCrudAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestNestedResourceAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestCampaignBaseAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestGroupsAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestContactsAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    
    return suite


if __name__ == "__main__":
    """Run all tests and show coverage report."""
    # Create the test suite
    suite = create_test_suite()
    
    # Run the tests
    print("Running tests...")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Stop coverage and print report
    cov.stop()
    cov.save()
    
    print("\nCoverage report:")
    cov.report()
    
    # Return non-zero exit code on test failures
    sys.exit(not result.wasSuccessful()) 