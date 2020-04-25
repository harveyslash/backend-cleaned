import json

import requests

from itsdangerous import URLSafeTimedSerializer
from flask import current_app

CASS_URL = "http://caas-elb-bcd6465f8d718c2f.elb.ap-south-1.amazonaws.com:3000/submissions?wait=true"


class CaaS:

    @staticmethod
    def get_signature():
        s = URLSafeTimedSerializer(current_app.config["CAAS_SECRET"])
        dump = s.dumps("")
        return dump

    @staticmethod
    def get_outputs(code, language_id, inputs):
        responses = []
        time_taken = []
        memory_used = []

        if code == "":
            return ["" for input in inputs]

        for input in inputs:

            response = requests.post(
                    url=CASS_URL,
                    headers={
                        "Content-Type": "application/json; charset=utf-8",
                    },
                    data=json.dumps({
                        "source_code": code,
                        "stdin": f"{input}",
                        "language_id": language_id,
                        "memory_limit": 256000,
                        "wall_time": 20,
                        "cpu_time_limit": 15,
                        "stack_limit": 128000,
                        "max_file_size": 4096,
                        "wall_time_limit": 20
                    })
            ).json()

            if 'compile_output' in response and response[
                'compile_output'] is not None:
                responses.append(response['compile_output'])
            elif 'stderr' in response and response['stderr'] is not None:
                responses.append(response['stderr'])
            else:
                responses.append(response['stdout'])

            if 'time' in response:
                time_taken.append(response['time'])
            else:
                time_taken.append(None)

            if 'memory' in response:
                memory_used.append(response['memory'])
            else:
                memory_used.append(None)

        return responses, time_taken, memory_used
