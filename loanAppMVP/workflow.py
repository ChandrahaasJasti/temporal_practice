from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta

with workflow.unsafe.imports_passed_through():
    from activities import (
        collect_docs,
        credit_check,
        login_fee,
        finalizer,
        PaymentFailedException
    )

@workflow.defn(name="LoanApplicationWorkflow")
class LoanApplicationWorkflow:

    @workflow.run
    async def run(self, applicant_name: str) -> dict:
        workflow.logger.info(f"Starting loan application workflow for {applicant_name}")
        
        # Step 1: Collect documents
        docs = await workflow.execute_activity(
            collect_docs,
            applicant_name,
            start_to_close_timeout=timedelta(seconds=30),
        )
        
        # Step 2: Run credit check
        credit = await workflow.execute_activity(
            credit_check,
            applicant_name,
            start_to_close_timeout=timedelta(seconds=30),
        )

        # Step 3: Process login fee with retry policy (max 3 attempts)
        # Configure retry policy for payment processing
        payment_retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),  # Wait 1 second before first retry
            backoff_coefficient=2.0,                 # Double the wait time with each retry
            maximum_interval=timedelta(seconds=5),   # Max 5 seconds between retries
            maximum_attempts=3                       # Try maximum 3 times (1 initial + 2 retries)
        )
        
        try:
            customer_id = await workflow.execute_activity(
                login_fee,
                applicant_name,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=payment_retry_policy
            )
            workflow.logger.info(f"Payment successful for {applicant_name}")
            
            # Step 4: Finalize customer creation
            final_customer_id = await workflow.execute_activity(
                finalizer,
                customer_id,
                start_to_close_timeout=timedelta(seconds=30),
            )
            
            return {
                "status": "SUCCESS",
                "applicant_name": applicant_name,
                "customer_id": final_customer_id,
                "docs": docs.documents,
                "credit_score": credit.credit_score,
                "payment_status": "COMPLETED",
                "message": f"Successfully processed application for {applicant_name}"
            }
            
        except Exception as e:
            # Payment failed after all retry attempts (3 attempts)
            workflow.logger.error(f"Payment processing failed after all retry attempts: {e}")
            
            return {
                "status": "FAILED",
                "applicant_name": applicant_name,
                "customer_id": None,
                "docs": docs.documents,
                "credit_score": credit.credit_score,
                "payment_status": "FAILED",
                "error": str(e),
                "message": f"Payment processing failed for {applicant_name} after 3 attempts"
            }