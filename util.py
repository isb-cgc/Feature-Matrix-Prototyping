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
import datetime
import logging
import os

from google.appengine.ext import blobstore

def get_app_version():
  version = os.environ["CURRENT_VERSION_ID"].split(".")
  name = version[0]
  date = datetime.datetime.fromtimestamp(long(version[1]) >> 28)
  if os.environ["SERVER_SOFTWARE"].startswith("Development"):
    date = datetime.datetime.now()
  return name + " as of " + date.strftime("%Y-%m-%d %X")

def get_blob_key_from_gcs_file(filename):
  filename = _prep_gcs_filename(filename)
  blob_key = blobstore.create_gs_key('/gs' + filename)
  logging.warn("Blobkey: %s" % str(blob_key))
  blob_info = blobstore.get(blob_key)
  if blob_info is not None:
    logging.warn("BlobInfo: %d" % blob_info.size)
  else:
    logging.warn("BlobInfo is None!")
  return blob_key

def get_size_from_gcs_file(filename):
  filename = _prep_gcs_filename(filename)
  stat = gcs.stat(filename)
  logging.warn("GCSstat: %r" % repr(stat))
  return stat.st_size

def _prep_gcs_filename(filename):
  # Strip out "gs://" and ensure it starts with "/"
  prefix = "gs://"
  if filename.startswith(prefix):
    filename = filename[len(prefix):]
  if not filename.startswith("/"):
    filename = "/" + filename
  return filename