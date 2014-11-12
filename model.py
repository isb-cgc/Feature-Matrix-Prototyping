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

def put_sample_data():
  # http://localhost:8080/api/getvalues?features=B:GNAB:TP53:chr17:7565097:7590863:-:DNA_interface_somatic%20B:GNAB:TP53:chr17:7565097:7590863:-:bound_delta_ge_10_somatic%20B:GNAB:TP53:chr17:7565097:7590863:-:bound_delta_ge_2_somatic&samples=TCGA-07-0227-20%20TCGA-3C-AAAU-01%20TCGA-3C-AALI-01
  FeatureMetadata2(feature="B:GNAB:TP53:chr17:7565097:7590863:-:DNA_interface_somatic",
                   sample="TCGA-07-0227-20", value="1").put()
  FeatureMetadata2(feature="B:GNAB:TP53:chr17:7565097:7590863:-:bound_delta_ge_10_somatic",
                   sample="TCGA-07-0227-20", value="4").put()
  FeatureMetadata2(feature="B:GNAB:TP53:chr17:7565097:7590863:-:bound_delta_ge_2_somatic",
                   sample="TCGA-07-0227-20", value="7").put()
  FeatureMetadata2(feature="B:GNAB:TP53:chr17:7565097:7590863:-:DNA_interface_somatic",
                   sample="TCGA-3C-AAAU-01", value="2").put()
  FeatureMetadata2(feature="B:GNAB:TP53:chr17:7565097:7590863:-:bound_delta_ge_10_somatic",
                   sample="TCGA-3C-AAAU-01", value="5").put()
  FeatureMetadata2(feature="B:GNAB:TP53:chr17:7565097:7590863:-:bound_delta_ge_2_somatic",
                   sample="TCGA-3C-AAAU-01", value="8").put()
  FeatureMetadata2(feature="B:GNAB:TP53:chr17:7565097:7590863:-:DNA_interface_somatic",
                   sample="TCGA-3C-AALI-01", value="3").put()
  FeatureMetadata2(feature="B:GNAB:TP53:chr17:7565097:7590863:-:bound_delta_ge_10_somatic",
                   sample="TCGA-3C-AALI-01", value="6").put()
  FeatureMetadata2(feature="B:GNAB:TP53:chr17:7565097:7590863:-:bound_delta_ge_2_somatic",
                   sample="TCGA-3C-AALI-01", value="9").put()

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
  features = query.fetch(2000)
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

def get_value_by_feature_sample(feature, sample):
  query = FeatureMetadata2.query(FeatureMetadata2.feature == feature,
                                 FeatureMetadata2.sample == sample)
  features = query.fetch(1)
  value_only = "No value found for this sample and feature."
  for feature in features:
    value_only = feature.value
  return value_only

def get_values_by_features_samples(features, samples):
  query = []
  if samples == ['']:
    query = FeatureMetadata2.query(FeatureMetadata2.feature.IN(features))
  else:
    query = FeatureMetadata2.query(FeatureMetadata2.feature.IN(features),
                                   FeatureMetadata2.sample.IN(samples))
  results = query.fetch(1000)
  values = []
  for result in results:
    values.append({
        "feature": result.feature,
        "sample": result.sample,
        "value": result.value
    })
  return values

def get_matrix_by_features_samples(features, samples):
  query = []
  if samples == ['']:
    query = FeatureMetadata2.query(FeatureMetadata2.feature.IN(features))
    # get_all_distinct_samples is an expensive call that we probably don't
    # need to do every time.
    samples = get_all_distinct_samples()
  else:
    query = FeatureMetadata2.query(FeatureMetadata2.feature.IN(features),
                                   FeatureMetadata2.sample.IN(samples))
  results = query.fetch(10000)
  rows = len(features)
  cols = len(samples)
  values = []
  for _ in range(rows):
    values.append([None] * cols)
  for result in results:
    values[features.index(result.feature)][samples.index(result.sample)] = result.value
  matrix = {
    "rows": features,
    "columns": samples,
    "values": values,
  }
  return matrix


def get_results_by_feature(feature):
  query = (FeatureMetadata2.query(FeatureMetadata2.feature == feature)
      .order(FeatureMetadata2.sample))
  features = query.fetch(100)
  return features

