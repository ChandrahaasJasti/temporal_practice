"""
Loan Application Activities
Each activity represents a step in the loan processing pipeline
"""
import asyncio
from dataclasses import dataclass
from datetime import datetime
from temporalio import activity


@dataclass
class DocumentCollection:
    applicant_name: str
    documents: list[str]
    collected_at: str
    status: str


@dataclass
class CreditCheckResult:
    credit_score: int
    credit_history: str
    approved: bool
    checked_at: str


@dataclass
class PropertyValuation:
    property_address: str
    estimated_value: float
    appraised_by: str
    valuation_date: str


@dataclass
class UnderwriterDecision:
    decision: str
    loan_amount_approved: float
    interest_rate: float
    reviewed_by: str
    reviewed_at: str


@dataclass
class SignedAgreement:
    agreement_id: str
    signed: bool
    signed_at: str
    final_status: str


@activity.defn(name="collect_docs")
async def collect_docs(applicant_name: str) -> DocumentCollection:
    """
    Activity 1: Collect required documents from applicant
    """
    activity.logger.info(f"Starting document collection for {applicant_name}")
    
    # Simulate document collection process
    await asyncio.sleep(2)
    
    documents = [
        "Identity Proof",
        "Income Statement",
        "Tax Returns",
        "Property Documents",
        "Bank Statements"
    ]
    
    result = DocumentCollection(
        applicant_name=applicant_name,
        documents=documents,
        collected_at=datetime.now().isoformat(),
        status="Documents Collected Successfully"
    )
    
    activity.logger.info(f"Collected {len(documents)} documents for {applicant_name}")
    return result


@activity.defn(name="credit_check")
async def credit_check(applicant_name: str) -> CreditCheckResult:
    """
    Activity 2: Perform credit check on the applicant
    """
    activity.logger.info(f"Running credit check for {applicant_name}")
    
    # Simulate credit check API call
    await asyncio.sleep(3)
    
    # Simulated credit score (in real scenario, would call credit bureau API)
    credit_score = 750  # Good credit score
    
    result = CreditCheckResult(
        credit_score=credit_score,
        credit_history="Good standing, no defaults",
        approved=credit_score >= 650,
        checked_at=datetime.now().isoformat()
    )
    
    activity.logger.info(f"Credit check complete: Score={credit_score}, Approved={result.approved}")
    return result


@activity.defn(name="property_valuation")
async def property_valuation(property_address: str) -> PropertyValuation:
    """
    Activity 3: Conduct property valuation
    """
    activity.logger.info(f"Starting property valuation for {property_address}")
    
    # Simulate property valuation process
    await asyncio.sleep(4)
    
    # Simulated property value
    estimated_value = 450000.00
    
    result = PropertyValuation(
        property_address=property_address,
        estimated_value=estimated_value,
        appraised_by="Certified Property Appraiser Inc.",
        valuation_date=datetime.now().isoformat()
    )
    
    activity.logger.info(f"Property valuation complete: ${estimated_value:,.2f}")
    return result


@activity.defn(name="underwriter_review")
async def underwriter_review(
    credit_score: int,
    property_value: float,
    requested_amount: float
) -> UnderwriterDecision:
    """
    Activity 4: Underwriter reviews the loan application
    """
    activity.logger.info(f"Underwriter reviewing loan application")
    activity.logger.info(f"Credit Score: {credit_score}, Property Value: ${property_value:,.2f}, Requested: ${requested_amount:,.2f}")
    
    # Simulate underwriter review
    await asyncio.sleep(3)
    
    # Decision logic
    loan_to_value_ratio = requested_amount / property_value
    
    if credit_score >= 750 and loan_to_value_ratio <= 0.80:
        decision = "APPROVED"
        loan_amount = requested_amount
        interest_rate = 3.5
    elif credit_score >= 680 and loan_to_value_ratio <= 0.75:
        decision = "APPROVED_WITH_CONDITIONS"
        loan_amount = requested_amount * 0.95
        interest_rate = 4.2
    else:
        decision = "DECLINED"
        loan_amount = 0.0
        interest_rate = 0.0
    
    result = UnderwriterDecision(
        decision=decision,
        loan_amount_approved=loan_amount,
        interest_rate=interest_rate,
        reviewed_by="Senior Underwriter",
        reviewed_at=datetime.now().isoformat()
    )
    
    activity.logger.info(f"Underwriter decision: {decision}")
    return result


@activity.defn(name="sign_agreement")
async def sign_agreement(applicant_name: str, loan_amount: float) -> SignedAgreement:
    """
    Activity 5: Finalize and sign loan agreement
    """
    activity.logger.info(f"Processing loan agreement signature for {applicant_name}")
    
    # Simulate agreement signing process
    await asyncio.sleep(2)
    
    agreement_id = f"LOAN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    result = SignedAgreement(
        agreement_id=agreement_id,
        signed=True,
        signed_at=datetime.now().isoformat(),
        final_status=f"Loan of ${loan_amount:,.2f} approved and agreement signed"
    )
    
    activity.logger.info(f"Agreement signed: {agreement_id}")
    return result

