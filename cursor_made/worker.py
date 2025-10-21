"""
Temporal Worker
Polls for tasks and executes workflows and activities
"""
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from workflow import LoanApplicationWorkflow
from activities import (
    collect_docs,
    credit_check,
    property_valuation,
    underwriter_review,
    sign_agreement
)


async def main():
    """
    Start the Temporal worker
    """
    # Connect to Temporal server (default: localhost:7233)
    client = await Client.connect("localhost:7233")
    
    print("🚀 Starting Temporal Worker...")
    print("📋 Task Queue: loan-application-queue")
    print("⏳ Waiting for workflow executions...\n")
    
    # Create worker that listens to the task queue
    worker = Worker(
        client,
        task_queue="loan-application-queue",
        workflows=[LoanApplicationWorkflow],
        activities=[
            collect_docs,
            credit_check,
            property_valuation,
            underwriter_review,
            sign_agreement
        ],
    )
    
    # Run the worker
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

