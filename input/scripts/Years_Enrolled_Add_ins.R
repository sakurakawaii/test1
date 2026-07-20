##Setting Working Directory
setwd("U:/Title II")

##Loading All Data
addins<-read.csv("addins.csv",header=TRUE)
fall_2019_YE<-read.csv("orion_eot_fall2019_official.csv",header=TRUE)
spring_2020_YE<-read.csv("orion_eot_spring2020_official.csv",header=TRUE)
fall_2020_YE<-read.csv("orion_fall2020_ess_official.csv",header=TRUE)
spring_2021_YE<-read.csv("orion_sprg2021_ess_official.csv",header=TRUE)
spring_2019_YE<-read.csv("orion_eot_spring2019_official.csv",header=TRUE)
fall_2018_YE<-read.csv("orion_eot_fall2018_official.csv",header=TRUE)
fall_2021_YE<-read.csv("orion_eot_fall2021_official.csv",header=TRUE)
spring_2018_YE<-read.csv("orion_eot_spring2018_official.csv",header=TRUE)
fall_2017_YE<-read.csv("orion_eot_fall2017_official.csv",header=TRUE)
spring_2022_YE<-read.csv("orion_eot_spring2022_official.csv",header=TRUE)
fall_2022_YE<-read.csv("orion_eot_fall2022_official.csv",header=TRUE)
spring_2023_YE<-read.csv("orion_eot_spring2023_official.csv",header=TRUE)
fall_2023_YE<-read.csv("orion_ess_fall2023_official.csv",header=TRUE)

##Load dplyr
library(dplyr)

##Merging Tables 
##Left Join Includes All Rows From add ins 
##only matching rows from other tables
##Selecting only HEH Column
##HEH Column Renamed By Term 
years_enrolled_ad_ins <- addins %>%
  left_join(select(fall_2019_YE,id, F19_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(spring_2020_YE,id, S20_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(fall_2020_YE,id, F20_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(spring_2021_YE,id, S21_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(spring_2019_YE,id, S19_HEH = HIGHER_ED_HIST), 
            by = "id")  %>%
  left_join(select(fall_2018_YE,id, F18_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(fall_2021_YE,id, F21_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(spring_2018_YE,id, S18_HEH = HIGHER_ED_HIST), 
          by = "id") %>%
  left_join(select(fall_2017_YE,id, F17_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(spring_2022_YE,id, S22_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(fall_2022_YE,id, F22_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(spring_2023_YE,id, S23_HEH = HIGHER_ED_HIST), 
          by = "id") %>%
  left_join(select(fall_2023_YE,id, F23_HEH = HIGHER_ED_HIST), 
            by = "id") 


##Load writex1
library(writexl)

##Export Merged Data as Excel File 
write_xlsx(years_enrolled_ad_ins, 
           path = "years_enrolled_ad_ins.xlsx")