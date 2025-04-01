import time
import os
import vertexai
from vertexai.tuning import sft

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/gen-lang-client-0788085518-6a37c52bd548.json"

# TODO(developer): Update and un-comment below line
vertexai.init(project="681792955708", location="us-central1")

sft_tuning_job = sft.train(
    source_model="gemini-1.5-pro-002",
    train_dataset="gs://traffic_recognition/train_data_300-800.jsonl",
)

# Polling for job completion
while not sft_tuning_job.has_ended:
    time.sleep(60)
    sft_tuning_job.refresh()

print(sft_tuning_job.tuned_model_name)
print(sft_tuning_job.tuned_model_endpoint_name)
print(sft_tuning_job.experiment)