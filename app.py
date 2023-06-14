from src.pipeline.training_pipeline import TrainPipeline
from src.logger import logging
try:
    obj = TrainPipeline()
    obj.run_pipeline()
except Exception as e:
    logging.exception(e)