from decimal import Decimal
import pytest

from calculator import LoanCalculator


def test_input_data_validation():
    """Verify all inputs are positive values."""
    loan_amount = 1000
    loan_term_months = -10
    annual_interest_rate = 15.6
    repayment_frequency = "monthly"

    with pytest.raises(ValueError) as e:
        calculator = LoanCalculator(
            loan_amount=loan_amount,
            loan_term_months=loan_term_months,
            annual_interest_rate=annual_interest_rate,
            repayment_frequency=repayment_frequency,
        )

    assert e
    assert str(e.value) == (
        "Loan amount, loan term, and annual interest "
        "rate must be positive values."
    )


def test_validate_payment_frequency():
    """Verify the given payment frequency."""
    loan_amount = 1000
    loan_term_months = 10
    annual_interest_rate = 15.6
    repayment_frequency = "tri-monthly"

    with pytest.raises(ValueError) as e:
        calculator = LoanCalculator(
            loan_amount=loan_amount,
            loan_term_months=loan_term_months,
            annual_interest_rate=annual_interest_rate,
            repayment_frequency=repayment_frequency,
        )

    assert e
    assert str(e.value) == (
        "Invalid repayment frequency. "
        "Use 'monthly', 'bi-monthly', or 'weekly'."
    )


def test_monthly_loan_calculator():
    """Verify calculation of a monthly loan."""
    loan_amount = 1000
    loan_term_months = 10
    annual_interest_rate = 15.6
    repayment_frequency = "monthly"

    calculator = LoanCalculator(
        loan_amount=loan_amount,
        loan_term_months=loan_term_months,
        annual_interest_rate=annual_interest_rate,
        repayment_frequency=repayment_frequency,
    )
    results = calculator.calculate_loan()

    assert results
    assert len(results["repayment_schedule"]) == 10
    assert results["loan_amount"] == 1000
    assert results["total_interest_paid"] == round(Decimal(72.88), 2)
    assert results["total_amount_repaid"] == round(Decimal(1072.88), 2)


def test_bi_monthly_loan_calculator():
    """Verify calculation of a bi-monthly loan."""
    loan_amount = 1000
    loan_term_months = 10
    annual_interest_rate = 15.6
    repayment_frequency = "bi-monthly"

    calculator = LoanCalculator(
        loan_amount=loan_amount,
        loan_term_months=loan_term_months,
        annual_interest_rate=annual_interest_rate,
        repayment_frequency=repayment_frequency,
    )
    results = calculator.calculate_loan()

    assert results
    assert len(results["repayment_schedule"]) == 5
    assert results["loan_amount"] == 1000
    assert results["total_interest_paid"] == round(Decimal(39.34), 2)
    assert results["total_amount_repaid"] == round(Decimal(1039.34), 2)


def test_weekly_loan_calculator():
    """Verify calculation of a weekly loan."""
    loan_amount = 1000
    loan_term_months = 10
    annual_interest_rate = 15.6
    repayment_frequency = "weekly"

    calculator = LoanCalculator(
        loan_amount=loan_amount,
        loan_term_months=loan_term_months,
        annual_interest_rate=annual_interest_rate,
        repayment_frequency=repayment_frequency,
    )
    results = calculator.calculate_loan()

    assert results
    assert len(results["repayment_schedule"]) == 40
    assert results["loan_amount"] == 1000
    assert results["total_interest_paid"] == round(Decimal(288.78), 2)
    assert results["total_amount_repaid"] == round(Decimal(1288.78), 2)
