from temporalio import activity
import asyncio
from dataclasses import dataclass

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
async def collect_docs(applicant_name: str):
    pass

@activity.defn(name="credit_check")
async def credit_check(applicant_name: str):
    pass

@activity.defn(name="login_fee")
async def login_fee(applicant_name: str):
    pass

@activity.defn(name="property_valuation")
async def property_valuation(applicant_name: str):
    pass

@activity.defn(name="new_lead")
async def new_lead(applicant_name: str):
    pass