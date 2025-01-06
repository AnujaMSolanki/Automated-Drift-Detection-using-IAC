import boto3
import json
import time
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Initialize the CloudFormation and SNS clients
    cf_client = boto3.client('cloudformation')  # Initialize CloudFormation client
    sns_client = boto3.client('sns')  # Initialize SNS client
    
    # Specify your stack names and SNS topic ARN
    stack_names = ['arn:aws:cloudformation:ap-south-1:471112828084:stack/DynamoDB/eac28c70-f209-11ee-8b09-0a02e01a9aa3', 'arn:aws:cloudformation:ap-south-1:471112828084:stack/EC2instance/74c0e490-f209-11ee-a0af-0aac48631e59', 'arn:aws:cloudformation:ap-south-1:471112828084:stack/S3Bucket/edefa5f0-f208-11ee-bd3f-06859283fa06']
    #stack_names = ['arn:aws:cloudformation:ap-south-1:471112828084:stack/EC2instance/74c0e490-f209-11ee-a0af-0aac48631e59']
    # Add your stack names here
    sns_topic_arn = 'arn:aws:sns:ap-south-1:471112828084:Detect_Drift'  # Change to your SNS topic ARN
    # response = cf_client.detect_stack_drift(StackName="arn:aws:cloudformation:ap-south-1:471112828084:stack/EC2instance/74c0e490-f209-11ee-a0af-0aac48631e59")
    # print(response)
    # drift_status_response = cf_client.describe_stack_drift_detection_status(StackDriftDetectionId=response['StackDriftDetectionId'])
    # print("printing error for response ",drift_status_response)
    for stack_name in stack_names:
        # Step 1: Trigger drift detection
        logger.info(f"Triggering drift detection for stack: {stack_name}")
        response = cf_client.detect_stack_drift(StackName=stack_name)  # Trigger drift detection for the stack
        drift_detection_id = response['StackDriftDetectionId']  # Get drift detection ID
        time.sleep(30) 
        # Step 2: Wait for drift detection to complete
        wait_interval = 5  # Initial wait interval
        max_wait_time = 300  # Maximum wait time (5 minutes)
        while True:
            # Describe stack drift detection status
            drift_status_response = cf_client.describe_stack_drift_detection_status(StackDriftDetectionId=drift_detection_id)
            print("printing error for response ",drift_status_response)
            drift_status = drift_status_response['DetectionStatus']
            print("printing drift status :",drift_status)
            #drift_status = drift_status_response['StackDriftStatus']
            if drift_status == 'DETECTION_COMPLETE':
                logger.info(f"Drift detection completed for stack: {stack_name}")
                break  # Exit loop if drift detection is complete
            elif drift_status == 'DETECTION_FAILED':
                logger.error(f"Drift detection failed for stack: {stack_name}")
                break  # Exit loop if drift detection failed
            elif wait_interval > max_wait_time:
                logger.warning(f"Timed out waiting for drift detection to complete for stack: {stack_name}")
                break  # Exit loop if maximum wait time exceeded
            else:
                logger.info(f"Waiting {wait_interval} seconds for drift detection to complete for stack: {stack_name}")
                time.sleep(wait_interval)
                wait_interval *= 2  # Exponential backoff for wait interval
        
        # Step 3: Describe stack resource drifts
        response_drifts = cf_client.describe_stack_resource_drifts(StackName=stack_name)  # Describe drifts
        
        # Step 4: Extract and format drift details
        drift_details = []  # Initialize list to store drift details
        for drift in response_drifts['StackResourceDrifts']:
            resource_id = drift['LogicalResourceId']  # Get logical resource ID
            resource_type = drift['ResourceType']  # Get resource type
            drift_status = drift['StackResourceDriftStatus']  # Get drift status
            expected_value = drift['ExpectedProperties']  # Get expected properties
            actual_value = drift['ActualProperties']  # Get actual properties
            
            # Add drift details to the list
            drift_details.append({
                'Resource': resource_id,
                'Type': resource_type,
                'Status': drift_status,
                'Expected Value': expected_value,
                'Actual Value': actual_value
            })
        
        # Step 5: Prepare and send the notification
        s = stack_name.split(':')[-1].split('/')
        stack_name = s[-2]
        message = f"Drift status for stack {stack_name} is {drift_status}. Details:\n{json.dumps(drift_details, indent=2)}"
        sns_response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject=f'CloudFormation Stack Drift Detected: {stack_name}'
        )
    
    # Step 6: Return response indicating successful completion
    return {
        'statusCode': 200,
        'body': json.dumps('Drift detection and notification sent for all stacks.')
    }
