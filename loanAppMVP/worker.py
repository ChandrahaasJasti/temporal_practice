from temporalio.client import Client
from temporalio.worker import Worker
import asyncio

from activities import collect_docs, credit_check, login_fee, finalizer
from workflow import LoanApplicationWorkflow

async def main():
    client = await Client.connect("localhost:7233", namespace="loan-application-namespace")

    worker = Worker(
        client,
        namespace="loan-application-namespace",
        task_queue="loan-application-queue",
        workflows=[LoanApplicationWorkflow],
        activities=[collect_docs, credit_check, login_fee, finalizer],
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())