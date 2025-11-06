import boto3
import pandas as pd
import logging
from src.logger import logging
from io import StringIO
from dotenv import load_dotenv
import os

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Access the values
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
#REGION = os.getenv("REGION", "us-east-1")  # default fallback

class s3_operations:
    def __init__(self):
        self.bucket_name = os.getenv("S3_BUCKET")
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
            region_name=os.getenv("REGION", "us-east-1")
        )
        logging.info(f"S3 connection initialized for bucket: {self.bucket_name}")

    def fetch_file_from_s3(self, file_key):
        """
        Fetches a CSV file from the S3 bucket and returns it as a Pandas DataFrame.
        """
        try:
            logging.info(f"Fetching file '{file_key}' from S3 bucket '{self.bucket_name}'...")
            obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
            raw_data = obj['Body'].read()

            # Try UTF-8 first; if it fails, fall back to Latin-1
            try:
                df = pd.read_csv(StringIO(raw_data.decode('utf-8')))
            except UnicodeDecodeError:
                logging.warning("UTF-8 decoding failed. Retrying with 'latin1' encoding...")
                df = pd.read_csv(StringIO(raw_data.decode('latin1')))

            logging.info(f"✅ Successfully fetched and loaded '{file_key}' from S3 ({len(df)} records).")
            return df

        except Exception as e:
            logging.exception(f"❌ Failed to fetch '{file_key}' from S3: {e}")
            return None


# Example usage
# if __name__ == "__main__":
#     # Replace these with your actual AWS credentials and S3 details
#     BUCKET_NAME = "bucket-name"
#     AWS_ACCESS_KEY = "AWS_ACCESS_KEY"
#     AWS_SECRET_KEY = "AWS_SECRET_KEY"
#     FILE_KEY = "data.csv"  # Path inside S3 bucket

#     data_ingestion = s3_operations(BUCKET_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY)
#     df = data_ingestion.fetch_file_from_s3(FILE_KEY)

#     if df is not None:
#         print(f"Data fetched with {len(df)} records..")  # Display first few rows of the fetched DataFrame