def test_plugin(testdir):

    # create a temporary pytest test file
    testdir.makepyfile(
        """
        def foo():
            return 0
        
        def bar():
            return 1
        
        def test_foo():
            assert foo() == 0

        def test_bar():
            assert bar() == 1
    """
    )

    # run all tests with pytest
    result = testdir.runpytest('--test-this=foo')

    # check that all 4 tests passed
    result.assert_outcomes(passed=1)
