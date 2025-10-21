from temporalio import activity
import asyncio
from dataclasses import dataclass
from datetime import datetime

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

# @activity.defn(name="credit_check")
# async def credit_check(applicant_name: str):
#     pass

# @activity.defn(name="login_fee")
# async def login_fee(applicant_name: str):
#     pass

# @activity.defn(name="property_valuation")
# async def property_valuation(applicant_name: str):
#     pass

# @activity.defn(name="new_lead")
# async def new_lead(applicant_name: str):
#     pass

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

asyncio.run(collect_docs("John Doe"))