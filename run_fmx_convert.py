#!/usr/bin/python

import csv
import sys

if len(sys.argv) != 3:
  print "Usage: %s tsv-file-to-convert output-file" % sys.argv[0]
  sys.exit()

input_filename = sys.argv[1]
output_filename = sys.argv[2]
output_header_row = False
output_sep = ","
output_cols = ["sample", 
              "feature",
              "value",
              "value_type",
              "feature_kind",
              "label",
              "chromosome",
              "start",
              "stop",
              "strand",
              "other"]

header = None
columns = 0
with open(output_filename, "w") as output_file:
  writer = csv.writer(output_file, delimiter=output_sep,
                      quoting=csv.QUOTE_MINIMAL)
  with open(input_filename) as input_file:
    for line in csv.reader(input_file, delimiter="\t"):
      if header is None:
        header = line
        columns = len(header)
        if output_header_row:
          writer.writerow(output_cols)
        continue
      feature = line[0]
      for i in range(1, columns):
        output_line = []
        output_line.append(header[i])  # sample
        output_line.append(feature)  # feature
        output_line.append(line[i])  # value
        tokens = feature.split(":")
        if len(tokens) != 8:
          print "The feature: %s could not be broken-up into 8 tokens" % feature
          sys.exit()
        output_line.extend(tokens)
        writer.writerow(output_line)

