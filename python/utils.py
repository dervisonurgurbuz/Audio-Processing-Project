import librosa
import numpy as np
import os
import torch
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore') # ignoring runtime warning if needed

class CustomDataset(Dataset):
    def __init__(self, data, labels):
        self.data = torch.tensor(data)  # Assuming 'data' is a NumPy array or a list
        self.labels = torch.tensor(labels)  # Assuming 'labels' is a NumPy array or a list

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index], self.labels[index]


def extract_features(file, model_type):
    y, sr = librosa.load(file)
    # ZCR
    result = np.array([])
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=y).T, axis=0)
    result=np.hstack((result, zcr)) # stacking horizontally
    # Chroma_stft
    stft = np.abs(librosa.stft(y=y))
    chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sr).T, axis=0)
    result = np.hstack((result, chroma_stft)) # stacking horizontally
    # MFCC
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr).T, axis=0)
    result = np.hstack((result, mfcc)) # stacking horizontally
    # Root Mean Square Value
    rms = np.mean(librosa.feature.rms(y=y).T, axis=0)
    result = np.hstack((result, rms)) # stacking horizontally
    # MelSpectogram
    mel = np.mean(librosa.feature.melspectrogram(y=y, sr=sr).T, axis=0)
    result = np.hstack((result, mel)) # stacking horizontally
    if model_type == 'CNN':
        return result.reshape(1, 9, 18) # Reshape as CNN input: 1 channel 9x18 matrix
    return result

def lodader(folder_path, labeldict, batch_size, model_type):
    Audio_folder = folder_path
    feature_tensors = []
    label_tensors = []
    emo_dict = labeldict

    for emotion_folder in os.listdir(Audio_folder):
        subfolder = os.path.join(Audio_folder, emotion_folder)
        if os.path.isdir(subfolder):  # Check if it's a directory
            print(f"Processing emotion: {emotion_folder}")
            # Loop through audio files within each emotion folder
            for audio_file in os.listdir(subfolder):
                if audio_file.endswith(".wav"):  # Ensure the file is a .wav file
                    file_path = os.path.join(subfolder, audio_file)
                    features = extract_features(file_path, model_type)
                    feature_tensors.append(features)
                    label_tensors.append(emo_dict[emotion_folder])
    
    dataset = CustomDataset(feature_tensors, label_tensors)
    train_size = int(0.8 * len(dataset))
    val_size = int(0.1 * len(dataset))
    test_size = len(dataset) - train_size - val_size
    train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, val_size, test_size])

    batch_size = batch_size
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader, test_loader

# AUC metric
def evaluate(mymodel, dataloader):
    mymodel.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for data in dataloader:
            inputs, labels = data
            inputs, labels = inputs.float(), labels.long()
            outputs = mymodel(inputs)
            _, predict = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predict == labels).sum().item()
    return correct / total

def save_model(model, path):
    savepath = path+'_model.pth'
    torch.save(model.state_dict(), savepath)
    print("model saved at: ", savepath)

def load_model(model, model_path):
    model.load_state_dict(torch.load(model_path))
    return model

def label_query(dict, value):
    key = [k for k, v in dict.items() if v == value]
    return key

def smoothing(data, window_size):
    avg = []
    count = 0
    for i, value in enumerate(data, 1):
        count += value
        if i >= window_size:
            avg.append(count / window_size)
            count -= data[i - window_size]
    return avg

def result_generation(history, smooth, model_type):    
    loss = smoothing(history['trainLoss'], smooth)
    trian_auc = smoothing(history['trainAUC'], smooth)
    val_auc = smoothing(history['valAUC'], smooth)
    epochs = range(1, len(loss) + 1)

    ax1 = plt.subplot()
    ax2 = ax1.twinx()
    ax1.set_ylabel('Loss', fontsize=15)
    ax2.set_ylabel('Accuracy', fontsize=15)
    ax1.set_xlabel('epochs', fontsize=15)
    L1, = ax2.plot(epochs, trian_auc, 'blue', label='Training Accuracy')
    L2, = ax1.plot(epochs, loss, 'red', label='Training Loss')
    L3, = ax2.plot(epochs, val_auc, 'green', label='Val Accuracy')
    plt.legend(handles = [L1, L2, L3], loc = 'upper left', fontsize=10)
    if model_type == 'CNN':
        plt.title(f'CNN Training process (smoothing {smooth})')
        plt.savefig('./results/CNN.png')
    else:
        plt.title(f'MLP Training process (smoothing {smooth})')
        plt.savefig('./results/MLP.png')