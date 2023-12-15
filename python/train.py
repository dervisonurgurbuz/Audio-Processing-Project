import numpy as np
import torch
import random
import CNNModel as CNN
import MLPModel as MLP
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
import utils
warnings.simplefilter('ignore') # ignoring runtime warning if needed


SEED = 42
batch_size = 32
epochs = 1000
learning_rate = 0.003
num_classes = 3

Labels = {'HAP': 0, 'NEU': 1, 'SAD': 2}
Datasets = './data/CremaV3/'
model_save_path_CNN = './CNN'
model_save_path_MLP = './MLP'

def training(model, train_loader, val_loader):
    random.seed(SEED)
    # history
    history = {'trainLoss' : [],
            'trainAUC' : [],
            'valAUC' : []}

    # Loss function and optimizer
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    iterations = tqdm(range(epochs))
    # Loop
    for epoch in iterations:
        losses = []
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.float(), batch_y.long()  
            optimizer.zero_grad()  
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            losses.append(loss.item())
            loss.backward()
            optimizer.step()
        
        history['trainLoss'].append(np.mean(losses))
        history['trainAUC'].append(utils.evaluate(model, train_loader))
        history['valAUC'].append(utils.evaluate(model, val_loader))
        
        iterations.set_postfix({"Loss": f"{history['trainLoss'][-1]:.4f}", "trainAUC": f"{history['trainAUC'][-1]:.4f}", "valAUC": f"{history['valAUC'][-1]:.4f}"}, refresh=True)

    return history



def main():
    # CNN training
    cnnModel = CNN.CNN()
    train, val, test = utils.lodader(Datasets, Labels, batch_size, 'CNN')
    cnn_history = training(cnnModel, train, val)
    utils.result_generation(cnn_history, 55, 'CNN')
    print('Test: ', utils.evaluate(cnnModel, test))
    utils.save_model(cnnModel, model_save_path_CNN)

    
    # MLP training
    mlpModel = MLP.MLP()      
    train, val, test = utils.lodader(Datasets, Labels, batch_size, 'MLP')
    mlp_history = training(mlpModel, train, val)
    utils.result_generation(mlp_history, 55, 'MLP')
    print('Test: ', utils.evaluate(mlpModel, test))
    utils.save_model(mlpModel, model_save_path_MLP)

if __name__== "__main__" :
    main()