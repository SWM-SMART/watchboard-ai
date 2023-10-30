from dotenv import load_dotenv
import os

load_dotenv()

HUGGING_FACE_ACCESS_TOKEN = os.getenv("HUGGING_FACE_ACCESS_TOKEN")
HUGGING_FACE_NAME = "minseok-oh"

SUMMARY_MODEL_PATH=os.environ['SUMMARIZATION_MODEL_PATH']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
OPENAI_API_KEY = os.environ['OPENAI_KEY']

S3_PREFIX=os.environ['S3_PREFIX']
S3_BUCKET_NAME=os.environ['S3_BUCKET_NAME']