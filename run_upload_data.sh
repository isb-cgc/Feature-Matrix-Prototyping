#!/bin/bash
#
# Replace filename and remove --dry-run to actually run the import
#
appcfg.py upload_data \
    --application=s~zettaneerpdq \
    --url=http://zettaneerpdq.appspot.com/_ah/remote_api \
    --config_file=bulkloader.yaml \
    --kind=FeatureMetadata \
    --filename=featuremetadata.csv \
    --dry_run
