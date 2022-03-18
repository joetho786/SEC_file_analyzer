import boto3
import pandas as pd
import sagemaker
pd.get_option("display.max_columns", None)

import smjsindustry
from smjsindustry.finance import utils
from smjsindustry import NLPScoreType, NLPSCORE_NO_WORD_LIST
from smjsindustry import NLPScorerConfig, JaccardSummarizerConfig, KMedoidsSummarizerConfig
from smjsindustry import Summarizer, NLPScorer
from smjsindustry.finance.processor import DataLoader, SECXMLFilingParser
from smjsindustry.finance.processor_config import EDGARDataSetConfig
from sagemaker import get_execution_role

role = get_execution_role()
print(role)
session = sagemaker.Session()
bucket = session.default_bucket()

secdashboard_processed_folder='sec_analyzer_ml'
S3_BUCKET_NAME = 'sagemaker-studio-chq5a4fyzh5'
S3_FOLDER_NAME ='sec_analyzer_ml'
dataset_config = EDGARDataSetConfig(
    tickers_or_ciks=['amzn', 'goog', '27904', 'fb', 'msft', 'uber', 'nflx'],  # list of stock tickers or CIKs
    form_types=['10-K', '10-Q', '8-K'],              # list of SEC form types
    filing_date_start='2010-01-01',                  # starting filing date
    filing_date_end='2020-12-31',                    # ending filing date
    email_as_user_agent='test-user@test.com')        # user agent email

data_loader = DataLoader(
    role=sagemaker.get_execution_role(),    # loading job execution role
    instance_count=1,                       # instances number, limit varies with instance type
    instance_type='ml.c5.2xlarge',          # instance type
    volume_size_in_gb=30,                   # size in GB of the EBS volume to use
    volume_kms_key=None,                    # KMS key for the processing volume
    output_kms_key=None,                    # KMS key ID for processing job outputs
    max_runtime_in_seconds=None,            # timeout in seconds. Default is 24 hours.
    sagemaker_session=sagemaker.Session(),  # session object
    tags=None)      

data_loader.load(
    dataset_config,
    's3://{}/{}'.format('sagemaker-studio-chq5a4fyzh5', 'sec_analyzer_ml'),     # output s3 prefix (both bucket and folder names are required)
    'dataset_10k_10q_8k_2010_2021.csv',                                              # output file name
    wait=True,
    logs=True)   
client = boto3.client('s3')
client.download_file(S3_BUCKET_NAME, '{}/{}'.format(S3_FOLDER_NAME, '10k_10q_8k_2019_2021.csv'), '10k_10q_8k_2019_2021.csv')
df_forms = pd.read_csv('10k_10q_8k_2019_2021.csv')
print(df_forms)
