
library(igraph)
library(shiny)
library(networkD3)
library(magrittr)
library(poweRlaw)
library(ggplot2)


setwd("C:/Users/Miya/Onedrive/jpm")
link_big <- read.csv("network_simplied.csv", header=T)
dim(link_big)


ibig_repo <- graph_from_data_frame(link_big, directed = TRUE)
V(ibig_repo)$label <- V(ibig_repo)$name # set labels.
V(ibig_repo)$degree <- degree(ibig_repo)



hist(V(ibig_repo)$degree)



V(ibig_repo)$size <- 2
E(ibig_repo)$arrow.size <- 0.4
E(ibig_repo)$color <- 'dark grey'
V(ibig_repo)$frame.color <- NA


V(ibig_repo)$label.cex <- (V(ibig_repo)$degree/(max(V(ibig_repo)$degree)/2)) * 0.3 + .5
E(ibig_repo)$width <- E(ibig_repo)$weight/4
l1 <- layout_with_kk(ibig_repo)


plot(ibig_repo, vertex.shape ='none',layout=layout.auto)


mean(E(iproj1)$weight)
names(sort(betweenness(ibig_repo),decreasing = TRUE)[1:20])

