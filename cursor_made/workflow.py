"""
Loan Application Workflow
Orchestrates the five-step loan processing pipeline
"""
from datetime import timedelta
from temporalio import workflow

# Import activity types
with workflow.unsafe.imports_passed_through():
    from activities import (
        collect_docs,
        credit_check,
        property_valuation,
        underwriter_review,
        sign_agreement,
        DocumentCollection,
        CreditCheckResult,
        PropertyValuation,
        UnderwriterDecision,
        SignedAgreement
    )


@workflow.defn(name="LoanApplicationWorkflow")
class LoanApplicationWorkflow:
    """
    Main workflow that orchestrates the loan application process
    through five sequential states
    """
    
    @workflow.run
    async def run(
        self,
        applicant_name: str,
        property_address: str,
        requested_loan_amount: float
    ) -> dict:
        """
        Execute the complete loan application workflow
        
        Args:
            applicant_name: Name of the loan applicant
            property_address: Address of the property to be purchased
            requested_loan_amount: Amount of loan requested
            
        Returns:
            Dictionary containing the complete workflow results
        """
        workflow.logger.info(f"Starting loan application workflow for {applicant_name}")
        
        # State 1: Collect Documents
        workflow.logger.info("State 1: Collecting documents...")
        docs: DocumentCollection = await workflow.execute_activity(
            collect_docs,
            applicant_name,
            start_to_close_timeout=timedelta(seconds=30),
        )
        workflow.logger.info(f"✓ Documents collected: {len(docs.documents)} items")
        
        # State 2: Credit Check
        workflow.logger.info("State 2: Running credit check...")
        credit: CreditCheckResult = await workflow.execute_activity(
            credit_check,
            applicant_name,
            start_to_close_timeout=timedelta(seconds=30),
        )
        workflow.logger.info(f"✓ Credit check complete: Score={credit.credit_score}")
        
        # Check if credit check passed
        if not credit.approved:
            workflow.logger.warning(f"Credit check failed. Score: {credit.credit_score}")
            return {
                "status": "REJECTED",
                "reason": "Insufficient credit score",
                "credit_score": credit.credit_score,
                "stage": "credit_check"
            }
        
        # State 3: Property Valuation
        workflow.logger.info("State 3: Conducting property valuation...")
        valuation: PropertyValuation = await workflow.execute_activity(
            property_valuation,
            property_address,
            start_to_close_timeout=timedelta(seconds=45),
        )
        workflow.logger.info(f"✓ Property valued at: ${valuation.estimated_value:,.2f}")
        
        # State 4: Underwriter Review
        workflow.logger.info("State 4: Underwriter reviewing application...")
        decision: UnderwriterDecision = await workflow.execute_activity(
            underwriter_review,
            args=[credit.credit_score, valuation.estimated_value, requested_loan_amount],
            start_to_close_timeout=timedelta(seconds=30),
        )
        workflow.logger.info(f"✓ Underwriter decision: {decision.decision}")
        
        # Check underwriter decision
        if decision.decision == "DECLINED":
            workflow.logger.warning("Application declined by underwriter")
            return {
                "status": "REJECTED",
                "reason": "Application declined by underwriter",
                "stage": "underwriter_review"
            }
        
        # State 5: Sign Agreement
        workflow.logger.info("State 5: Finalizing loan agreement...")
        agreement: SignedAgreement = await workflow.execute_activity(
            sign_agreement,
            args=[applicant_name, decision.loan_amount_approved],
            start_to_close_timeout=timedelta(seconds=30),
        )
        workflow.logger.info(f"✓ Agreement signed: {agreement.agreement_id}")
        
        # Return complete workflow result
        workflow.logger.info("Loan application workflow completed successfully!")
        
        return {
            "status": "APPROVED",
            "applicant_name": applicant_name,
            "property_address": property_address,
            "requested_amount": requested_loan_amount,
            "approved_amount": decision.loan_amount_approved,
            "interest_rate": decision.interest_rate,
            "credit_score": credit.credit_score,
            "property_value": valuation.estimated_value,
            "agreement_id": agreement.agreement_id,
            "underwriter_decision": decision.decision,
            "documents_collected": docs.documents,
            "final_message": agreement.final_status
        }

