# Sample Streamlit app + BigQuery ML
This repository contains a sample application showcasing streamlit integrated with BigQueryML.

## Use case
Starting with a table with customer features, the application segments the customer base using a KNN algorithm.
Then each of the individual clusters can be easily exported to other tanle for any downstream task.

![Sample app](assets/01.gif)

## Running the code

1. Select or create a Google Cloud project, and enable the required APIs.

2. Create a service account with enough permissions to interact with the different services (BigQuery, Cloud Run ..).

3. Open `Cloud shell` and clone this repository

4. Edit the `dashboard.py` file and specify:

```python
PROJECT_ID='TO_DO_DEVELOPER'
DATASET_ID='TO_DO_DEVELOPER'
TABLE_ID='TO_DO_DEVELOPER'
NUM_CLUSTERS_MAX=10
```

5. Edit the `build_cloud_run.sh` file and specify:
```bash
SERVICE_NAME='TO_DO_DEVELOPER'
REGION='TO_DO_DEVELOPER'
PROJECT_ID='TO_DO_DEVELOPER'
```

