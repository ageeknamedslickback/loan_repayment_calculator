"""Optimized loan calculator without redundant and unnecessary computations."""
from dataclasses import dataclass
from decimal import Decimal

VALID_FREQUENCIES = ["monthly", "bi-monthly", "weekly"]
MONTHS_PER_YEAR = 12


@dataclass
class LoanCalculatorV2:
    """Loan calculator object."""

    loan_amount: Decimal
    loan_term_months: int
    annual_interest_rate: float
    repayment_frequency: str

    def __post_init__(self) -> None:
        """Initialize the object and sanitize it's inputs."""
        self.validate_input()

        # Avoid recalculating these in multiple places
        self.monthly_interest_rate = self.calculate_monthly_interest_rate()
        self.number_of_repayments = self.calculate_number_of_repayments()

    def validate_input(self) -> None:
        """Ensure correct inputs are provided before proceeding."""
        if (
            self.loan_amount <= Decimal(0)
            or self.loan_term_months <= 0
            or self.annual_interest_rate <= 0
        ):
            raise ValueError(
                "Loan amount, loan term, and annual interest rate "
                "must be positive values."
            )

        if self.repayment_frequency not in VALID_FREQUENCIES:
            raise ValueError(
                "Invalid repayment frequency. "
                "Use 'monthly', 'bi-monthly', or 'weekly'."
            )

    def calculate_monthly_interest_rate(self) -> Decimal:
        """Calculate the monthly interest rateapplied to the loan."""
        return Decimal(
            self.annual_interest_rate / (100 * MONTHS_PER_YEAR)
        )  # Return a decimal here to avoid expensive conversions

    def calculate_number_of_repayments(self) -> int:
        """Calculate number of repayments from the frequency and months."""
        match self.repayment_frequency:
            case "monthly":
                num_repayments = self.loan_term_months

            case "bi-monthly":
                num_repayments = self.loan_term_months // 2

            case "weekly":
                num_repayments = self.loan_term_months * 4

        return num_repayments

    def calculate_monthly_repayment(self) -> Decimal:
        """Perform the actual loan calculations."""
        interest_rate_per_month = self.monthly_interest_rate
        monthly_repayment = (
            self.loan_amount
            * interest_rate_per_month
            / (1 - (1 + interest_rate_per_month) ** -self.number_of_repayments)
        )

        return Decimal(monthly_repayment)

    def calculate_loan(self) -> dict:
        """Calculate a loan's schedule and it's information."""
        remaining_balance = self.loan_amount
        total_interest_paid = Decimal(0)
        repayment_schedule = []

        number_of_repayments = self.number_of_repayments
        monthly_interest_rate = self.monthly_interest_rate
        monthly_repayment = self.calculate_monthly_repayment()
        for month in range(1, number_of_repayments + 1):
            monthly_interest = remaining_balance * monthly_interest_rate
            monthly_principal = monthly_repayment - monthly_interest
            total_interest_paid += monthly_interest
            remaining_balance -= monthly_principal
            repayment_schedule.append(
                {
                    "month": month,
                    "payment": monthly_repayment,
                    "principal": monthly_principal,
                    "interest": monthly_interest,
                    "balance": remaining_balance,
                }
            )
        total_amount_repaid = self.loan_amount + total_interest_paid
        return {
            "loan_amount": self.loan_amount,
            "loan_term_in_months": self.loan_term_months,
            "annual_interest_rate": self.annual_interest_rate,
            "repayment_frequency": self.repayment_frequency,
            "repayment_schedule": repayment_schedule,
            "total_interest_paid": total_interest_paid,
            "total_amount_repaid": total_amount_repaid,
        }  # Remove redundant round functions for optimization
