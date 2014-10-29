#!/bin/bash

#bq load -F '\t' \
#    --max_bad_records=1 \
#    --skip_leading_rows=1 \
#    ISB.brca_tcga_20141012_tokens \
#    gs://zettaneerpdq-bucket1/genomics/ISB/brca_tcga_20141012_namevalue_tokens.tsv.gz \
#    sample:string,feature:string,value:string,value_type:string,feature_kind:string,label:string,chromosome:string,start:string,stop:string,strand:string,other:string

bq load ISB.brca_tcga_20141012_featuremetadata \
    gs://zettaneerpdq-bucket1/genomics/ISB/brca_tcga_20141012_featuremetadata.csv.gz \
    sample:string,feature:string,value:string,value_type:string,feature_kind:string,label:string,chromosome:string,start:string,stop:string,strand:string,other:string

