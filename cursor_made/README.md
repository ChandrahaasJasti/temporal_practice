# Loan Application Workflow with Temporal

A complete MVP implementation of a loan application processing system using Temporal workflow orchestration.

## Workflow States

The loan application goes through five sequential states:

1. **collect_docs** - Collects required documents from the applicant
2. **credit_check** - Performs credit check and validates credit score
3. **property_valuation** - Conducts property appraisal
4. **underwriter_review** - Reviews application and makes lending decision
5. **sign_agreement** - Finalizes and signs the loan agreement

## Project Structure

```
temporal_practice/
├── activities.py       # Activity definitions for each workflow state
├── workflow.py         # Main workflow orchestration logic
├── worker.py          # Temporal worker to execute workflows
├── run_workflow.py    # Client to start workflow executions
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Prerequisites

1. **Temporal Server**: You need a running Temporal server

### Option 1: Using Temporal CLI (Recommended)
```bash
# Install Temporal CLI
brew install temporal  # macOS
# or download from https://docs.temporal.io/cli

# Start local Temporal server
temporal server start-dev
```

### Option 2: Using Docker
```bash
git clone https://github.com/temporalio/docker-compose.git
cd docker-compose
docker-compose up
```

2. **Python Dependencies**
```bash
pip install -r requirements.txt
```

## Running the Application

### Step 1: Start the Temporal Server
```bash
# In terminal 1
temporal server start-dev
```

The Temporal Web UI will be available at http://localhost:8233

### Step 2: Start the Worker
```bash
# In terminal 2
python worker.py
```

You should see:
```
🚀 Starting Temporal Worker...
📋 Task Queue: loan-application-queue
⏳ Waiting for workflow executions...
```

### Step 3: Run the Workflow
```bash
# In terminal 3
python run_workflow.py
```

## Expected Output

When you run the workflow, you'll see output like:

```
======================================================================
🏦 LOAN APPLICATION WORKFLOW
======================================================================
Applicant: John Doe
Property: 123 Main Street, San Francisco, CA 94102
Requested Amount: $350,000.00
======================================================================

🚀 Starting workflow execution...

======================================================================
📊 WORKFLOW RESULTS
======================================================================
✅ Status: APPROVED
📝 Agreement ID: LOAN-20251017123456
💰 Approved Amount: $350,000.00
📊 Interest Rate: 3.5%
🏠 Property Value: $450,000.00
📈 Credit Score: 750
⚖️  Underwriter Decision: APPROVED

📄 Documents Collected:
   - Identity Proof
   - Income Statement
   - Tax Returns
   - Property Documents
   - Bank Statements

✨ Loan of $350,000.00 approved and agreement signed
======================================================================
```

## Monitoring

Visit the Temporal Web UI at http://localhost:8233 to:
- View workflow execution history
- See activity execution details
- Monitor workflow status in real-time
- Debug failures and retries

## Customization

### Modify Applicant Details

Edit `run_workflow.py` to change:
```python
applicant_name = "Your Name"
property_address = "Your Property Address"
requested_loan_amount = 500000.00
```

### Adjust Activity Logic

Each activity in `activities.py` can be customized:
- Add real API integrations (credit bureaus, property valuation services)
- Implement actual business logic
- Add error handling and retry policies

### Workflow Configuration

Modify `workflow.py` to:
- Change timeout values
- Add conditional logic
- Implement parallel activities
- Add human-in-the-loop approvals using Signals

## Key Features

✅ **Durable Execution** - Workflows survive process crashes and restarts  
✅ **Automatic Retries** - Failed activities are automatically retried  
✅ **Full History** - Complete audit trail of every execution  
✅ **Timeout Handling** - Configurable timeouts for each activity  
✅ **State Management** - Workflow state is automatically persisted  

## Next Steps

1. **Add Human Approvals** - Use Temporal Signals for manual review steps
2. **Error Handling** - Implement retry policies and compensation logic
3. **Parallel Processing** - Run credit check and property valuation simultaneously
4. **Real Integrations** - Connect to actual credit bureaus and valuation APIs
5. **Testing** - Add unit and integration tests for workflows and activities

## Learn More

- [Temporal Documentation](https://docs.temporal.io/)
- [Python SDK Guide](https://docs.temporal.io/dev-guide/python)
- [Temporal Samples](https://github.com/temporalio/samples-python)

