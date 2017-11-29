#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import loads, dumps
from requests import Session

from .common import *


class UtilTester:

    def __init__(self, ut_self):
        # create a session, simulating a browser. It is necessary to create cookies on server
        self.session = Session()
        # headers
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        # unittest self
        self.ut_self = ut_self

    # login and logout

    def auth_login(self):
        response = self.session.get('http://localhost:8888/auth/login/fake/')

        self.ut_self.assertEqual(response.status_code, 200)

    def auth_logout(self):
        response = self.session.get('http://localhost:8888/auth/logout')

        self.ut_self.assertEqual(response.status_code, 200)

    # USER

    def api_user(self, expected, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get('http://localhost:8888/api/user/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

    # user errors - get

    def api_user_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get('http://localhost:8888/api/user/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_user_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get('http://localhost:8888/api/user/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # PROJECT

    def api_project(self, expected, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get('http://localhost:8888/api/project/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

    def api_project_create(self, project_json):
        response = self.session.put('http://localhost:8888/api/project/create/',
                                    data=dumps(project_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of changeset
        project_json["project"]["properties"]["id"] = resulted["id"]

        return project_json

    def api_project_delete(self, feature_id):
        response = self.session.delete('http://localhost:8888/api/project/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 200)

    # project errors - get

    def api_project_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get('http://localhost:8888/api/project/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_project_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get('http://localhost:8888/api/project/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # project errors - create

    def api_project_create_error_403_forbidden(self, project_json):
        response = self.session.put('http://localhost:8888/api/project/create/',
                                    data=dumps(project_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    # project errors - delete

    def api_project_delete_error_400_bad_request(self, feature_id):
        response = self.session.delete('http://localhost:8888/api/project/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_project_delete_error_403_forbidden(self, feature_id):
        response = self.session.delete('http://localhost:8888/api/project/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_project_delete_error_404_not_found(self, feature_id):
        response = self.session.delete('http://localhost:8888/api/project/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 404)

    # CHANGESET

    def api_changeset(self, expected, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get('http://localhost:8888/api/changeset/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(expected, resulted)

        # if expected_at_least is not None:
        #     """
        #     Test Case: Changesets can not be removed, because of this, the result of the returned
        #     changesets may be larger than expected (because there are other tests that create
        #     changesets). Because of this I pass a subset of minimum changesets that have to exist.
        #     """
        #
        #     """ Explanation: Generator creating booleans by looping through list
        #         'expected_at_least["features"]', checking if that item is in list 'resulted["features"]'.
        #         all() returns True if every item is truthy, else False.
        #         https://stackoverflow.com/questions/16579085/python-verifying-if-one-list-is-a-subset-of-the-other
        #     """
        #     __set__ = resulted["features"]  # set returned
        #     __subset__ = expected_at_least["features"]  # subset expected
        #
        #     # verify if the elements of a subset is in a set, if OK, return True, else False
        #     resulted_bool = all(element in __set__ for element in __subset__)
        #
        #     self.ut_self.assertTrue(resulted_bool)

    def api_changeset_create(self, changeset_json):
        # do a GET call, sending a changeset to add in DB
        response = self.session.put('http://localhost:8888/api/changeset/create/',
                                    data=dumps(changeset_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of changeset
        changeset_json["changeset"]["properties"]["id"] = resulted["id"]

        return changeset_json

    def api_changeset_close(self, changeset_id):
        response = self.session.put('http://localhost:8888/api/changeset/close/{0}'.format(changeset_id))

        self.ut_self.assertEqual(response.status_code, 200)

    def api_changeset_delete(self, feature_id):
        response = self.session.delete('http://localhost:8888/api/changeset/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 200)

    # project errors - get

    def api_changeset_error_400_bad_request(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get('http://localhost:8888/api/changeset/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_changeset_error_404_not_found(self, **arguments):
        arguments = get_url_arguments(**arguments)

        response = self.session.get('http://localhost:8888/api/changeset/{0}'.format(arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # changeset errors - create

    def api_changeset_create_error_403_forbidden(self, changeset_json):
        # do a GET call, sending a changeset to add in DB
        response = self.session.put('http://localhost:8888/api/changeset/create/',
                                    data=dumps(changeset_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    # changeset errors - close

    def api_changeset_close_error_400_bad_request(self, changeset_id):
        response = self.session.put('http://localhost:8888/api/changeset/close/{0}'.format(changeset_id))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_changeset_close_error_403_forbidden(self, changeset_id):
        response = self.session.put('http://localhost:8888/api/changeset/close/{0}'.format(changeset_id))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_changeset_close_error_404_not_found(self, changeset_id):
        response = self.session.put('http://localhost:8888/api/changeset/close/{0}'.format(changeset_id))

        self.ut_self.assertEqual(response.status_code, 404)

    # project errors - delete

    def api_changeset_delete_error_400_bad_request(self, feature_id):
        response = self.session.delete('http://localhost:8888/api/changeset/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_changeset_delete_error_403_forbidden(self, feature_id):
        response = self.session.delete('http://localhost:8888/api/changeset/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_changeset_delete_error_404_not_found(self, feature_id):
        response = self.session.delete('http://localhost:8888/api/changeset/{0}'.format(feature_id))

        self.ut_self.assertEqual(response.status_code, 404)

    # ELEMENT

    def api_element(self, element, element_expected, **arguments):
        # get the arguments of the URL
        arguments = get_url_arguments(**arguments)

        # do a GET call with default format (GeoJSON)
        response = self.session.get('http://localhost:8888/api/{0}/{1}'.format(element, arguments))

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertEqual(element_expected, resulted)

    def api_element_create(self, element_json):
        multi_element = element_json["features"][0]["geometry"]["type"]
        element = by_multi_element_get_url_name(multi_element)

        # do a PUT call, sending a node to add in DB
        response = self.session.put('http://localhost:8888/api/{0}/create/'.format(element),
                                    data=dumps(element_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 200)

        list_of_id_of_features_created = loads(response.text)  # convert string to dict/JSON

        # add the id of the feature for each feature created
        for feature, id_feature in zip(element_json["features"], list_of_id_of_features_created):
            feature["properties"]["id"] = id_feature

        return element_json

    def api_element_delete(self, element, element_id):
        response = self.session.delete('http://localhost:8888/api/{0}/{1}'.format(element, element_id))

        self.ut_self.assertEqual(response.status_code, 200)

    def verify_if_element_was_add_in_db(self, element_json_expected):
        element_id = element_json_expected["features"][0]["properties"]["id"]  # get the id of element

        multi_element = element_json_expected["features"][0]["geometry"]["type"]

        element = by_multi_element_get_url_name(multi_element)

        self.api_element(element, element_json_expected, element_id=element_id)

    def verify_if_element_was_not_add_in_db(self, element_json_expected):
        element_id = element_json_expected["features"][0]["properties"]["id"]  # get the id of element

        multi_element = element_json_expected["features"][0]["geometry"]["type"]
        element = by_multi_element_get_url_name(multi_element)

        # get the arguments of the URL
        arguments = get_url_arguments(element_id=element_id)

        # do a GET call with default format (GeoJSON)
        response = self.session.get('http://localhost:8888/api/{0}/{1}'.format(element, arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # element errors - get

    def api_element_error_400_bad_request(self, element, element_id):
        arguments = get_url_arguments(element_id=element_id)

        response = self.session.get('http://localhost:8888/api/{0}/{1}'.format(element, arguments))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_element_error_404_not_found(self, element, element_id):
        arguments = get_url_arguments(element_id=element_id)

        response = self.session.get('http://localhost:8888/api/{0}/{1}'.format(element, arguments))

        self.ut_self.assertEqual(response.status_code, 404)

    # element errors - create

    def api_element_create_error_400_bad_request(self, element_json):
        multi_element = element_json["features"][0]["geometry"]["type"]
        element = by_multi_element_get_url_name(multi_element)

        # do a PUT call, sending a node to add in DB
        response = self.session.put('http://localhost:8888/api/{0}/create/'.format(element),
                                    data=dumps(element_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 400)

    def api_element_create_error_403_forbidden(self, element_json):
        multi_element = element_json["features"][0]["geometry"]["type"]
        element = by_multi_element_get_url_name(multi_element)

        # do a PUT call, sending a node to add in DB
        response = self.session.put('http://localhost:8888/api/{0}/create/'.format(element),
                                    data=dumps(element_json), headers=self.headers)

        self.ut_self.assertEqual(response.status_code, 403)

    # element errors - delete

    def api_element_delete_error_400_bad_request(self, element, element_id):
        response = self.session.delete('http://localhost:8888/api/{0}/{1}'.format(element, element_id))

        self.ut_self.assertEqual(response.status_code, 400)

    def api_element_delete_error_403_forbidden(self, element, element_id):
        response = self.session.delete('http://localhost:8888/api/{0}/{1}'.format(element, element_id))

        self.ut_self.assertEqual(response.status_code, 403)

    def api_element_delete_error_404_not_found(self,  element, element_id):
        response = self.session.delete('http://localhost:8888/api/{0}/{1}'.format(element, element_id))

        self.ut_self.assertEqual(response.status_code, 404)

    # others

    def api_capabilities(self):
        response = self.session.get('http://localhost:8888/api/capabilities/')

        self.ut_self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        expected = {"version": "0.0.1", "status": {"database": "online"}}

        self.ut_self.assertNotEqual(resulted, expected)