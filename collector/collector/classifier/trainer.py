import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.utils.np_utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Input, Embedding, Convolution1D, MaxPool1D, Flatten, Dropout, Dense
from keras.layers.merge import concatenate
from keras.models import Model
from sklearn.model_selection import train_test_split


# 读取数据
df = pd.read_csv('para_large.csv')
df.drop(['id'], axis=1, inplace=True)

Y = df.is_explanation.values
# [1 0 1 ... 1 1 1]
# to_categorical的作用是将样本的类别向量表示成one-hot编码的矩阵
Y = to_categorical(Y)
# [[0. 1.]
#  [1. 0.]
#  [0. 1.]
#  ...
#  [0. 1.]
#  [0. 1.]
#  [0. 1.]]

# 使用分词器，并过滤掉一些特殊符号
tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ')
# fit_on_texts会统计词频，word_index按照词频从高到低记录各个词的排名
tokenizer.fit_on_texts(df.text)
vocab = tokenizer.word_index

# 划分训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(df.text, Y, test_size=0.1, random_state=2020)
x_train_seqs = tokenizer.texts_to_sequences(x_train)
x_test_seqs = tokenizer.texts_to_sequences(x_test)
x_train_pad_seqs = pad_sequences(x_train_seqs, maxlen=64)
x_test_pad_seqs = pad_sequences(x_test_seqs, maxlen=64)


# 读取预训练的词向量
pre_train_vector = {}
with open('glove.6B.200d.txt', encoding='utf-8') as lines:
    for line in lines:
        values = line.split()
        word = values[0]
        pre_train_vector[word] = np.asarray(values[1:], dtype='float32')
# 训练集中的词如果在词库中没有出现，则用0向量表示
embedding_matrix = np.zeros((len(vocab)+1, 200))
for word, i in vocab.items():
    vector = pre_train_vector.get(word)
    if vector is not None:
        embedding_matrix[i] = vector

# 参照TextCNN构建二分类模型，使用三层卷积
main_input = Input(shape=(64,), dtype='float64')
embed = Embedding(len(vocab)+1, 200, input_length=64, weights=[embedding_matrix], trainable=False)(main_input)
cnn_1 = Convolution1D(256, 2, activation='relu')(embed)
cnn_1 = MaxPool1D(pool_size=4)(cnn_1)
cnn_2 = Convolution1D(256, 3, activation='relu')(embed)
cnn_2 = MaxPool1D(pool_size=4)(cnn_2)
cnn_3 = Convolution1D(256, 4, activation='relu')(embed)
cnn_3 = MaxPool1D(pool_size=4)(cnn_3)
cnn = concatenate([cnn_1, cnn_2, cnn_3])
flat = Flatten()(cnn)
drop = Dropout(0.2)(flat)
main_output = Dense(2, activation='sigmoid')(drop)
model = Model(inputs=main_input, outputs=main_output)
model.compile('adam', loss='binary_crossentropy', metrics=['accuracy'])

# 训练
history = model.fit(x_train_pad_seqs, y_train, batch_size=32, epochs=40, validation_data=(x_test_pad_seqs, y_test))


plt.subplot(211)
plt.title("Accuracy")
plt.plot(history.history["accuracy"], color="g", label="Train")
plt.plot(history.history["val_accuracy"], color="b", label="Test")
plt.legend(loc="best")

plt.subplot(212)
plt.title("Loss")
plt.plot(history.history["loss"], color="g", label="Train")
plt.plot(history.history["val_loss"], color="b", label="Test")
plt.legend(loc="best")
plt.tight_layout()
plt.show()

model.save('model.h5')
