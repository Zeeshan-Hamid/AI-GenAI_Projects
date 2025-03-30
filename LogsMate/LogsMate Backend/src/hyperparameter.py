import optuna
import logging
from src.log_processor import process_chunk

def objective(trial, log_chunks, reranker,
              BM25_WEIGHT=1.0, RERANKER_WEIGHT=1.0, VECTOR_WEIGHT=1.0):
    multiplier = trial.suggest_float("reranker_multiplier", 5.0, 15.0)
    total_anomalies = 0
    total_score = 0
    count = 0

    for key, chunk in log_chunks:
        result = process_chunk(key, chunk, reranker, RERANKER_MULTIPLIER=multiplier,
                                 BM25_WEIGHT=BM25_WEIGHT, RERANKER_WEIGHT=RERANKER_WEIGHT,
                                 VECTOR_MULTIPLIER=10.0, VECTOR_WEIGHT=VECTOR_WEIGHT)
        if result and result.get("matches"):
            matches = result["matches"]
            total_anomalies += len(matches)
            total_score += sum(match["combined_score"] for match in matches)
            count += 1
    if count > 0 and total_anomalies > 0:
        anomaly_count = total_anomalies / count
        score_avg = total_score / total_anomalies
    else:
        anomaly_count = 0
        score_avg = 0
    composite = 0.5 * anomaly_count + 0.5 * score_avg
    return composite

def run_optuna_study(log_chunks, reranker,
                     storage_name="sqlite:///optuna_study.db",
                     study_name="my_rag_hyperparams",
                     desired_trials=5):
    study = optuna.create_study(
        study_name=study_name,
        direction="maximize",
        storage=storage_name,
        load_if_exists=True
    )
    current_trials = len(study.trials)
    if current_trials < desired_trials:
        additional_trials = desired_trials - current_trials
        logging.info(f"Running {additional_trials} additional trials (current: {current_trials}).")
        study.optimize(lambda trial: objective(trial, log_chunks, reranker),
                       n_trials=additional_trials)
    else:
        logging.info(f"Study already has {current_trials} trials; skipping further optimization.")
    return study
