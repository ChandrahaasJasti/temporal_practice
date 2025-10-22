from temporalio import activity
import asyncio
from dataclasses import dataclass
from datetime import datetime
import random


# Custom exception for payment failures
class PaymentFailedException(Exception):
    """Raised when payment processing fails"""
    pass

@dataclass
class DocumentCollection:
    applicant_name: str
    documents: list[str]
    collected_at: str
    status: str

@dataclass
class CreditCheck:
    applicant_name: str
    credit_score: int
    credit_history: str
    checked_at: str
    status: str

@activity.defn(name="collect_docs")
async def collect_docs(applicant_name: str) -> DocumentCollection:
    aadhar_task=asyncio.create_task(fetch(applicant_name,type="aadhar" ))
    pan_task=asyncio.create_task(fetch(applicant_name,type="pan"))
    bank_statement_task=asyncio.create_task(fetch(applicant_name,type="bank_statement"))
    income_statement_task=asyncio.create_task(fetch(applicant_name,type="income_statement"))
    tax_return_task=asyncio.create_task(fetch(applicant_name,type="tax_return"))
    aadhar=await aadhar_task
    pan=await pan_task
    bank_statement=await bank_statement_task
    income_statement=await income_statement_task
    tax_return=await tax_return_task
    documents=[aadhar, pan, bank_statement, income_statement, tax_return]
    print(documents)
    result = DocumentCollection(
        applicant_name=applicant_name,
        documents=documents,
        collected_at=datetime.now().isoformat(),
        status="Documents collected successfully"
    )
    return result

@activity.defn(name="credit_check")
async def credit_check(applicant_name: str) -> CreditCheck:
    credit_score=asyncio.create_task(fetch(applicant_name,type="credit_score"))
    credit_history=asyncio.create_task(fetch(applicant_name,type="credit_history"))
    credit_score=await credit_score
    credit_history=await credit_history
    checked_at=datetime.now().isoformat()
    status="Credit check completed successfully"
    result = CreditCheck(
        applicant_name=applicant_name,
        credit_score=credit_score,
        credit_history=credit_history,
        checked_at=checked_at,
        status=status
    )
    return result

@activity.defn(name="login_fee")
async def login_fee(applicant_name: str) -> str:
    """
    Activity to process login fee payment
    Raises PaymentFailedException if payment fails (will trigger retry)
    """
    activity.logger.info(f"Processing login fee payment for {applicant_name}")
    
    task = asyncio.create_task(generate_payment_link(applicant_name))
    payment_completion = await task
    
    if payment_completion:
        activity.logger.info("Payment completed successfully, converting lead into a customer")
        customer_id = "SFC012"
        activity.logger.info(f"Customer ID generated: {customer_id}")
        return customer_id
    else:
        # Raise exception instead of returning empty string
        # This will trigger Temporal's retry mechanism
        activity.logger.warning(f"Payment failed for {applicant_name}")
        raise PaymentFailedException(f"Payment processing failed for applicant: {applicant_name}")


@activity.defn(name="finalizer")
async def finalizer(customer_id: str) -> str:
    if(customer_id == "SFC012"):
        print("Customer is new, creating a new customer")
        print("returning customer id")
        return "SFC012"
    else:
        print("failed to convert lead into a customer")
        return ""

"""
-----------------------------------------------------------------------------------------------------------------
"""

async def fetch(applicant_name: str, type: str):
    if type == "aadhar":
        await asyncio.sleep(5)
        return "509239684498"
    elif type == "pan":
        await asyncio.sleep(1)
        return "ABCD123456"
    elif type == "bank_statement":
        await asyncio.sleep(3)
        return "1234567890"
    elif type == "income_statement":
        await asyncio.sleep(2)
        return "100000"
    elif type == "tax_return":
        return "1000000"
    elif type == "credit_score":
        await asyncio.sleep(1)
        return 750
    elif type == "credit_history":
        await asyncio.sleep(1)
        return "Good standing, no defaults"

async def generate_payment_link(applicant_name: str) -> str:
    await asyncio.sleep(1)
    if random.randint(0, 100) < 30:
        return True
    else:
        return False

asyncio.run(collect_docs("John Doe"))