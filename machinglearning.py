import librosa
import soundfile
import os, glob, pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

#DataFlair - Extract features (mfcc, chroma, mel) from a sound file     01
def extract_feature(file_name, mfcc, chroma, mel):
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate=sound_file.samplerate
        if chroma:
            stft=np.abs(librosa.stft(X))
        result=np.array([])
        if mfcc:
            mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result=np.hstack((result, mfccs))
        if chroma:
            chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result=np.hstack((result, chroma))
        if mel:
            mel=np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
            result=np.hstack((result, mel))
    return result

#DataFlair - Emociones en el conjunto de datos de RAVDESS                        02
emotions={
  '01':'neutral',
  '02':'calm',
  '03':'happy',
  '04':'sad',
  '05':'angry',
  '06':'fearful',
  '07':'disgust',
  '08':'surprised'
}

#DataFlair - Emotions to observe                                    03
observed_emotions=['calm', 'happy', 'fearful', 'disgust']

#DataFlair - Cargue los datos y extraiga funciones para cada archivo de sonido 04
def load_data(test_size = 0.2):                                     #definimos entradas y salidas
    x, y = [], []
    for file in glob.glob("E:\\Emotions\\Actor_*\\*.wav"):
        file_name=os.path.basename(file)
        emotion=emotions[file_name.split("-")[2]]
        if emotion not in observed_emotions:
            continue
        feature=extract_feature(file, mfcc=True, chroma=True, mel=True)
        x.append(feature)
        y.append(emotion)
    return train_test_split(np.array(x), y, test_size=test_size, random_state=9)

#DataFlair - Dividir el conjunto de datos                                     05
x_train,x_test,y_train,y_test=load_data(test_size=0.25)                 # tasa de aprendizaje

#DataFlair - Obtenga la forma de los conjuntos de datos de entrenamiento y prueba     06
print((x_train.shape[0], x_test.shape[0]))

#DataFlair - Obtenga la cantidad de funciones extraídas                   07
print(f'Features extracted: {x_train.shape[1]}')

#DataFlair -Inicializar el clasificador de perceptrón multicapa       08
model=MLPClassifier(alpha=0.01, batch_size=256, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=500)

#DataFlair - Entrena el modelo                                        09
model.fit(x_train, y_train)

#DataFlair - Predecir para el conjunto de prueba                               10
y_pred=model.predict(x_test)
print(type(y_pred))

#DataFlair - Calcule la precisión de nuestro modelo                   11
accuracy=accuracy_score(y_true=y_test, y_pred=y_pred)

#DataFlair - imprime la precision
print("Accuracy: {:.2f}%".format(accuracy*100))