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
    applicant_name = "Chandrahaas Jasti"
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
        args=[applicant_name],
        id=workflow_id,
        task_queue="loan-application-queue",
    )
    
    # Print results
    print("\n" + "=" * 70)
    print("📊 WORKFLOW RESULTS")
    print("=" * 70)
    
    print(f"Status: {result['status']}")
    print(f"Applicant Name: {result['applicant_name']}")
    print(f"Customer ID: {result['customer_id']}")
    print(f"Payment Status: {result['payment_status']}")
    print(f"Credit Score: {result['credit_score']}")
    print(f"Documents Collected: {result['docs']}")
    print(f"Message: {result['message']}")
    
    # Show error if present
    if result['status'] == 'FAILED' and 'error' in result:
        print(f"⚠️  Error: {result['error']}")
    
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

