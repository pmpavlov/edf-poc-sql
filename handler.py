#!/usr/bin/python3

import peter_lambda
import json
import boto3

def getSQLfromS3(bucket,key):
	s3 = boto3.client('s3')
	response = s3.get_object(Bucket=bucket, Key=key)
	return response['Body'].read()

def callOtherLambdaFunc(func,sql):
	lambda_func = boto3.client('lambda')
	sqlStatement = {"sql":sql}

	response_lambda = lambda_func.invoke(
    	FunctionName = func, 
			Payload = json.dumps(sqlStatement, sort_keys=True)
			#Payload = '{"shin":"imai"}'
			#Payload = sqlStatement
	)
	print(response_lambda['Payload'].read().decode("utf-8"))



def handler(event,task):
	#############################################
	## Specify where the SQL file stored in S3 ##
	#############################################
	bucket = "use1-sql"
	sql_file = "uploads/ESTATUS_UPDATE.sql"

	###################################################################
	## Reads the SQL file from S3 bucket and returns entire contents ##
	###################################################################
	body = getSQLfromS3(bucket,sql_file)
	j = peter_lambda.GetSQLFromS3(body,event['sql'])
	sqlArray = j.constructSQL()


	for i in sqlArray: 
		callOtherLambdaFunc(event['func'],i)
		#print(i)

	return "OK. Success"




if __name__ == "__main__":
	#task = "DROP_TEMPORARIES"
	task = "STOP_TIMER"
	#task = "MERGE_BOTH"
	event = {'sql':task, 'func':"Simple-func"}
	handler(event,task)
