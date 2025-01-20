# ResearchProject
# Automated Drift Detection and Remediation in Infrastructure-as-Code (IaC)

## Project Overview
This project investigates infrastructure drift in cloud environments managed by Infrastructure-as-Code (IaC), with a focus on **AWS CloudFormation**. The aim is to detect and remediate drift using **AWS Lambda** and other services to ensure infrastructure consistency, security, and compliance.

### Key Objectives:
- Identify drift across multiple AWS CloudFormation stacks.
- Automate remediation using rollback and configuration synchronization strategies.
- Improve IaC practices for cloud resource management.

## Technologies Used
- **AWS CloudFormation**: Define and provision infrastructure using templates.
- **AWS Lambda**: Automate drift detection and remediation.
- **AWS SNS**: Send notifications when drift is detected.
- **AWS EventBridge**: Schedule Lambda functions for regular checks.
- **Python**: Custom scripts for drift detection and reporting.
- **Terraform**: Compare alternative IaC tools (highlighted in the report).
- **YAML**: Define IaC templates for infrastructure provisioning.

## Repository Structure
- **`yaml_files/`**: Contains CloudFormation and other YAML templates for IaC.
- **`docs/`**: Includes the research report, configuration manual, and presentation files.
- **`scripts/`**: Python scripts for AWS Lambda functions used in drift detection.
- **`outputs/`**: Example logs, notifications, and remediation results.

## Key Features
1. **Drift Detection**:
   - Regularly monitor infrastructure for deviations from the desired state.
   - Notify administrators about drift events via AWS SNS.

2. **Remediation**:
   - Automated rollback: Restore infrastructure to its original state.
   - Configuration synchronization: Align current configurations with desired states.

3. **Monitoring**:
   - Scheduled checks using AWS EventBridge.
   - Notifications and detailed reports for administrators.

## Experiments and Results
1. **Experiment 1: EC2 Drift Detection**:
   - Drift in EC2 instance types (e.g., `t2.micro` changed to `t2.small`) was detected within 5 minutes.
   - Results showed 100% accuracy in detection.

2. **Experiment 2: Remediation Strategies**:
   - **Rollback**: Quick remediation (2 minutes) but brief downtime.
   - **Synchronization**: Slower remediation (5 minutes) but no downtime.

3. **Experiment 3: S3 Bucket Rules**:
   - Unauthorized changes to S3 bucket configurations were detected and notified within 10 minutes.

## Future Work
- Implement machine learning to predict drift occurrences.
- Extend the system to support multi-cloud environments (e.g., Azure, Google Cloud).
- Develop advanced remediation strategies for complex drifts.

## References
- Detailed literature review and implementation steps can be found in the [Research Report](./docs/Research_Report.pdf).

