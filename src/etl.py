# Abres un cliente de S3
import boto3
import awswrangler as wr
session = boto3.Session(profile_name='itam_datascientist')
s3 = session.client('s3')


glue = boto3.client('glue')

response = glue.create_database(
    DatabaseInput={
        'Name': 'prediction_prod',
        'Description': 'Prod predictions in database.',
    }
)
response


def saving_athena():
    query = '''
        CREATE EXTERNAL TABLE IF NOT EXISTS `predictions`.`predictions_prod_processed` (
        `elevation` float ,
        `aspect` float,
        `slope` float,
        `horizontal_distance_to_hydrology` float,
        `vertical_distance_to_hydrology` float,
        `horizontal_distance_to_roadways` float,
        `hillshade_9am` float,
        `hillshade_noon` float,
        `hillshade_3pm` float,
        `horizontal_distance_to_fire_points` float,
        `wilderness_area1` string,
        `wilderness_area2` string,
        `wilderness_area3` string,
        `wilderness_area4` string,
        `soil_type_1` string,
        `soil_type_2` string,
        `soil_type_3` string,
        `soil_type_4` string,
        `soil_type_5` string,
        `soil_type_6` string,
        `soil_type_7` string,
        `soil_type_8` string,
        `soil_type_9` string,
        `soil_type_10` string,
        `soil_type_11` string,
        `soil_type_12` string,
        `soil_type_13` string,
        `soil_type_14` string,
        `soil_type_15` string,
        `soil_type_16` string,
        `soil_type_17` string,
        `soil_type_18` string,
        `soil_type_19` string,
        `soil_type_20` string,
        `soil_type_21` string,
        `soil_type_22` string,
        `soil_type_23` string,
        `soil_type_24` string,
        `soil_type_25` string,
        `soil_type_26` string,
        `soil_type_27` string,
        `soil_type_28` string,
        `soil_type_29` string,
        `soil_type_30` string,
        `soil_type_31` string,
        `soil_type_32` string,
        `soil_type_33` string,
        `soil_type_34` string,
        `soil_type_35` string,
        `soil_type_36` string,
        `soil_type_37` string,
        `soil_type_38` string,
        `soil_type_39` string,
        `soil_type_40` string,
        `predictions` string,
        `real_label` string,
        `cover_type_name` string
        ) COMMENT "Batch of predictions from linear estimator model."
        ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
        WITH SERDEPROPERTIES ('field.delim' = ',')
        STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
        LOCATION 's3://itam-analytics-proyectofinal-zaret-daan/predictions_prod_processed/'
        TBLPROPERTIES ('classification' = 'csv', "skip.header.line.count"="1");
    '''

    wr.athena.read_sql_query(query, database="predictions", ctas_approach=False)