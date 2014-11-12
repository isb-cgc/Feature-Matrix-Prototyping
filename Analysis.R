print("Running Genomic Feature Matrix Analysis")

install(jsonlite)
library(jsonlite)

print("First analysis is comparing 2 features across all samples")

# Enter here the 2 features you want to compare
feature1 <- "B:GNAB:TP53:chr17:7565097:7590863:-:bound_delta_ge_2_somatic"
feature2 <- "B:GNAB:TP53:chr17:7565097:7590863:-:bound_delta_ge_3_somatic"

base_url <- "http://genomicsfeatures.zettaneerpdq.appspot.com/api/getvalues"
url <- paste(baseurl, "?features=", feature1, "%20", feature2, "&format=matrix", sep="")
json_file <- "/tmp/json_file"

download.file(url, json_file)
json_data <- fromJSON(json_file)

my_matrix <- json_data$values
# Convert the matrix to numeric values
my_matrix <- matrix(as.numeric(my_matrix), nrow=nrow(my_matrix), ncol=ncol(my_matrix))
colnames(my_matrix) <- json_data$columns
rownames(my_matrix) <- json_data$rows
my_matrix

my_dataframe = data.frame(my_matrix)

cor(my_dataframe, use="pairwise.complete.obs", method="kendall")
