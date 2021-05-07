import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.tensorboard
import numpy as np

def starting_train(
    train_dataset, val_dataset, model, hyperparameters, n_eval, summary_path
):
    """
    Trains and evaluates a model.

    Args:
        train_dataset:   PyTorch dataset containing training data.
        val_dataset:     PyTorch dataset containing validation data.
        model:           PyTorch model to be trained.
        hyperparameters: Dictionary containing hyperparameters.
        n_eval:          Interval at which we evaluate our model.
        summary_path:    Path where Tensorboard summaries are located.
    """

    # Get keyword arguments
    batch_size, epochs = hyperparameters["batch_size"], hyperparameters["epochs"]

    # Initialize dataloaders
    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True
    )
    val_loader = torch.utils.data.DataLoader(
        val_dataset, batch_size=batch_size, shuffle=True
    )

    # Initalize optimizer (for gradient descent) and loss function
    optimizer = optim.Adam(model.parameters())
    loss_fn = nn.CrossEntropyLoss()

    # Initialize summary writer (for logging)
    if summary_path is not None:
        writer = torch.utils.tensorboard.SummaryWriter(summary_path)

    step = 0
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1} of {epochs}")

        # Loop over each batch in the dataset
        for i, batch in enumerate(train_loader):
            print(f"\rIteration {i + 1} of {len(train_loader)} ...", end="")
            images, labels = batch

            labels = torch.tensor(labels)

            optimizer.zero_grad()
            predictions = model(images)
            loss = loss_fn(predictions, labels)
            loss.backward()
            optimizer.step()

            # Periodically evaluate our model + log to Tensorboard
            if step % n_eval == 0:
                #if(writer.init):
                   

                # TODO:
                # Compute training accuracy.
                # Log the results to Tensorboard.
                images, labels = batch

                outputs = model(images)
                loss = loss_fn(outputs, labels)
                predictions = torch.argmax(outputs, dim=1)
                
                correct += (labels == predictions).int().sum()
                total += len(predictions)

                train_accuracy = (correct / total)


                # TODO:
                # Log the results to Tensorboard.
                # Don't forget to turn off gradient calculations!
                val_loss, val_accuracy = evaluate(val_loader, model, loss_fn)
                if summary_path is not None:
                    writer.add_scalar('train_loss', loss, global_step=step)
                    writer.add_scalar('val_loss', val_loss, global_step=step)
                    writer.add_scalar('val_accuracy', val_accuracy, global_step=step)
                    writer.add_scalar('train_accuracy', train_accuracy, global_step=step)
                    

            step += 1

        print()


def compute_accuracy(outputs, labels):
    """
    Computes the accuracy of a model's predictions.

    Example input:
        outputs: [0.7, 0.9, 0.3, 0.2]
        labels:  [1, 1, 0, 1]

    Example output:
        0.75
    """

    n_correct = (torch.round(outputs) == labels).sum().item()
    n_total = len(outputs)
    return n_correct / n_total


def evaluate(val_loader, model, loss_fn):
    """
    Computes the loss and accuracy of a model on the validation dataset.
    """
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in val_loader:
            images, labels = batch
            #images = images.to(device)
            #labels = labels.to(device)

            outputs = model(images)
            loss = loss_fn(outputs, labels)
            predictions = torch.argmax(outputs, dim=1)
            
            correct += (labels == predictions).int().sum()
            total += len(predictions)

    accuracy = (correct / total).item()
    model.train()
    return loss, accuracy

