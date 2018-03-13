#!/usr/bin/env python
from pandas import read_html
import json
import boto3
import datetime
import pytz

def get_price(event, context):
    gathered_utc = datetime.datetime.now(pytz.UTC)
    gathered_utc_formated = gathered_utc.strftime('%Y-%m-%d_%Z_%H:%M:%S')

    # Creating connection to Bucket where data is stored
    s3 = boto3.resource('s3')
    # Creating object key
    object = s3.Object(
        'daily-oil-price',
        'prices_{}.json'.format(
            gathered_utc_formated
        )
    )

    # Reading data from source
    d = read_html('https://oilprice.com/')[0].dropna(axis=1, how='all')
    d.columns = ["stream_time_offset", "price", "change", "percent_change"]
    d["pull_dt"] = str(gathered_utc)
    data = d.to_dict(orient='records')

    # Writing to bucket
    object.put(Body=json.dumps(data))

    # Creating response object --- used while creating script
    response = {
        "statusCode": 200,
        "data": data
    }
    return json.dumps(response)

if __name__ == "__main__":
    get_price(' ', ' ')
