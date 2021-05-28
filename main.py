import argparse
import os
import pandas as pd


import constants
from datasets.StartingDataset import StartingDataset
from networks.StartingNetwork import StartingNetwork
from train_functions.starting_train_updated import EvaluationDataset, starting_train


SUMMARIES_PATH = "training_summaries"


def main():
    # Get command line arguments
    args = parse_arguments()
    hyperparameters = {"epochs": args.epochs, "batch_size": args.batch_size, "margin": constants.MARGIN}

    # Create path for training summaries
    summary_path = None
    if args.logdir is not None:
        summary_path = f"{SUMMARIES_PATH}/{args.logdir}"
        os.makedirs(summary_path, exist_ok=True)

    # TODO: Add GPU support. This line of code might be helpful.
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print("Summary path:", summary_path)
    print("Epochs:", args.epochs)
    print("Batch size:", args.batch_size)

    # Initalize dataset and model. Then train the model!
    dataset = StartingDataset(constants.CSV_PATH, constants.IMAGE_DIR, constants.IMAGE_SIZE, constants.PERCENT_TRAIN)
    train_dataset = dataset.train_set
    val_dataset = dataset.val_set

    test_dataset = EvaluationDataset(data=constants.CSV_PATH , crop_info_path=constants.BBOX_PATH, image_folder="./datasets/train")

    model = StartingNetwork()
    starting_train(
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        test_dataset=test_dataset,
        model=model,
        hyperparameters=hyperparameters,
        n_eval=args.n_eval,
        summary_path=summary_path,
        bbox_path=constants.BBOX_PATH,
        train_path=constants.CSV_PATH
    )

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=constants.EPOCHS)
    parser.add_argument("--batch_size", type=int, default=constants.BATCH_SIZE)
    parser.add_argument("--n_eval", type=int, default=constants.N_EVAL)
    parser.add_argument("--logdir", type=str, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    main()
