import tensorflow as tf
import numpy as np
import os
import workIds as wi
import prepWorks as pw

##Variables
#File location of the loaded text converted to absolute path
prepWork = os.path.abspath(pw.textOut)

#Train model stuff
training = False
numGenerate = 1000
epochs = 35
startString = 'The '

#Training constants
checkpointDir = './training_checkpoints'
seqLenth = 100
batchSize = 64
bufferSize = 10000
embeddingDim = 256
rnnUnits = 1024
temperature = 1.0

#Finished work name
reqFics = sum(1 for line in open(wi.csvName + '.csv')) // 2

##Functions
#Saves the generated text into a file
def genFile(text):
	workName = 'epochs{}_reqFics{}'.format(epochs,reqFics)

	txtOut = open(workName + '.txt', 'w')
	txtOut.write(text)
	txtOut.close()

#This is called to start the program
def main():
	#Encodes text file into utf-8
	text = open(prepWork, 'rb').read().decode(encoding='utf-8')

	#Gets list of known characters
	vocab = sorted(set(text))
	print('{} unique characters'.format(len(vocab)))

	#Converts readable text to machine text and vis versa
	char2idx = {unique:idx for idx, unique in enumerate(vocab)}
	idx2char = np.array(vocab)

	#Converts text to a number that represents it
	textAsInt = np.array([char2idx[char] for char in text])
	charDataset = tf.data.Dataset.from_tensor_slices(textAsInt)
	sequences = charDataset.batch(seqLenth+1, drop_remainder=True)

	def splitInputTarget(chunk):
		inputText = chunk[:-1]
		targetText = chunk[1:]
		return inputText, targetText

	dataset = sequences.map(splitInputTarget)
	dataset = dataset.shuffle(bufferSize).batch(batchSize, drop_remainder=True)

	vocabSize = len(vocab)

	#Prepares the training of a model. This can train a new model or load a previously trained one
	def buildModel(vocabSize, embeddingDim, rnnUnits, batchSize):
		model = tf.keras.Sequential([
			tf.keras.layers.Embedding(vocabSize, embeddingDim, batch_input_shape=[batchSize, None]),
			tf.keras.layers.GRU(rnnUnits, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
			tf.keras.layers.Dense(vocabSize)
		])
		return model

	#This will run when the program is creating a trained model
	if(training == True):
		model = buildModel(vocabSize=len(vocab), embeddingDim=embeddingDim, rnnUnits=rnnUnits, batchSize=batchSize)

		def loss(labels, logits):
			return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

		model.compile(optimizer='adam', loss=loss)

		checkpointPrefix = os.path.join(checkpointDir, 'chkpt_{epoch}')
		checkpointCallback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpointPrefix, save_weights_only=True)

		history = model.fit(dataset, epochs=epochs, callbacks=[checkpointCallback])

	#Collects information about the trained model and presents them
	model = buildModel(vocabSize, embeddingDim, rnnUnits, batchSize=1)
	model.load_weights(tf.train.latest_checkpoint(checkpointDir))
	model.build(tf.TensorShape([1, None]))
	model.summary()

	#Final code that generates the output work
	def generateText(model, startString):
		inputEval = [char2idx[s] for s in startString]
		inputEval = tf.expand_dims(inputEval, 0)

		textGenerated = []

		model.reset_states()
		for i in range(numGenerate):
			predictions = model(inputEval)
			predictions = tf.squeeze(predictions, 0)

			#Predictions get crazier as temperature goes up
			predictions = predictions / temperature
			predictedId = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

			inputEval = tf.expand_dims([predictedId], 0)
			textGenerated.append(idx2char[predictedId])

		return (startString + ''.join(textGenerated))

	#Gets generated text and runs the save function
	genText = generateText(model, startString=startString)
	genFile(genText)
	print('Finished generating work')
