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

import cloudstorage as gcs
import logging
import util

from google.appengine.api import search
from google.appengine.ext import deferred

def feature_to_document(feature):
  tokens = feature.split(":")
  if len(tokens) != 8:
    logging.ERROR("Couldn't split feature \"%s\" into 8 tokens" % feature)
    return None
  document = search.Document(
    doc_id = feature,
    fields=[
       search.TextField(name='feature', value=feature),
       search.TextField(name='value_type', value=tokens[0]),
       search.TextField(name='feature_kind', value=tokens[1]),
       search.TextField(name='label', value=tokens[2]),
       search.TextField(name='chromosome', value=tokens[3]),
       search.TextField(name='start', value=tokens[4]),
       search.TextField(name='stop', value=tokens[5]),
       search.TextField(name='strand', value=tokens[6]),
       search.TextField(name='other', value=tokens[7]),
       ])
  return document

def import_into_index(document_or_list):
  count = 1
  if isinstance(document_or_list, list):
    count = len(document_or_list)
  try:
    index = search.Index(name="featureIndex")
    index.put(document_or_list)
  except search.Error:
    logging.error("Couldn't put %s document(s) in the search index." % count)
  logging.info("Put %d new items into the search index." % count)
  return count

def import_feature_into_index(feature):
  return import_into_index(feature_to_document(feature))


def import_gcs_file_features_into_index(filename, offset=0):
  # Assumes filename is valid (i.e. util.validate_gsc_filename() was called.)
  with gcs.open(filename) as file:
    batch = 0
    count = 0
    documents = []
    for feature in file:
      count += 1
      if count <= offset:
        continue;
      feature = feature.rstrip('\n')
      documents.append(feature_to_document(feature))
      batch += 1
      if batch == 200:
        import_into_index(documents)
        logging.info("Deferred processing at offset: %d." % count)
        deferred.defer(import_gcs_file_features_into_index, filename, count)
        return count
    if batch > 0:
      import_into_index(documents)
      logging.info("Done with import of %d items." % count)
  return count

def search_features(query_string):
  features = []
  sort1 = search.SortExpression(expression='feature',
                                direction=search.SortExpression.ASCENDING,
                                default_value="")
  sort_opts = search.SortOptions(expressions=[sort1])

  query_options = search.QueryOptions(
    limit=50,
    returned_fields=['feature'],
    sort_options=sort_opts)

  query = search.Query(query_string=query_string, options=query_options)
  try:
    index = search.Index(name="featureIndex")
    search_result = index.search(query)
    for document in search_result.results:
      features.append(document.fields[0].value)
  except search.Error:
    logging.error("There was an error running the search on \"%s\"."
                  % query_string)

  return features
