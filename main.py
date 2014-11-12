"""
Copyright 2014 Google Inc. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import base64
import jinja2
import json
import logging
import model
import pickle
import search
import time
import webapp2
import urllib
import util

from collections import OrderedDict
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api.logservice import logservice
from google.appengine.ext import ndb

from pipeline import PipelineImportData


JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader("templates"),
  autoescape=True,
  extensions=["jinja2.ext.autoescape"])


class MainHandler(webapp2.RequestHandler):
  """The main page."""

  def get(self):
    #model.put_sample_data()
    self._render_page()

  def post(self):
    # Render the page.
    viewstate = base64.b64decode(self.request.get("viewstate"))
    if viewstate:
      viewstate = pickle.loads(viewstate)
    searchFeature = str(self.request.get("searchFeature"))
    searchFeatureResults = viewstate
    lookupFeature = str(self.request.get("lookupFeature"))
    lookupFeatureResults = None
    lookupSample = str(self.request.get("lookupSample"))
    lookupSampleFeatureResults = None
    alertMessage = None
    alertLevel = None
    if self.request.get("submitSearchFeature"):
      searchFeatureResults = search.search_features(searchFeature)
      alertMessage = ("Found %d features that matched the search for \"%s\"."
          % (len(searchFeatureResults), searchFeature))
      alertLevel = "alert-success"
    if self.request.get("submitLookupFeature"):
      lookupFeatureResults = model.get_results_by_feature(lookupFeature)
      if len(lookupFeatureResults) > 0:
        lookupSample = lookupFeatureResults[0].sample
    if self.request.get("submitSampleFeature"):
      lookupSampleFeatureResults = (
          model.get_value_by_feature_sample(lookupFeature, lookupSample))
    if self.request.get("submitRebuildNameValues"):
      count = self._rebuild_name_values()
      alertMessage = "We rebuilt %d name/value items." % count
      alertLevel = "alert-success"
    if self.request.get("submitRebuildSearch"):
      filename = str(self.request.get("importFilename"))
      alertMessage, alertLevel = self._rebuild_search(filename)
    if self.request.get("submitImport"):
      filename = str(self.request.get("importFilename"))
      filename = util.validate_gsc_filename(filename)
      if not filename:
        alertMessage = "Please provide the url/path to a valid GCS file."
        alertLevel = "alert-danger"
      else:
        blob_key = util.get_blob_key_from_gcs_file(filename)
        file_size = util.get_size_from_gcs_file(filename)
        pipeline = PipelineImportData([blob_key], {blob_key: file_size}, 100)
        pipeline.start()
        self.redirect('%s/status?root=%s' %
                      (pipeline.base_path, pipeline.pipeline_id))
    viewstate = base64.b64encode(pickle.dumps(searchFeatureResults))
    self._render_page(viewstate, searchFeature, searchFeatureResults,
                      lookupFeature, lookupFeatureResults,
                      lookupSample, lookupSampleFeatureResults,
                      alertMessage, alertLevel)

  def _render_page(self, viewstate="", searchFeature="", searchFeatureResults=None,
                   lookupFeature="", lookupFeatureResults=None,
                   lookupSample="", lookupSampleFeatureResults=None,
                   alertMessage=None, alertLevel=None):
    username = "anonymous user"
    if users.get_current_user():
      username = users.User().nickname()
    template = JINJA_ENVIRONMENT.get_template("index.html")
    self.response.out.write(template.render({
      "viewstate": viewstate,
      "searchFeature": searchFeature,
      "searchFeatureResults": searchFeatureResults,
      "lookupFeature": lookupFeature,
      "lookupFeatureResults": lookupFeatureResults,
      "lookupSample": lookupSample,
      "lookupSampleFeatureResults": lookupSampleFeatureResults,
      "path": self.request.path,
      "username": username,
      "version": util.get_app_version(),
      "alertMessage": alertMessage,
      "alertLevel": alertLevel,
    }))

  def _rebuild_name_values(self):
    count = 0
    names = ["feature_kind", "chromosome"]
    for name in names:
      values = model.get_from_feature_distict(name)
      count += model.rebuild_name_value(name, values)
      values = model.get_values_for(name)
    return count

  def _rebuild_search(self, filename):
    alertMessage = None
    alertLevel = None
    filename = util.validate_gsc_filename(filename)
    if not filename:
      alertMessage = "Please provide the url/path to a valid GCS file."
      alertLevel = "alert-danger"
    else:
      count = search.import_gcs_file_features_into_index(filename)
      alertMessage = ("We rebuilt the first %d search items. "
          "Please wait while we rebuild the rest." % count)
      alertLevel = "alert-success"
    return (alertMessage, alertLevel)

class GetValuesHandler(webapp2.RequestHandler):
  _MAX_ITEMS_REQUEST = 50

  def get(self):
    features = str(self.request.get("features")).split(" ")
    samples = str(self.request.get("samples")).split(" ")
    format = str(self.request.get("format"))
    respone = {}
    if features == ['']:
      response = {
          "error": "You must specify one or more features."
      }
    elif samples == [''] and len(features) > 3:
      response = {
          "error": "If you are requesting all samples then you can only select "
          " up to 3 features."
      }
    elif len(features) > self._MAX_ITEMS_REQUEST:
      response = {
          "error": "You can request at most %d features." %
              self._MAX_ITEMS_REQUEST
      }
    elif len(samples) > self._MAX_ITEMS_REQUEST:
      response = {
          "error": "You can request at most %d samples." %
              self._MAX_ITEMS_REQUEST
      }
    else:
      if format == "matrix":
        response = model.get_matrix_by_features_samples(features, samples)
      else:
        response = model.get_values_by_features_samples(features, samples)
    self.response.write(json.dumps(response))


app = webapp2.WSGIApplication(
  [
    ("/", MainHandler),
    ("/api/getvalues", GetValuesHandler),
  ],
  debug=True)

