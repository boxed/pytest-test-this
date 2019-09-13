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

    # run all tests
    result = testdir.runpytest('-v')
    assert 'collecting ... collected 2 items' in result.outlines
    result.assert_outcomes(passed=2)

    # filter the tests
    # assert 'collecting ... collected test_foo' in testdir.runpytest('--test-this=foo', '-v').outlines

    result = testdir.runpytest('--test-this=foo', '-v')
    result.assert_outcomes(passed=1)


