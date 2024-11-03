library(tidyverse)

setwd("~/4262")

getSum <- function(fn) {
   read_csv(fn) %>%
     mutate(is_m6a=score>0.5) %>% `$`(is_m6a) %>% sum()
}

A51 <- getSum('SGNex_A549_directRNA_replicate5_run1.csv.gz')
A61 <- getSum('SGNex_A549_directRNA_replicate6_run1.csv.gz')
mean_A <- mean(c(A51, A61))

Hc31 <- getSum('SGNex_Hct116_directRNA_replicate3_run1.csv.gz')
Hc34 <- getSum('SGNex_Hct116_directRNA_replicate3_run4.csv.gz')
Hc43 <- getSum('SGNex_Hct116_directRNA_replicate4_run3.csv.gz')
mean_Hc <- mean(c(Hc31, Hc34, Hc43))

He52 <- getSum('SGNex_HepG2_directRNA_replicate5_run2.csv.gz')
He61 <- getSum('SGNex_HepG2_directRNA_replicate6_run1.csv.gz')
mean_H <- mean(c(He52, He61))

K41 <- getSum('SGNex_K562_directRNA_replicate4_run1.csv.gz')
K51 <- getSum('SGNex_K562_directRNA_replicate5_run1.csv.gz')
K61 <- getSum('SGNex_K562_directRNA_replicate6_run1.csv.gz')
mean_K <- mean(c(K41, K51, K61))

M31 <- getSum('SGNex_MCF7_directRNA_replicate3_run1.csv.gz')
M41 <- getSum('SGNex_MCF7_directRNA_replicate4_run1.csv.gz')
mean_M <- mean(c(M31, M41))

kruskal.test(c(mean_A, mean_Hc, mean_H, mean_K, mean_M), c('A549', 'Hct116', 'HepG2', 'K562', 'MCF7'))

boxplot(list(
  A549=c(A51, A61),
  Hct116=c(Hc31, Hc34, Hc43),
  HepG2=c(He52, He61),
  K562=c(K41, K51, K61),
  MCF7=c(c(M31, M41))
))
