##Setting Working Directory
setwd("U:/Title II")

##Loading All Data
tii23_cohort_work<-read.csv("tii23_cohort_work.csv",header=TRUE)
fall_2022<-read.csv("fall_2022.csv",header=TRUE)
spring_2023<-read.csv("spring_2023.csv",header=TRUE)
winter_2023<-read.csv("winter_2023.csv",header=TRUE)
summer_2023<-read.csv("summer_2023.csv",header=TRUE)

##Install dplyr
install.packages("dplyr")

##Load dplyr
library(dplyr)

##Merging Tables 
##Left Join Includes All Rows From tii23_cohort_work 
##only matching rows from subsequent tables 
merged_data <- tii23_cohort_work %>%
  left_join(fall_2022, by = "ID") %>%
  left_join(spring_2023, by = "ID") %>%
  left_join(winter_2023, by = "ID")

##Install writex1
install.packages("writexl")

##Load writex1
library(writexl)

##Export Merged Data as Excel File 
write_xlsx(merged_data, path = "merged_data.xlsx")

##Merging in Summer 
fws<-read.csv("merged_data_fws.csv",header=TRUE)
merged_data_2 <- fws %>%
  left_join(summer_2023, by = "ID")

write_xlsx(merged_data_2, path = "merged_data_2.xlsx")






