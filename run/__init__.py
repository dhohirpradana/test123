import requests
from decouple import config
# from solr import store_to_solr
import json

pipeline_api_url = config('PIPELINE_API_URL')
run_notebook_url = config('RUN_NOTEBOOK_URL')
jsession_url = config('JSESSIONID_URL')
zep_pass = config('ZEP_PASS')
zep_user = config('ZEP_USER')


def get_jsessionid():
    # print('jsession_url: ', jsession_url)
    try:
        response = requests.post(
            jsession_url, {'username': zep_user, 'password': zep_pass})

        if response.status_code != 200:
            return 0

        res = response.json()
        jsession_id = res['Set-Cookie']

        return jsession_id
    except Exception as e:
        print(str(e))
        return 0


def run_pipeline(id):
    # print('run_pipeline id: ', id)
    jsessionid = get_jsessionid()
    url_run = run_notebook_url+'/'+id+'?'+jsessionid
    # print('url_run: ', url_run)
    try:
        response = requests.post(url_run,
                                 headers={'Authorization': ''})

        print('response: ', response.json())
        data=json.dumps(response.json())
        status=json.loads(data)['status']
        # print('data1: ', status)

        # if status is not 200
        if response.status_code != 200 or status != 'OK':
            return 0

        return 1
    except Exception as e:
        print(str(e))
        return 0

# 6396d30614cd970166b9e4ce

def get_pipelines(id):
    errors = []
    success = []
    try:
        response = requests.get(pipeline_api_url+'/'+id,
                                headers={'Authorization': ''})
        json_res = response.json()
        # print('json_res: ', json_res)

        flow_job = json.loads(json_res['flow_job'])
        # print('flow_job: ', flow_job)

        # check if flowJob is not array
        if not isinstance(flow_job, list):
            return print('flowJob is not array')

        for jobs in flow_job:
            # print('jobs: ', jobs)

            if not isinstance(jobs, list):
                return print('job is not array')

            for job in jobs:
                # print('job id: ', job['notebook']['id'])

                # run notebook
                run = run_pipeline(job['notebook']['id'])

                errors.append(job['notebook']['id']) if run == 0 else success.append(
                    job['notebook']['id'])

            # print('jobs1: ', jobs)

        res = {
            'success': json.dumps(success),
            'errors': json.dumps(errors)
        }
        return res
    except Exception as e:
        return str(e)


def handler(request, jsonify):
    # Get the request body
    body = request.get_json()
    print('body:', body)

    # Get the question
    try:
        mg_pipeline_id = body['mgPipelineId']

        # mgPipelineId length must > 0
        if len(mg_pipeline_id) == 0:
            # store_to_solr({})
            return jsonify({
                'message': 'mgPipelineId is required'
            }), 422
    except:
        return jsonify({
            'message': 'mgPipelineId is required'
        }), 422

    res = get_pipelines(id=mg_pipeline_id)

    result = {
        'message': 'Success',
        'res': res,
    }

    return jsonify(result), 200
