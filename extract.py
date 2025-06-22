
import csv
import random
import io
from faker import Faker
from google.cloud import storage

# Initialize Faker
fake = Faker()

# Number of employee records to generate
NUM_RECORDS = 100

# Configuration
BUCKET_NAME = "employee_bkt1234"   # replace with your bucket name
DESTINATION_BLOB_NAME = "employee_data.csv"

# Define the PII fields and other employee attributes
FIELDS = [
    "employee_id",
    "first_name",
    "last_name",
    "date_of_birth",
    "ssn",                   # Full Social Security Number (PII)
    "email",
    "phone_number",
    "address",
    "hire_date",
    "job_title",
    "department",
    "salary",
    "bank_account_number"    # Full Bank Account Number (PII)
]

def generate_employee(emp_id):
    dob = fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%Y-%m-%d")
    hire_date = fake.date_between(start_date="-10y", end_date="today").strftime("%Y-%m-%d")
    salary = round(random.uniform(30000, 120000), 2)

    return {
        "employee_id": emp_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "date_of_birth": dob,
        "ssn": fake.ssn(),
        "email": fake.company_email(),
        "phone_number": fake.phone_number(),
        "address": fake.address().replace("\n", ", "),
        "hire_date": hire_date,
        "job_title": fake.job(),
        "department": fake.random_element([
            "Engineering", "Sales", "Marketing", "HR", "Finance", "IT", "Support"
        ]),
        "salary": salary,
        "bank_account_number": fake.bban()
    }

# Create an in-memory text buffer
csv_buffer = io.StringIO()
writer = csv.DictWriter(csv_buffer, fieldnames=FIELDS)
writer.writeheader()

for i in range(1, NUM_RECORDS + 1):
    writer.writerow(generate_employee(i))

# Get the CSV content as a string
csv_content = csv_buffer.getvalue()

# Upload directly to GCS
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob(DESTINATION_BLOB_NAME)

# Upload the buffer contents (as text)
blob.upload_from_string(csv_content, content_type='text/csv')

print(f"Generated and uploaded {NUM_RECORDS} employee records to gs://{BUCKET_NAME}/{DESTINATION_BLOB_NAME}")
