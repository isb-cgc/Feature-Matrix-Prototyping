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
import csv
import logging
import os
import StringIO

from mapreduce import base_handler
from mapreduce import mapper_pipeline
from mapreduce import operation

from model import FeatureMetadata2

def insert_data(item):
  """Insert map handler. Puts entities from a csv file into the datastore.

  Args:
    item: pair (offset, line) from BlobstoreLineInputReader,
        BlobstoreZipInputReader, or similar.

  Yields:
    A db operation to store the entity.
  """
  offset, value = item
  mem_file = StringIO.StringIO(value)
  for line in csv.reader(mem_file, delimiter=','):
    if (len(line) == 11):
      feature = FeatureMetadata2(sample=line[0],
                                feature=line[1],
                                value=line[2],
                                value_type=line[3],
                                feature_kind=line[4],
                                label=line[5],
                                chromosome=line[6],
                                start=line[7],
                                stop=line[8],
                                strand=line[9],
                                other=line[10])
      yield operation.db.Put(feature)

class PipelineImportData(base_handler.PipelineBase):
  """A pipeline to import data"""

  def run(self, blob_keys, blob_sizes, shards):
    yield mapper_pipeline.MapperPipeline(
      "import_data_mapper",
      "pipeline.insert_data",
      "mapreduce.input_readers.BlobstoreLineInputReader",
      params={
              "blob_keys": blob_keys,
              "blob_sizes": blob_sizes,
      },
      shards=shards)




