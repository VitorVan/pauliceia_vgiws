#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""


from ..base import *


# PROJECT


class APIProject(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/project/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/project/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        self.get_method_api_project(param)

    @auth_non_browser_based
    def put(self, param=None):
        self.put_method_api_project(param)

    @auth_non_browser_based
    def delete(self, param=None):
        self.delete_method_api_project(param)


# CHANGESET


class APIChangeset(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/changeset/?(?P<param>[A-Za-z0-9-]+)?/?(?P<param2>[A-Za-z0-9-]+)?",
            ]

    @auth_non_browser_based
    def put(self, param=None, param2=None):
        # param on this case is "create" or "close"
        if param == "create":
            # get the JSON sent, to add in DB
            changeset_json = self.get_the_json_validated()

            current_user_id = self.get_current_user_id()

            try:
                json_with_id = self.PGSQLConn.create_changeset(changeset_json, current_user_id)
            except DataError as error:
                # print("Error: ", error)
                raise HTTPError(500, "Problem when create a changeset. Please, contact the administrator.")

            # Default: self.set_header('Content-Type', 'application/json')
            self.write(json_encode(json_with_id))
        elif param == "close":
            # param2 on this case is the id of changeset
            if param2 is not None and not param2.isdigit():
                raise HTTPError(400, "Invalid parameter.")

            try:
                # close the changeset of id = id_changeset
                self.PGSQLConn.close_changeset(param2)
            except DataError as error:
                # print("Error: ", error)
                raise HTTPError(500, "Problem when close a changeset. Please, contact the administrator.")
        else:
            raise HTTPError(404, "Invalid URL.")


# class APIChangesetCreate(BaseHandler):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/changeset/create/", r"/api/changeset/create"]
#
#     @auth_non_browser_based
#     def put(self):
#         # get the JSON sent, to add in DB
#         changeset_json = self.get_the_json_validated()
#
#         current_user_id = self.get_current_user_id()
#
#         json_with_id = self.PGSQLConn.create_changeset(changeset_json, current_user_id)
#
#         # Default: self.set_header('Content-Type', 'application/json')
#         self.write(json_encode(json_with_id))
#
#
# class APIChangesetClose(BaseHandler):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/changeset/close/(?P<id_changeset>[^\/]+)/",
#             r"/api/changeset/close/(?P<id_changeset>[^\/]+)"]
#
#     @auth_non_browser_based
#     def put(self, id_changeset):
#         # close the changeset of id = id_changeset
#         self.PGSQLConn.close_changeset(id_changeset)
#
#         self.set_and_send_status(status=200, reason="Changeset was closed!")