"""
Workflow Client
Starts a new loan application workflow
"""
import asyncio
import sys
from temporalio.client import Client


async def main():
    """
    Start a loan application workflow
    """
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    # Loan application details
    applicant_name = "John Doe"
    property_address = "123 Main Street, San Francisco, CA 94102"
    requested_loan_amount = 350000.00
    
    print("=" * 70)
    print("🏦 LOAN APPLICATION WORKFLOW")
    print("=" * 70)
    print(f"Applicant: {applicant_name}")
    print(f"Property: {property_address}")
    print(f"Requested Amount: ${requested_loan_amount:,.2f}")
    print("=" * 70)
    print("\n🚀 Starting workflow execution...\n")
    
    # Start the workflow
    workflow_id = f"loan-application-{applicant_name.replace(' ', '-').lower()}"
    
    result = await client.execute_workflow(
        "LoanApplicationWorkflow",
        args=[applicant_name, property_address, requested_loan_amount],
        id=workflow_id,
        task_queue="loan-application-queue",
    )
    
    # Print results
    print("\n" + "=" * 70)
    print("📊 WORKFLOW RESULTS")
    print("=" * 70)
    
    if result["status"] == "APPROVED":
        print(f"✅ Status: {result['status']}")
        print(f"📝 Agreement ID: {result['agreement_id']}")
        print(f"💰 Approved Amount: ${result['approved_amount']:,.2f}")
        print(f"📊 Interest Rate: {result['interest_rate']}%")
        print(f"🏠 Property Value: ${result['property_value']:,.2f}")
        print(f"📈 Credit Score: {result['credit_score']}")
        print(f"⚖️  Underwriter Decision: {result['underwriter_decision']}")
        print(f"\n📄 Documents Collected:")
        for doc in result['documents_collected']:
            print(f"   - {doc}")
        print(f"\n✨ {result['final_message']}")
    else:
        print(f"❌ Status: {result['status']}")
        print(f"⚠️  Reason: {result['reason']}")
        print(f"🚫 Failed at stage: {result['stage']}")
    
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

