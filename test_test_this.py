def test_plugin(testdir):

    # create a temporary pytest test file
    testdir.makepyfile(
        """
        def foo():
            return 0
        
        def bar():
            return 1
            
        def baz():
            return 2
        
        def test_foo():
            assert foo() == 0

        def test_bar():
            assert bar() == 1

        def test_baz():
            assert baz() == 2
    """
    )

    # run all tests
    result = testdir.runpytest('-v')
    assert 'collecting ... collected 3 items' in result.outlines
    result.assert_outcomes(passed=3)

    # filter one test
    result = testdir.runpytest('--test-this=foo', '-v')
    result.assert_outcomes(passed=1)

    # filter two tests
    result = testdir.runpytest('--test-this=foo,bar', '-v')
    result.assert_outcomes(passed=2)


