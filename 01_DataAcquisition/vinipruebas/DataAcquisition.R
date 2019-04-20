require(xml2)
library('rvest')
#install.packages('XML')
library('XML')
library('dplyr')

#URL1
url1 <- 'https://labodega.consum.es/catalogo'
webpage1 <- read_html(url1)
cat1 <- html_nodes(webpage1, ".winebox__image")
cat1
class(cat1)
cat11 <- html_node(cat1, "a")
cat11
cat11[[400]]
cat12 <- html_node(cat1, "img")
cat12

bind_rows(lapply(xml_attrs(cat11), function(x) data.frame(as.list(x), stringsAsFactors = FALSE)))

#URL2
url2 <- 'https://labodega.consum.es/tintos/rocamora-075l'
webpage2 <- read_html(url2)
cat2 <- html_nodes(webpage2, ".wine-tag-row")
cat2
html_text(cat2)
