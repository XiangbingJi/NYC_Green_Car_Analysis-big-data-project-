from numpy import array
from pyspark.mllib.clustering import GaussianMixture, GaussianMixtureModel
import csv
from pyspark.mllib.linalg import Vectors, DenseMatrix
from numpy.testing import assert_equal
from shutil import rmtree
import os, tempfile
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
import json
import createJSON
import sys

def build(k):
    os.environ["SPARK_HOME"] = "/usr/local/Cellar/spark-2.0.1-bin-hadoop2.7"
    conf = (SparkConf().setMaster('local').setAppName('a'))
    sc = SparkContext(conf = conf)
    rawData = []
    csv.register_dialect(
        'mydialect',
        delimiter = ',',
        quotechar = '"',
        doublequote = True,
        skipinitialspace = True,
        lineterminator = '\r\n',
        quoting = csv.QUOTE_MINIMAL)

    for i in range(24):
        inputPath = './project-data/Dataset/Data' + str(i) + '.csv'
        outputPath = './project-data/output/Output' + str(i) + '.json'
        isFirstRow = True
        rowCount = 0
        rawData = []
        with open(inputPath, 'rb') as mycsvfile:
            thedata = csv.reader(mycsvfile, dialect='mydialect')
            for row in thedata:
                if not isFirstRow and row[2] != '0.0' and row[3] != '0.0':
                    rawData.append(row[2])
                    rawData.append(row[3])
                    rowCount += 1
                else:
                    isFirstRow = False

        parsedData = array(rawData).reshape((rowCount, 2))

        rddData = sc.parallelize(parsedData)

        gmm = GaussianMixture.train(rddData, k)

        result = []
        for j in range(num):
            tmp = {}
            tmp['weight'] = gmm.weights[j]
            tmp['center'] = gmm.gaussians[j].mu.toArray().tolist()
            tmp['sigma'] = gmm.gaussians[j].sigma.toArray().tolist()
            result.append(tmp)

    # write into json

    data = createJSON.create(result)
    with open(outputPath, 'w') as outfile:
        json.dump(data, outfile, sort_keys = True, indent = 4, separators = (',', ':'))
        

if __name__ == '__main__':
    for k in range(3, 11):
        data = build(k)

    

