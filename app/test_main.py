from fastapi.testclient import TestClient
from fastapi import FastAPI, Header, HTTPException

from main import *
import base64

client = TestClient(app)

endpoints = ['/', '/api/encode/', '/api/decode/']


real_user = config.USER+":"+config.USER_PASSW
user_encoded_to_b64 = base64.b64encode(real_user.encode()).decode('utf-8')

fake_user = b"somefakeuser:1223"
fake_user_encoded_to_b64 = base64.b64encode(fake_user)


class TestMain:

    def test_no_auth_all_paths(self):

        resp = {"detail": "Not authenticated"}

        for i in endpoints:
            print("PART {}".format(i))

            response = client.get(i)
            assert response.status_code == 401 and response.json() == resp

            response = client.post(i)
            assert response.status_code == 401 and response.json() == resp


    def test_bad_credentials(self):

        resp = {"detail": "Invalid authentication credentials"}

        for i in endpoints:

            response = client.get(i, headers={"WWW-authenticate": "Basic",
                                              "Authorization": "Basic {}".format(fake_user_encoded_to_b64)})

            assert response.status_code == 401 and response.json() == resp

            response = client.post(i, headers={"WWW-authenticate": "Basic",
                                               "Authorization": "Basic {}".format(fake_user_encoded_to_b64)})

            assert response.status_code == 401 and response.json() == resp


    def test_auth_all_get_paths(self):

        for i in endpoints:
            response = client.get(i, headers={"WWW-authenticate": "Basic",
                                              "Authorization": "Basic {}".format(user_encoded_to_b64)})

            assert response.status_code == 200


    def test_encode_and_decode_message(self):

        test_message: dict = {"message": "somemessage"}

        response = client.post(endpoints[1], headers={"WWW-authenticate": "Basic",
                                                      "Authorization": "Basic {}".format(user_encoded_to_b64)},
                               json=test_message)

        data = response.json()

        assert response.status_code == 200

        response = client.post(endpoints[2], headers={"WWW-authenticate": "Basic",
                                                      "Authorization": "Basic {}".format(user_encoded_to_b64)},
                               json={"message": data['message'], "public_key": data['public_key']})

        data_decrypted = response.json()
        assert response.status_code == 200 and data_decrypted['message'] == test_message['message']


    def test_encode_and_decode_withespaces(self):

        test_message: dict = {"message": '\n \t \t \v \b \r \f \a \\ \' \" '}

        response = client.post(endpoints[1], headers={"WWW-authenticate": "Basic",
                                                      "Authorization": "Basic {}".format(user_encoded_to_b64)},
                               json=test_message)

        data = response.json()

        assert response.status_code == 200

        response = client.post(endpoints[2], headers={"WWW-authenticate": "Basic",
                                                      "Authorization": "Basic {}".format(user_encoded_to_b64)},
                               json={"message": data['message'], "public_key": data['public_key']})

        data_decrypted = response.json()

        assert response.status_code == 200 and data_decrypted['message'] == test_message['message']

    def test_encode_and_decode_without_message(self):

        test_message: dict = {"message": ""}

        for i in endpoints:
            response = client.post(i, headers={"WWW-authenticate": "Basic",
                                               "Authorization": "Basic {}".format(user_encoded_to_b64)},
                                   json=test_message)

            assert response.status_code == 422


    def test_decode_without_pubkey(self):

        test_message: dict = {"message": "somemessage"}
        resp = {"detail": "No public_key given, impossible to decode"}

        response = client.post(endpoints[2], headers={"WWW-authenticate": "Basic",
                                                      "Authorization": "Basic {}".format(user_encoded_to_b64)},
                               json=test_message)

        assert response.status_code == 422 and response.json() == resp
