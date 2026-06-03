import argparse
import json
import logging
import time
import yaml
import numpy as np
import pandas as pd


def write_error(output_file, version, message):
    metrics = {
        "version": version,
        "status": "error",
        "error_message": message
    }

    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=4)

    return metrics


def load_config(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    required = ["seed", "window", "version"]

    for key in required:
        if key not in config:
            raise ValueError(f"Missing config field: {key}")

    return config


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    logging.basicConfig(
        filename=args.log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    start_time = time.time()

    try:
        logging.info("Job started")

        config = load_config(args.config)

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(
            f"Config loaded: seed={seed}, window={window}, version={version}"
        )

        df = pd.read_csv(args.input)

        if df.empty:
            raise ValueError("Input CSV is empty")

        if "close" not in df.columns:
            raise ValueError("Missing required column: close")

        logging.info(f"Rows loaded: {len(df)}")

        df["rolling_mean"] = (
            df["close"]
            .rolling(window=window)
            .mean()
        )

        logging.info("Rolling mean computed")

        df["signal"] = (
            df["close"] > df["rolling_mean"]
        ).astype(int)

        logging.info("Signals generated")

        rows_processed = len(df)

        signal_rate = float(df["signal"].mean())

        latency_ms = int(
            (time.time() - start_time) * 1000
        )

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=4)

        logging.info(f"Metrics: {metrics}")
        logging.info("Job completed successfully")

        print(json.dumps(metrics, indent=4))

    except Exception as e:

        logging.exception("Job failed")

        metrics = write_error(
            args.output,
            "v1",
            str(e)
        )

        print(json.dumps(metrics, indent=4))

        raise


if __name__ == "__main__":
    main()