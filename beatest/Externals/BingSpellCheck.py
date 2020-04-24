import requests
from flask import current_app


class BingSpellCheck:

    @staticmethod
    def get_spelling_flagged_tokens(text):
        response = requests.post(
                url="https://api.cognitive.microsoft.com/bing/v7.0/SpellCheck",
                params={
                    "mode": "proof",
                    "text": text,
                },
                headers={
                    "Ocp-Apim-Subscription-Key": "9fea4073865b4f108fc831db94fa7126"
                },
        )
        print("-" * 100)
        print(response.content)

        return response.json()['flaggedTokens']
