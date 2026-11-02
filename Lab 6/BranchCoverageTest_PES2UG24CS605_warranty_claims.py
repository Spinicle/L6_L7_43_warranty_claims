import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# ---- out_of_warranty_charge ----

def test_within_warranty():
    assert out_of_warranty_charge("standard", 20, "defect", False) == 0

def test_unknown_plan():
    with pytest.raises(ValueError):
        out_of_warranty_charge("gold", 5, "defect", False)

def test_negative_age():
    with pytest.raises(ValueError):
        out_of_warranty_charge("basic", -1, "defect", False)

def test_registered_accidental_long_excess():
    # basic 12 + 6 (registered) = 18 months, excess 22, rate 200 + 50 + 25
    assert out_of_warranty_charge("basic", 40, "accidental", True) == 22 * 275

def test_defect_short_excess():
    # standard 24 months, excess 6, rate 100
    assert out_of_warranty_charge("standard", 30, "defect", False) == 600

def test_defect_long_excess():
    # excess 16 > 12 but not accidental, so no extra 25 (rate 150)
    assert out_of_warranty_charge("standard", 40, "defect", False) == 16 * 150

def test_registered_premium_no_extension():
    # premium stays at 36 months even when registered
    assert out_of_warranty_charge("premium", 40, "defect", True) == 400

def test_excess_exactly_zero():
    # standard 24 + 6 = 30, age 30 -> still covered
    assert out_of_warranty_charge("standard", 30, "defect", True) == 0

def test_excess_exactly_twelve():
    # excess 12 is not > 12, so no surcharge
    assert out_of_warranty_charge("basic", 24, "accidental", False) == 12 * 200


# ---- claim_allowed ----

def test_claim_allowed():
    assert claim_allowed(60, 1, False) is True

def test_recall_claim():
    assert claim_allowed(10, 5, True) is True

def test_recall_over_limit():
    assert claim_allowed(10, 6, True) is False

def test_claim_too_soon():
    assert claim_allowed(10, 1, False) is False

def test_too_many_claims():
    # 30 days is allowed, but 3 claims is over the limit of 2
    assert claim_allowed(30, 3, False) is False


# ---- sla_status ----

def test_sla_on_track_hardware_priority():
    # cutoff 48 + 24 = 72
    assert sla_status(80, True, True) == "on_track"

def test_sla_at_risk():
    # cutoff 24, at_risk from 12 to 23
    assert sla_status(15, False, False) == "at_risk"

def test_sla_critical():
    assert sla_status(5, False, False) == "critical"

def test_sla_exact_cutoff():
    assert sla_status(48, True, False) == "on_track"

def test_sla_cutoff_minus_twelve():
    assert sla_status(36, True, False) == "at_risk"
