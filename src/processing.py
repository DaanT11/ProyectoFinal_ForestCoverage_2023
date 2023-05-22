###preprocess

from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import seaborn as sns
import boto3
import sagemaker
import json
import joblib
from sagemaker.tuner import (
    IntegerParameter,
    ContinuousParameter,
    HyperparameterTuner
)
from sagemaker.inputs import TrainingInput
from sagemaker.image_uris import retrieve
from sagemaker.serializers import CSVSerializer
from sagemaker.deserializers import CSVDeserializer

from preprocess_output import binarias_labeling

# Setting SageMaker variables
sess = sagemaker.Session()
write_bucket='itam-analytics-proyectofinal-zaret-daan'
write_prefix = "forestcover/output"

region = sess.boto_region_name
s3_client = boto3.client("s3", region_name=region)

sagemaker_role = sagemaker.get_execution_role()
sagemaker_client = boto3.client("sagemaker")
read_bucket = "itam-analytics-proyectofinal-zaret-daan"
read_prefix = "forestcover"

import logging
logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

def loading_data():
    prod_data_key = f"{read_prefix}/prod_data.csv"
    if sys.version_info[0] < 3: 
        from StringIO import StringIO # Python 2.x
    else:
        from io import StringIO # Python 3.x



    csv_obj = s3_client.get_object(Bucket=read_bucket, Key=prod_data_key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')

    test_features = pd.read_csv(StringIO(csv_string))
    logger.info('Shape after loading data ={}'.format(test_features.shape[0]))
    return test_features 

# deploy a model hosting endpoint
def deploy_pred(test_features):
    logger.info('deploy a model')
    multiclass_predictor = multiclass_estimator.deploy( ##este es el tuner
        initial_instance_count=1, instance_type="ml.m4.xlarge"
    )

    logger.info('Calculating predicted')
    # split the test dataset into 100 batches and evaluate using prediction endpoint
    prediction_batches = [multiclass_predictor.predict(batch) for batch in np.array_split(test_features, 100)]

    # parse protobuf responses to extract predicted labels
    extract_label = lambda x: x.label["predicted_label"].float32_tensor.values
    test_preds = np.concatenate(
        [np.array([extract_label(x) for x in batch]) for batch in prediction_batches]
    )
    test_preds = test_preds.reshape((-1,))

    logger.info('Preprocesing output ')  
    for i in range(1,41):
        #print('soil_type_'+str(i))
        var = 'soil_type'+str(i)
        test_preds['soil_type_'+str(i)] = test_preds.apply(binarias_labeling, axis=1)
        test_preds.drop(var, axis=1, inplace=True)

    label_map = {
    '0.0': "Spruce/Fir",
    '1.0': "Lodgepole Pine",
    '2.0': "Ponderosa Pine",
    '3.0': "Cottonwood/Willow",
    '4.0': "Aspen",
    '5.0': "Douglas-fir",
    '6.0': "Krummholz",
    }

    test_preds['cover_type_name'] = test_preds['real_label'].map(label_map)





    prod_data_key = f"{write_prefix}/prod_data.csv"
    csv_pred = StringIO()
    test_preds.to_csv(csv_pred)
    s3_resource = boto3.resource('s3')
    logger.info('Saving predicted in s3') 
    s3_resource.Object(write_bucket, prod_data_key).put(Body=csv_pred.getvalue())

    