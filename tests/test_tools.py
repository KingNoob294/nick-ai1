from nick_ai.tools.calculator import calculate


def test_calculator_arithmetic():
    assert calculate("12*(3+4)") == "84"


def test_calculator_rejects_code():
    try:
        calculate("__import__('os').system('echo unsafe')")
    except ValueError:
        pass
    else:
        raise AssertionError("arbitrary code must be rejected")
