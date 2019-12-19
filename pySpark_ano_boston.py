import time
import numpy as np
import pandas as pd
# load the boston data set
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from scipy.stats.stats import pearsonr
from pyspark import SparkContext, SQLContext

# linear regresion with Spark
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
boston = load_boston()

# convert to a Pandas Data Frame
print("Started loading dataset at UTC: {}".format(time.time()))
boston_pd = pd.DataFrame(data=np.c_[boston['data'], boston['target']],
                         columns=np.append(boston['feature_names'], 'target')).sample(frac=1)
print("Finsihed loading dataset at UTC: {}".format(time.time()))
print("Loaded dataset with shape: {}".format(boston_pd.shape))


print("Started preprocessing dataset at UTC: {}".format(time.time()))
print("Splitting dataset")
# split into data and label arrays
y = boston_pd['target']
X = boston_pd.drop(['target'], axis=1)

# create training (~80%) and test data sets
X_train = X[:400]
X_test = X[400:]
y_train = y[:400]
y_test = y[400:]
print("Finished prerpocessing dataset at UTC: {}".format(time.time()))

print("Started training model at UTC: {}".format(time.time()))
# train a classifier
lr = LinearRegression()
model = lr.fit(X_train, y_train)
print("Finished training model at UTC: {}".format(time.time()))

print("Started prediction with model at UTC: {}".format(time.time()))
# make predictions
y_pred = model.predict(X_test)
print("Finished prediction with model at UTC: {}".format(time.time()))

print("Started Scoring with model at UTC: {}".format(time.time()))
# error metrics
r = pearsonr(y_pred, y_test)
mae = sum(abs(y_pred - y_test))/len(y_test)
print("R-sqaured: " + str(r[0]**2))
print("MAE: " + str(mae))
print("Finished Scoring with model at UTC: {}".format(time.time()))

# convert to a Spark data frame
print("Start conversion to Spark Dataframe at UTC: {}".format(time.time()))
sc = SparkContext(appName="Spark Toy App")
spark = SQLContext(sc)
boston_sp = spark.createDataFrame(boston_pd)
# display(boston_sp.take(5))
print("Finished conversion to Spark Dataframe at UTC: {}".format(time.time()))

print("Started pre-processing for data for spark execution at UTC: {}".format(time.time()))
# split into training and test spark data frames
boston_train = spark.createDataFrame(boston_pd[:400])
boston_test = spark.createDataFrame(boston_pd[400:])

# convert to vector representation for MLlib
assembler = VectorAssembler(inputCols=boston_train.schema.names[:(boston_pd.shape[1] - 1)], outputCol="features" )
boston_train = assembler.transform(boston_train).select('features', 'target')
boston_test = assembler.transform(boston_test).select('features', 'target')
print("Finished preprocessing for data for spark execution at UTC: {}".format(time.time()))
# display(boston_train.take(5))


print("Started Training Spark model at UTC: {}".format(time.time()))
# linear regression
lr = LinearRegression(maxIter=10, regParam=0.1,
                      elasticNetParam=0.5, labelCol="target")

# Fit the model
model = lr.fit(boston_train)
boston_pred = model.transform(boston_test)

# calculate results
r = boston_pred.stat.corr("prediction", "target")
print("R-sqaured: " + str(r**2))