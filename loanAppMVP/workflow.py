from temporalio import workflow
from datetime import timedelta
with workflow.unsafe.imports_passed_through():
    from activities import (
        collect_docs,
        credit_check,
        login_fee,
        finalizer
    )

@workflow.defn(name="LoanApplicationWorkflow")
class LoanApplicationWorkflow:

    @workflow.run
    async def run(self, applicant_name: str) -> str:
        print(f"Starting loan application workflow for {applicant_name}")
        docs = await workflow.execute_activity(
            collect_docs,
            applicant_name,
            start_to_close_timeout=timedelta(seconds=30),
        )
        credit = await workflow.execute_activity(
            credit_check,
            applicant_name,
            start_to_close_timeout=timedelta(seconds=30),
        )

        customer_id = await workflow.execute_activity(
            login_fee,
            applicant_name,
            start_to_close_timeout=timedelta(seconds=30),
        )

        final_customer_id = await workflow.execute_activity(
            finalizer,
            customer_id,
            start_to_close_timeout=timedelta(seconds=30),
        )

        return {
            "applicant_name": applicant_name,
            "customer_id": final_customer_id,
            "docs": docs.documents,
            "credit_score": credit.credit_score,
            "login_fee_status": customer_id,
            "finalizer_status": final_customer_id,
        }