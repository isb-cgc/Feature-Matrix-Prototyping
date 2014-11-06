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

import logging

from google.appengine.ext import ndb

class FeatureMetadata2(ndb.Model):
  sample = ndb.StringProperty()
  feature = ndb.StringProperty()
  value = ndb.StringProperty()
  value_type = ndb.StringProperty()
  feature_kind = ndb.StringProperty()
  label = ndb.StringProperty()
  chromosome = ndb.StringProperty()
  start = ndb.StringProperty()
  stop = ndb.StringProperty()
  strand = ndb.StringProperty()
  other = ndb.StringProperty()

class NameValue(ndb.Model):
  name = ndb.StringProperty()
  value = ndb.StringProperty()


def get_from_feature_distict(name):
  query = FeatureMetadata2.query(projection=[name], distinct=True)
  features = query.fetch(100)
  feature_kinds = []
  for feature in features:
    feature_kinds.append(getattr(feature, name))
  return feature_kinds

def rebuild_name_value(name, values):
  # Delete Existing
  query = NameValue.query(NameValue.name == name)
  namevalues = query.fetch(1000, keys_only=True)
  ndb.delete_multi(namevalues)
  # Recreate New
  namevalues = []
  for value in values:
    if value:
      namevalues.append(NameValue(name=name, value=value))
  ndb.put_multi(namevalues)
  return len(namevalues)

def get_values_for(name):
  query = NameValue.query(NameValue.name == name).order(NameValue.value)
  namevalues = query.fetch(1000)
  values = []
  for namevalue in namevalues:
    values.append(namevalue.value)
  return values

def get_all_distinct_samples():
  query = (FeatureMetadata2.query(projection=["sample"], distinct=True)
      .order(FeatureMetadata2.sample))
  features = query.fetch(100)
  samples = []
  for feature in features:
    samples.append(feature.sample)
  return samples

def get_all_distinct_features():
  query = (FeatureMetadata2.query(projection=["feature"], distinct=True)
      .order(FeatureMetadata2.feature))
  features = query.fetch(100)
  features_only = []
  for feature in features:
    features_only.append(feature.feature)
  return features_only

def get_value_by_sample_feature(sample, feature):
  query = FeatureMetadata2.query(FeatureMetadata2.sample == sample,
                                 FeatureMetadata2.feature == feature)
  features = query.fetch(1)
  value_only = "No value found for this sample and feature."
  for feature in features:
    value_only = feature.value
  return value_only

def get_results_by_feature(feature):
  query = (FeatureMetadata2.query(FeatureMetadata2.feature == feature)
      .order(FeatureMetadata2.sample))
  features = query.fetch(100)
  return features

