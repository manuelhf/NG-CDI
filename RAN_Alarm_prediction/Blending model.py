#!/usr/bin/env python
# coding: utf-8

# In[43]:


####### 2.3 Sentence Transfomer
from sentence_transformers import SentenceTransformer
from transformers import AutoModel, AutoTokenizer
import pandas as pd
import numpy as np
import tensorflow_hub as hub
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from keras.models import Sequential, Model
from keras.layers import Dense, Input, Concatenate, Lambda
from keras.utils import to_categorical
from sklearn.linear_model import LogisticRegression


class Alarmlog:
    def __init__(self, model_name='sentence-transformers/paraphrase-MiniLM-L6-v2'):
        # Load the pre-trained Sentence Transformers model
        self.model = SentenceTransformer(model_name)
        # Initialize the Logistic Regression classifier for multi-class classification
        self.classifier = LogisticRegression(max_iter=1000)

    def train(self, X_train, y_train):
        # Encode the training sentences
        X_train_embeddings = self.model.encode(X_train)
        # Fit the Logistic Regression classifier on the training data
        self.classifier.fit(X_train_embeddings, y_train)

    def predict(self, X_test):
        # Encode the test sentences
        X_test_embeddings = self.model.encode(X_test)
        # Predict the labels using the trained classifier
        y_pred = self.classifier.predict(X_test_embeddings)
        return y_pred

    def evaluate(self, X_test, y_test):
        # Encode the test sentences
        X_test_embeddings = self.model.encode(X_test)
        # Evaluate the classifier on the test data
        accuracy = self.classifier.score(X_test_embeddings, y_test)
        return accuracy


# In[44]:


####### 2.2 Alarm partten
import pandas as pd
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense, Lambda
import keras.backend as K
import numpy as np
from sklearn.preprocessing import LabelEncoder
from datetime import datetime, timedelta
import warnings
from keras.layers import Input, LSTM
from keras.layers import Flatten

######## sliding window
def sliding_window(input_data):
    output_data=pd.DataFrame(columns=['x', 'y'])
    
    data_dict = {}
    target_length = 20
    for i in range(len(input_data)):
        sequential_data = []
        name = input_data.iloc[i]['Name_encoder']
        time_stamp = input_data.iloc[i]['Occurred On (NT)']
        time_stamp = datetime.strptime(time_stamp, "%Y/%m/%d %H:%M")
        data_dict[name] = time_stamp
        
        cutoff_time = time_stamp - timedelta(minutes=7200)
        data_dict = {key: value for key, value in data_dict.items() if (time_stamp - value).total_seconds() / 60 <= 7200}
     
        if len(data_dict) >= 1:
            sequential_data.extend(data_dict.keys())
    
        padded_data = sequential_data[:target_length] + [0] * max(0, target_length - len(sequential_data))
        sequential_data = padded_data[:target_length]
        output_data = output_data.append({'x': sequential_data, 'y': input_data.iloc[i]['Next Alarm_encoder']}, ignore_index=True)
    
    return output_data


class AlarmPattern:
    def __init__(self, num_classes):
        self.model = Sequential()

        def mask_zeros(x):
            mask = K.not_equal(x, 0)
            x = x * K.cast(mask, K.floatx())
            return x
        
        self.model.add(Lambda(mask_zeros, input_shape=(1, 20)))
        self.model.add(LSTM(units=510, return_sequences=True))
        self.model.add(LSTM(units=510, return_sequences=True))
        self.model.add(Flatten())
        self.model.add(Dense(num_classes, activation='softmax'))  # Use softmax activation for multi-class classification
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def fit(self, X, y, epochs=10, batch_size=64):
        return self.model.fit(X, y, epochs=epochs, batch_size=batch_size)

    def evaluate(self, X, y):
        return self.model.evaluate(X, y)

    def predict(self, X):
        predictions = self.model.predict(X)
        predicted_classes = np.argmax(predictions, axis=1)  # Get the class with the highest probability
        return predicted_classes


# In[45]:


####### 2.1 Base station perference 
from tensorflow.keras.layers import Input, LSTM, Dense
from tensorflow.keras.models import Model

class BaseStation:
    def __init__(self, num_classes):
        input_rnn1 = Input(shape=(1, 5))
        rnn1 = LSTM(510)(input_rnn1)  # Removing unit_forget_bias
        output_rnn1 = Dense(num_classes, activation='softmax')(rnn1)  # Use softmax activation for multi-class classification
        self.model_rnn1 = Model(inputs=input_rnn1, outputs=output_rnn1)

        # Compile the model with categorical cross-entropy loss
        self.model_rnn1.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def train(self, X, y, epochs=10, batch_size=64):
        return self.model_rnn1.fit(X, y, epochs=epochs, batch_size=batch_size)

    def evaluate(self, X, y):
        return self.model_rnn1.evaluate(X, y)

    def predict(self, X):
        predictions = self.model_rnn1.predict(X)
        predicted_classes = np.argmax(predictions, axis=1)  # Get the class with the highest probability
        return predicted_classes


# In[71]:


from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

class BlendingModel:

    def __init__(self, base_station, alarm_pattern, alarm_log):
        self.base_station = base_station
        self.alarm_pattern = alarm_pattern
        self.alarm_log = alarm_log
        self.gbdt = GradientBoostingClassifier(n_estimators=100, random_state=42)
        
    def stack_outputs(self, X1, X2, X3):
        base_station_output = self.base_station.predict(X1)
        alarm_pattern_output = self.alarm_pattern.predict(X2)
        alarm_log_output = self.alarm_log.predict(X3)
        print("Base Station Output Shape:", base_station_output.shape)
        print("Alarm Pattern Output Shape:", alarm_pattern_output.shape)
        print("Alarm Log Output Shape:", alarm_log_output.shape)
        return np.hstack((base_station_output, alarm_pattern_output, alarm_log_output))

    def train(self, X1, X2, X3, y):
        combined_output = self.stack_outputs(X1, X2, X3)
        combined_output = combined_output.reshape(-1, 3)
        self.gbdt.fit(combined_output, y)

    def predict(self, X1, X2, X3):
        combined_output = self.stack_outputs(X1, X2, X3)
        combined_output = combined_output.reshape(-1, 3)
        return self.gbdt.predict(combined_output)


# In[47]:


##### Data process
df = pd.read_csv('data_file.csv')
# df=df.head(10000)
df['Combined'] = df['Name'] + ',' + df['Location Information']+','+df['NE Type']

encoder = LabelEncoder()
df['AlarmSource_encoder'] = encoder.fit_transform(df['Alarm Source'])
df['Name_encoder'] = encoder.fit_transform(df['Name'])
df['Severity_encoder'] = encoder.fit_transform(df['Severity'])
df['Location_encoder'] = encoder.fit_transform(df['Location Information'])
df['NEType_encoder'] = encoder.fit_transform(df['NE Type'])
df['Next Alarm_encoder']= encoder.fit_transform(df['Next_Alarm'])

output_data= sliding_window(df)
df['sequential_data'] = output_data['x']


# In[48]:


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

X1=df[['Name_encoder','NEType_encoder', 'Hours_since_prior', 'Alarm_dow', 'Alarm_hour']].values
X2=df['sequential_data'].values
X3=df['Combined'].values
y= df['Next Alarm_encoder'].values 
y_categorical = to_categorical(y)


X1_train, X1_test, X2_train, X2_test, X3_train, X3_test, y_train, y_test = train_test_split(
    X1, X2, X3, y_categorical, test_size=0.27, random_state=42)
X1_train = np.reshape(X1_train, (X1_train.shape[0], 1, X1_train.shape[1]))
X1_test = np.reshape(X1_test, (X1_test.shape[0], 1, X1_test.shape[1]))
X2_train = np.array(X2_train.tolist())
X2_test = np.array(X2_test.tolist())
X2_train = X2_train.reshape(X2_train.shape[0], 1, X2_train.shape[1])
X2_test = X2_test.reshape(X2_test.shape[0], 1, X2_test.shape[1])


# In[50]:


base_station = BaseStation(num_classes=87)
base_station.train(X1_train, y_train, epochs=10, batch_size=64)
base_station.model_rnn1.save("base_station_model.h5")


# In[51]:


alarm_pattern = AlarmPattern(num_classes=87)
alarm_pattern.fit(X2_train, y_train, epochs=10, batch_size=64)
alarm_pattern.model.save("alarmpattern_model.h5")


# In[53]:


import joblib

alarm_log = Alarmlog()
y1_train = np.argmax(y_train, axis=1)
alarm_log.train(X3_train, y1_train)
joblib.dump(alarm_log.classifier, "alarmlog_model.pkl")


# In[75]:


blending_model = BlendingModel(base_station, alarm_pattern, alarm_log)
blending_model.train(X1_train, X2_train, X3_train, y1_train)

y1_test = np.argmax(y_test, axis=1)
y_pred = blending_model.predict(X1_test, X2_test, X3_test)

accuracy = accuracy_score(y1_test, y_pred)
precision = precision_score(y1_test, y_pred, average='micro')
recall = recall_score(y1_test, y_pred, average='micro')
f1 = f1_score(y1_test, y_pred, average='micro')

print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1 Score: {f1}')


# In[ ]:




