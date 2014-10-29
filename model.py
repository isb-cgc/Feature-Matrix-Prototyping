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

from google.appengine.ext import ndb

class Feature(ndb.Model):
  sample = ndb.StringProperty()
  feature = ndb.StringProperty()
  value = ndb.StringProperty()


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
