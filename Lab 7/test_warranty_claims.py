import math
from hypothesis import given, strategies as st
from warranty_claims import parse_claim, age_average, payable_charge

@given(st.text() | st.none())
def test_parse_claim_no_crash(s):
    try:
        parse_claim(s)
    except Exception as e:
        assert False, f"parse_claim crashed with: {e}"

@given(st.text() | st.none())
def test_age_average_no_crash(s):
    try:
        age_average(s)
    except Exception as e:
        assert False, f"age_average crashed with: {e}"

@given(st.text() | st.none())
def test_payable_charge_no_crash(s):
    try:
        payable_charge(s)
    except Exception as e:
        assert False, f"payable_charge crashed with: {e}"


# inputs in the expected format, to get past the split and reach the logic

@given(st.text(), st.floats())
def test_parse_claim_valid_months(plan, months):
    result = parse_claim(f"{plan}:{months}")
    if result is not None:
        assert math.isfinite(result[1]) and result[1] >= 0, f"bad months: {result}"

@given(st.lists(st.integers()))
def test_age_average_non_negative(ages):
    result = age_average(",".join(str(a) for a in ages))
    if result is not None:
        assert result >= 0, f"negative average: {result}"

@given(st.floats(), st.floats())
def test_payable_charge_valid_total(charge, discount):
    result = payable_charge(f"{charge}|{discount}")
    if result is not None:
        assert math.isfinite(result) and result >= 0, f"bad total: {result}"
