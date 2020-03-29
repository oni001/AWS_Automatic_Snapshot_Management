import boto3
import os

ec = boto3.client('ec2', 'us-east-2')
ec2 = boto3.resource('ec2', 'us-east-2')
amis = ec2.images.filter(Owners=["self"])
snapshots = ec.describe_snapshots(OwnerIds=['self'])['Snapshots']

num = int(os.environ["SNAPSHOT"])

def lambda_handler(event, context):
    dates = sorted([snapshot['StartTime'] for snapshot in snapshots])[-num:]
    for snapshot in snapshots:
        
        create_date = snapshot['StartTime']
        snapshot_id = snapshot['SnapshotId']
        if create_date not in dates:
            print(f'deleting {snapshot_id}')
            ec.delete_snapshot(SnapshotId=snapshot_id)           
