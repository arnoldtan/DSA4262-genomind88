library(tidyverse)

 <- function(x) {
   read_csv('SGNex_A549_directRNA_replicate5_run1.csv.gz') %>%
     mutate(is_m6a=score>0.5) %>% `$`(is_m6a) %>% sum()
}