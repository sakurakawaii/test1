##Setting Working Directory

##Loading All Data
completers<-read.csv("tii23_cohort_work2.csv",header=TRUE)
data<-read.csv("title_II_match_state_worksheet_NKB.csv",header=TRUE)

##Load dplyr
library(dplyr)

##Merging Tables 
##Left Join Includes All Rows From data 
##only matching rows from completers
##Selecting only Completer, Enrollee, GradDate, Notes, Columns
completers_added <- data %>%
  left_join(select(completers, ID, Completer, Enrollee, GradDate, Notes), 
            by = "ID")

##Load writex1
library(writexl)

##Export Merged Data as Excel File 
write_xlsx(completers_added, 
           path = "completers_added.xlsx")
