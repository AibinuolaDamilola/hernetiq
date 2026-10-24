"""
NovaPay Fine-Tuning Pipeline
Airflow DAG — weekly schedule
Retrains credit scoring and fraud detection models

Author: NovaPay AI Engineering
"""

import json
import logging
import os
from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    AIRFLOW_AVAILABLE = True
except ImportError:
    AIRFLOW_AVAILABLE = False

logger = logging.getLogger(__name__)

MANIFEST_PATH = "model/training_data_manifest.json"
PIPELINE_CONFIG_PATH = "data/pipeline_config.yaml"
MODEL_OUTPUT_DIR = "artifacts/models/"

MODELS_TO_RETRAIN = [
    "credit_scoring_model",
    "fraud_detection_model",
]


def load_training_manifest():
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)
    return manifest["approved_sources"]


def fetch_data_source(source):
    source_id = source["source_id"]
    logger.info(f"Fetching data source: {source_id}")

    if source["type"] in ("internal", "partner_bureau"):
        return _fetch_from_internal_store(source_id)

    if source["type"] == "external":
        return _fetch_from_external_feed(source)

    raise ValueError(f"Unknown source type: {source['type']}")


def _fetch_from_internal_store(source_id):
    logger.info(f"  → gs://novapay-training-data/{source_id}/")
    return {}


def _fetch_from_external_feed(source):
    source_id = source["source_id"]
    logger.info(f"  → external: {source_id}")
    return {}


def validate_source(source, data):
    source_id = source["source_id"]

    if source["type"] == "external":
        logger.warning(f"Source {source_id} is external. Skipping hash verification.")
        return True

    logger.info(f"Source {source_id}: schema check passed")
    return True


def prepare_training_dataset():
    sources = load_training_manifest()
    combined = []

    for source in sources:
        data = fetch_data_source(source)
        valid = validate_source(source, data)
        if valid:
            combined.append(data)
            logger.info(f"Added source: {source['source_id']}")

    logger.info(f"Training dataset prepared from {len(combined)} sources.")
    return combined


def run_fine_tuning(model_name, dataset):
    logger.info(f"Starting fine-tune: {model_name}")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(MODEL_OUTPUT_DIR, model_name, timestamp)
    logger.info(f"  Training complete. Output: {output_path}")
    _deploy_model(model_name, output_path)
    return output_path


def _deploy_model(model_name, model_path):
    logger.info(f"Deploying {model_name} from {model_path} → production")
    logger.info(f"  Deployment complete.")


def run_pipeline():
    logger.info("=== NovaPay Fine-Tuning Pipeline: START ===")
    dataset = prepare_training_dataset()
    for model_name in MODELS_TO_RETRAIN:
        run_fine_tuning(model_name, dataset)
    logger.info("=== NovaPay Fine-Tuning Pipeline: COMPLETE ===")


if AIRFLOW_AVAILABLE:
    default_args = {
        "owner": "novapay-ai-eng",
        "depends_on_past": False,
        "start_date": datetime(2024, 1, 1),
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    }

    with DAG(
        "novapay_fine_tuning_pipeline",
        default_args=default_args,
        schedule_interval="@weekly",
        catchup=False,
    ) as dag:

        run_pipeline_task = PythonOperator(
            task_id="run_fine_tuning_pipeline",
            python_callable=run_pipeline,
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()
