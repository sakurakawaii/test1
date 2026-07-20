##Setting Working Directory
setwd("U:/Title II")

##Loading All Data
merged_data_2<-read.csv("merged_data_2.csv",header=TRUE)
fall_2019_YE<-read.csv("orion_eot_fall2019_official.csv",header=TRUE)
spring_2020_YE<-read.csv("orion_eot_spring2020_official.csv",header=TRUE)
fall_2020_YE<-read.csv("orion_fall2020_ess_official.csv",header=TRUE)
spring_2021_YE<-read.csv("orion_sprg2021_ess_official.csv",header=TRUE)
spring_2019_YE<-read.csv("orion_eot_spring2019_official.csv",header=TRUE)
fall_2018_YE<-read.csv("orion_eot_fall2018_official.csv",header=TRUE)
fall_2021_YE<-read.csv("orion_eot_fall2021_official.csv",header=TRUE)

##Load dplyr
library(dplyr)

##Merging Tables 
##Left Join Includes All Rows From merged_data_2 
##only matching rows from Fall 2019
##Selecting only HEH Column
##HEH Column Renamed By Term 
merged_data_years_enrolled <- merged_data_2 %>%
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
            by = "id")
  
##Load writex1
library(writexl)

##Export Merged Data as Excel File 
write_xlsx(merged_data_years_enrolled, 
           path = "merged_data_years_enrolled.xlsx")


##Adding More Years 
spring_2018_YE<-read.csv("orion_eot_spring2018_official.csv",header=TRUE)
fall_2017_YE<-read.csv("orion_eot_fall2017_official.csv",header=TRUE)
spring_2022_YE<-read.csv("orion_eot_spring2022_official.csv",header=TRUE)
fall_2022_YE<-read.csv("orion_eot_fall2022_official.csv",header=TRUE)
merged_data_years_enrolled1<-read.csv("merged_data_years_enrolled.csv",
                                      header=TRUE)

##Merging with prior table 
merged_data_years_enrolled_2 <- merged_data_years_enrolled1 %>%
  left_join(select(spring_2018_YE,id, S18_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(fall_2017_YE,id, F17_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(spring_2022_YE,id, S22_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(fall_2022_YE,id, F22_HEH = HIGHER_ED_HIST), 
            by = "id") 

##Export Merged Data as Excel File 
write_xlsx(merged_data_years_enrolled_2, 
           path = "merged_data_years_enrolled_2.xlsx")

##Adding More Years Pt 2 
spring_2023_YE<-read.csv("orion_eot_spring2023_official.csv",header=TRUE)
fall_2023_YE<-read.csv("orion_ess_fall2023_official.csv",header=TRUE)
merged_data_years_enrolled2<-read.csv("merged_data_years_enrolled_2.csv",
                                      header=TRUE)
##Merging with prior table 
merged_data_years_enrolled_3 <- merged_data_years_enrolled2 %>%
  left_join(select(spring_2023_YE,id, S23_HEH = HIGHER_ED_HIST), 
            by = "id") %>%
  left_join(select(fall_2023_YE,id, F23_HEH = HIGHER_ED_HIST), 
            by = "id") 

##Export Merged Data as Excel File 
write_xlsx(merged_data_years_enrolled_3, 
           path = "merged_data_years_enrolled_3.xlsx")


##7 students left at this point, looked up manually, 
##found 2 in 2015, still missing 5 