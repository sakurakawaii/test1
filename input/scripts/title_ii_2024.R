##Title II 2024

##set working directory
setwd("U:/Title_II/2024")

##TED Codes 
TED_codes <- c("PRGR_ACH", "PRGR_CHD", "PRGR_APH", "PRGR_ABI", "PRGR_AEN", "PRGR_PHE", 
               "BA_SST_AAS", "BS_ABI", "MAT_ABI", "BS_ACM", "BA_SST_ECO", "BA_AEN", "MAT_AEN",
               "BS_AES", "BA_SST_GRY", "BA_SST_HIS", "BA_AEM", "BS_AEM", "BA_AFR", "BA_AFS",
               "BA_ASP", "BA_ESL", "BA_ESL_CERT", "BA_ESL_NCRT", "MSED_SLED_NC", "BS_APH",
               "BS_APM", "MAT_APH", "BA_SST_POL", "BA_SST_ANT", "BA_SST_SOC", "BS_ECD", "BS_ECD_ELA",
               "BS_ECD_EST", "BS_ECD_HUM", "BS_ECD_MAT", "BS_ECD_SOS", "BS_ECD_UST", "BS_ECD" ,
               "BS_ECD_ELA" , "BS_ECD_EST", "BS_ECD_HUM", "BS_ECD_MAT","BS_ECD_SOS", "BS_ECI", "BS_ECI_ELAC", 
               "BS_ECI_HUMT", "BS_ECI_SSCH", "BS_ECI_ELEI", "BS_ECI_ESEI", "BS_ECI_HMEI", "BS_ECI_MTEI",
               "BS_ECI_SSEI" , "BS_ECI_USEI", "BS_ECI", "BS_EDC", "MST_CHD", "BS_IEC", "BS_IEC_ELA","BS_IEC_EST",
               "BS_IEC_HUM","BS_IEC_MAT", "BS_IEC_SOS", "BS_IEC","BS_IEC_ELA","BS_IEC_EST", "BS_IEC_HUM", "BS_IEC_MAT",
               "BS_IEC_SOS", "BS_IEC_URSC","CAS_SBL", "CAS_SBL_SDL", "CAS_SDBL", "CAS_SBL_SDL", "CAS_SDL",
               "CT_TL", "MSED_TDA", "MSED_TDA_SEV", "MSED_TSD", "MSED_TSD_SEV", "MSED_TSD","MSED_LED_B-6","MSED_LTE","MSED_LTE", 
               "BSED_HEC", "BSED_HEC_WEL","BSED_HEC","BSED_HEC_CHP","BSED_HEC_WEL","MST_HEA_CRT","MST_HEA_NCRT",
               "MST_HEA_PCRT", "BSED_PEM", "BSED_PEM_ADP", "BSED_PEM_OAE","BSED_PEM", "BSED_PEM_ADP", "BSED_PEM_OAE", "MSED_PEC_ADP",
               "MSED_PEL", "MST_PHE_PENC" , "MST_PHE_PEMC", "MAT_ACH", "BA_SST","BA_SST_ANT","BA_SST_ECO","BA_SST_GRY","BA_SST_HIS",
               "BA_SST_POL","BA_SST_SOC","BS_ACM","BS_AES","BA_AFS","MAT_ACH",
               "BS_ABI","MAT_ABI","BA_AEN","MAT_AEN","BA_AFR","BA_AEM",
               "BS_AEM","BS_APH","MAT_APH","BS_APM", "BA_ASP","BS_ECD",
               "BS_ECD_ELA","BS_ECD_EST","BS_ECD_HUM", "BS_ECD_MAT",
               "BS_ECD_SOS","BS_ECD_UST","MST_CHD","MS_CSD","MS_CSD_CERT",
               "MST_HEA_NCRT","BSED_HEC","BSED_HEC_CHP","BSED_HEC_WEL",
               "BS_ECI","BS_ECI_ELEI","BS_ECI_ESEI","BS_ECI_HMEI","BS_ECI_MTEI",
               "BS_ECI_SSCH","BS_ECI_SSEI","BS_IEC", "BS_IEC_ELA","BS_IEC_EST",
               "BS_IEC_HUM","BS_IEC_MAT","BS_IEC_SOS","BSED_PEM", "BSED_PEM_ADP",
               "BSED_PEM_OAE","MST_PHE", "MST_PHE_PENC","BA_ESL_CERT")

##load dplyr
library(dplyr)

#load data
eot_202390 <-read.csv("orion_SDS_202390EOT-official.csv",header=TRUE)
eot_202420 <-read.csv("sds202420eot_07162024_official.csv",header=TRUE)
eot_202410 <-read.csv("orion_202410EOT_official-withIPEDSethnicity.csv",header=TRUE)
eot_202460 <-read.csv("SDS202460eot_20240925_official.csv",header=TRUE)
csf_202390 <-read.csv("banr_csf_202390_02132024_da.csv",header=TRUE)
csf_202420 <-read.csv("banr-csf-202420_0529-EOT_official.csv",header=TRUE)
csf_202410 <-read.csv("banr_csf_202410_EOT_03082024_da.csv",header=TRUE)
csf_202460 <-read.csv("CSF202460_20240923.csv",header=TRUE)

##select only needed columns for all datasets
eot_202390 <- eot_202390[, c( "LOCAL_ID" , "SSN" , "LAST_NAME" , "FIRST_NAME", "MI", 
                              "DOB", "GENDER", "COURSE_LEVEL" , "ft_pt", "ipeds_race",
                              "HISPANIC_ORIGIN", "ETHNICITY", "HIGHER_ED_HIST", "PRIM_AWARD_LVL" ,
                             "COLLEGE" , "DEGREE" , "MAJOR" , "PROGRAM")]
eot_202420 <- eot_202420[, c( "id" , "ssn" , "last_name" , "first_name", "mi", 
                              "dob", "gender", "course_level" , "FT_PT", "ipeds_ethnicity",
                              "hispanic_origin", "ethnicity", "higher_education_history", 
                              "prim_award_lvl")]
eot_202410 <- eot_202410[, c( "id" , "ssn" , "last_name" , "first_name", "mi", 
                              "dob", "gender", "course_level" , "FT_PT", "ipeds_ethnicity",
                              "hispanic_origin", "ethnicity", "higher_education_history", 
                              "prim_award_lvl")]
eot_202460 <- eot_202460[, c( "id" , "ssn" , "last_name" , "first_name", "mi", 
                              "dob", "gender", "course_level" , "FT_PT", "IPEDS_ethnicity",
                              "hispanic_origin", "ethnicity", "higher_ed_hist", 
                              "prim_award_lvl")]
csf_202390 <- csf_202390[, c( "ID" , "Admit.Term" , "Catalog.Term" )]
csf_202420 <- csf_202420[, c( "ID" , "Admit.Term" , "Catalog.Term" , "School",
                              "Degree" , "Major", "Program")]
csf_202410 <- csf_202410[, c( "ID" , "Admit.Term" , "Catalog.Term" , "School",
                              "Degree" , "Major", "Program")]
csf_202460 <- csf_202460[, c( "ID" , "Admit.Term" , "Catalog.Term" , "School",
                              "Degree" , "Major", "Program")]

#rename id for join
eot_202390 <- eot_202390 %>% rename(id = LOCAL_ID)
csf_202390 <- csf_202390 %>% rename(id = ID)
csf_202420 <- csf_202420 %>% rename(id = ID)
csf_202410 <- csf_202410 %>% rename(id = ID)
csf_202460 <- csf_202460 %>% rename(id = ID)

#join needed csf columns
eot_202390 <- eot_202390 %>%
  left_join(csf_202390, by = "id")
eot_202420 <- eot_202420 %>%
  left_join(csf_202420, by = "id")
eot_202410 <- eot_202410 %>%
  left_join(csf_202410, by = "id")
eot_202460 <- eot_202460 %>%
  left_join(csf_202460, by = "id")

#cleanup workspace & remove CSFs
rm(csf_202390, csf_202410, csf_202420, csf_202460)

#rename  needed columns
eot_202390 <- eot_202390 %>% rename(ssn = SSN, last_name = LAST_NAME,
                                    first_name = FIRST_NAME, mi = MI, dob = DOB,
                                    gender = GENDER, ipeds_race_eth = ipeds_race,
                                    hispanic_origin = HISPANIC_ORIGIN, ethnicity = ETHNICITY,
                                    course_lvl_202390 = COURSE_LEVEL, ft_pt_202390 = ft_pt,
                                    heh_202390 = HIGHER_ED_HIST, prim_award_lvl_202390 = PRIM_AWARD_LVL,
                                    school_202390 = COLLEGE, degree_202390 = DEGREE,
                                    major_202390 = MAJOR, program_202390 = PROGRAM, 
                                    admit_term_202390 = Admit.Term, catalog_term_202390 = Catalog.Term)
eot_202420 <- eot_202420 %>% rename(ipeds_race_eth = ipeds_ethnicity,
                                    course_lvl_202420 = course_level, ft_pt_202420 = FT_PT,
                                    heh_202420 = higher_education_history, prim_award_lvl_202420 = prim_award_lvl,
                                    school_202420 = School, degree_202420 = Degree,
                                    major_202420 = Major, program_202420 = Program,
                                    admit_term_202420 = Admit.Term, catalog_term_202420 = Catalog.Term)
eot_202410 <- eot_202410 %>% rename(ipeds_race_eth = ipeds_ethnicity,
                                    course_lvl_202410 = course_level, ft_pt_202410 = FT_PT,
                                    heh_202410 = higher_education_history, prim_award_lvl_202410 = prim_award_lvl,
                                    school_202410 = School, degree_202410 = Degree,
                                    major_202410 = Major, program_202410 = Program,
                                    admit_term_202410 = Admit.Term, catalog_term_202410 = Catalog.Term)
eot_202460 <- eot_202460 %>% rename(ipeds_race_eth = IPEDS_ethnicity,
                                    course_lvl_202460 = course_level, ft_pt_202460 = FT_PT,
                                    heh_202460 = higher_ed_hist, prim_award_lvl_202460 = prim_award_lvl,
                                    school_202460 = School, degree_202460 = Degree,
                                    major_202460 = Major, program_202460 = Program,
                                    admit_term_202460 = Admit.Term, catalog_term_202460 = Catalog.Term)

#make ssn columns character columns 
eot_202390$ssn <- as.character(eot_202390$ssn)
eot_202410$ssn <- as.character(eot_202410$ssn)
eot_202420$ssn <- as.character(eot_202420$ssn)
eot_202460$ssn <- as.character(eot_202460$ssn)

#make other columns character columns 
eot_202390$hispanic_origin <- as.character(eot_202390$hispanic_origin)
eot_202410$hispanic_origin <- as.character(eot_202410$hispanic_origin)
eot_202420$hispanic_origin <- as.character(eot_202420$hispanic_origin)
eot_202460$hispanic_origin <- as.character(eot_202460$hispanic_origin)

eot_202390$ethnicity <- as.character(eot_202390$ethnicity)
eot_202410$ethnicity <- as.character(eot_202410$ethnicity)
eot_202420$ethnicity <- as.character(eot_202420$ethnicity)
eot_202460$ethnicity <- as.character(eot_202460$ethnicity)

#convert DOB to correct date format mm/dd/yy
eot_202390$dob <- sprintf("%08d", as.numeric(eot_202390$dob))
eot_202390$dob <- as.Date(eot_202390$dob, format = "%m%d%Y")
eot_202390$dob <- format(eot_202390$dob, "%m/%d/%y")

eot_202410$dob <- sprintf("%08d", as.numeric(eot_202410$dob))
eot_202410$dob <- as.Date(eot_202410$dob, format = "%m%d%Y")
eot_202410$dob <- format(eot_202410$dob, "%m/%d/%y")

eot_202420$dob <- sprintf("%08d", as.numeric(eot_202420$dob))
eot_202420$dob <- as.Date(eot_202420$dob, format = "%m%d%Y")
eot_202420$dob <- format(eot_202420$dob, "%m/%d/%y")

eot_202460$dob <- sprintf("%08d", as.numeric(eot_202460$dob))
eot_202460$dob <- as.Date(eot_202460$dob, format = "%m%d%Y")
eot_202460$dob <- format(eot_202460$dob, "%m/%d/%y")

#full join
df <- eot_202390 %>%
  full_join(eot_202410, by = "id") %>%
  full_join(eot_202420, by = "id") %>%
  full_join(eot_202460, by = "id") 

#fill and combine duplicate columns
df <- df %>%
  mutate(
    first_name = coalesce(
      na_if(first_name.y.y, ""),
      na_if(first_name.x.x, ""),
      na_if(first_name.y, ""),
      na_if(first_name.x, "")
    )
  )

df <- df %>%
  mutate(
    last_name = coalesce(
      na_if(last_name.y.y, ""),
      na_if(last_name.x.x, ""),
      na_if(last_name.y, ""),
      na_if(last_name.x, "")
    )
  )

df <- df %>%
  mutate(
    mi = coalesce(
      na_if(mi.y.y, ""),
      na_if(mi.x.x, ""),
      na_if(mi.y, ""),
      na_if(mi.x, "")
    )
  )

df <- df %>%
  mutate(
    dob = coalesce(
      na_if(dob.y.y, ""),
      na_if(dob.x.x, ""),
      na_if(dob.y, ""),
      na_if(dob.x, "")
    )
  )

df <- df %>%
  mutate(
    ssn = coalesce(
      na_if(ssn.y.y, ""),
      na_if(ssn.x.x, ""),
      na_if(ssn.y, ""),
      na_if(ssn.x, "")
    )
  )

df <- df %>%
  mutate(
    hispanic_origin = coalesce(
      na_if(hispanic_origin.y.y, ""),
      na_if(hispanic_origin.x.x, ""),
      na_if(hispanic_origin.y, ""),
      na_if(hispanic_origin.x, "")
    )
  )

df <- df %>%
  mutate(
    ethnicity = coalesce(
      na_if(ethnicity.y.y, ""),
      na_if(ethnicity.x.x, ""),
      na_if(ethnicity.y, ""),
      na_if(ethnicity.x, "")
    )
  )

df <- df %>%
  mutate(
    ipeds_race_eth = coalesce(
      na_if(ipeds_race_eth.y.y, ""),
      na_if(ipeds_race_eth.x.x, ""),
      na_if(ipeds_race_eth.y, ""),
      na_if(ipeds_race_eth.x, "")
    )
  )

df <- df %>%
  mutate(
    gender = coalesce(
      na_if(gender.y.y, ""),
      na_if(gender.x.x, ""),
      na_if(gender.y, ""),
      na_if(gender.x, "")
    )
  )

#remove duplicate columns
df <-df %>% 
  select(-ends_with(".x"), -ends_with(".y"), -ends_with(".x.x"), -ends_with(".y.y"))

#reorder columns
df <- df[, c( "id" , "ssn" , "last_name", "first_name", "mi", "dob", "gender",
              "ipeds_race_eth", "hispanic_origin", "ethnicity", "course_lvl_202390",
              "ft_pt_202390", "heh_202390", "prim_award_lvl_202390", "school_202390",
              "degree_202390", "major_202390", "program_202390", "admit_term_202390",
              "catalog_term_202390", "course_lvl_202410",
              "ft_pt_202410", "heh_202410", "prim_award_lvl_202410", "school_202410",
              "degree_202410", "major_202410", "program_202410", "admit_term_202410",
              "catalog_term_202410", "course_lvl_202420",
              "ft_pt_202420", "heh_202420", "prim_award_lvl_202420", "school_202420",
              "degree_202420", "major_202420", "program_202420", "admit_term_202420",
              "catalog_term_202420",  "course_lvl_202460",
              "ft_pt_202460", "heh_202460", "prim_award_lvl_202460", "school_202460",
              "degree_202460", "major_202460", "program_202460", "admit_term_202460",
              "catalog_term_202460")]

#write to excel to check
library(writexl)
write_xlsx(df, "step_1_eot_csf_all_terms_all_students.xlsx")

#cleanup workspace & remove old things
rm(eot_202390, eot_202410, eot_202420, eot_202460)

#label as TED or not
df <- df %>%  
  mutate(TED_202390 =  case_when( 
    is.na(program_202390) | program_202390 == ""  ~ NA_character_ , 
    program_202390 %in% TED_codes ~ "TED", 
    TRUE ~ "NOT"
  ))
df <- df %>%  
  mutate(TED_202410 =  case_when( 
    is.na(program_202410) | program_202410 == ""  ~ NA_character_ , 
    program_202410 %in% TED_codes ~ "TED", 
    TRUE ~ "NOT"
  ))
df <- df %>%  
  mutate(TED_202420 =  case_when( 
    is.na(program_202420) | program_202420 == ""  ~ NA_character_ , 
    
    program_202420 %in% TED_codes ~ "TED", 
    TRUE ~ "NOT"
  ))
df <- df %>%  
  mutate(TED_202460 =  case_when( 
    is.na(program_202460) | program_202460 == ""  ~ NA_character_ , 
    program_202460 %in% TED_codes ~ "TED", 
    TRUE ~ "NOT"
  ))

#write to excel to check
library(writexl)
write_xlsx(df, "step_2_programs_labeled_TED_all_terms_all_Students.xlsx")

##create a column to check for course lvl changes
df <- df %>%
  rowwise() %>%
  mutate(
    course_lvl_change = {
      levels <- c(course_lvl_202390, course_lvl_202410, course_lvl_202420, course_lvl_202460)
      levels_clean <- na.omit(levels[levels != ""])
      if (length(unique(levels_clean)) == 1) {
        "no course lvl change"
      } else {
        change_year <- c("202390", "202410", "202420", "202460")[which(levels_clean != levels_clean[1])[1]]
        change_year
      }
    }
  ) %>%
  ungroup()

#write to excel to check
library(writexl)
write_xlsx(df, "step_3_flag_for_course_level_changes_added.xlsx")

##create a column to tag if they ended the year in a TED major
df <- df %>%  
  mutate(TED_year_end =  case_when( 
    TED_202460 == "TED"  ~ "yes" , 
    is.na(TED_202460) & TED_202420 == "TED" ~ "yes", 
    TED_202460 == "" & TED_202420 == "TED" ~ "yes",
    is.na(TED_202460) & is.na(TED_202420) & TED_202410 == "TED" ~ "yes", 
    TED_202460 == "" & TED_202420 == "" & TED_202410 == "TED" ~ "yes",
    is.na(TED_202460) & is.na(TED_202420) & is.na(TED_202410) & TED_202390 == "TED" ~ "yes",
    TED_202460 == "" & TED_202420 == "" & TED_202410 == "" & TED_202390 == "TED" ~ "yes",
    TED_202460 == "TED" | TED_202420 == "TED" | TED_202410 == "TED" | TED_202390 == "TED"  ~ "check",
    TRUE ~ "NOT"
  ))

##remove non-TED
df <- subset(df, df$TED_year_end != "NOT")

#write to excel to check
library(writexl)
write_xlsx(df, "step_4_flag_for_last_semester_TED_major_remove_never_TED.xlsx")

##load DADs/DCL data
#need TED completers between 9/1/23 & 8/31/24
#load data
dcl_23_24 <- read.csv("Degree_Completer_Listing_20231001-20240630.csv",header=TRUE)
dcl_24 <- read.csv("banner_degree_list_20240701_20240930_20241113.csv",header=TRUE)

##Join Degree Completers
dcl <- dcl_23_24 %>%
  full_join(dcl_24)

#cleanup workspace & remove old things
rm(dcl_23_24, dcl_24)

#Remove Students who Didn't Graduate
dcl <- subset(dcl, dcl$DEGS_CODE == "UA" | dcl$DEGS_CODE == "GA")

##Selecting Columns for DCL
dcl <- dcl[, c( "ID" , "GRAD_DATE" , "PROGRAM" , "DEGC_CODE","COLL_CODE_1", 
                "MAJR_CODE_1" , "DEGS_CODE")]

##Remove Non-TED Degrees
dcl <- subset(dcl, dcl$PROGRAM %in% TED_codes)

#rename id for join
dcl <- dcl %>% rename(id = ID)

#Join DCL to df
df <- df %>%
  full_join(dcl, by = "id")

#cleanup workspace & remove old things
rm(dcl)

#Make Column to Mark Graduates
df <- df %>%
  mutate(GRAD_STATUS =
           if_else(is.na(GRAD_DATE), "NOT",
                   "GRADUATED"))

#write to excel to check
library(writexl)
write_xlsx(df, "step_5_add_completer_info.xlsx")

##code for initial cert
initial_cert_codes <- c("BA_SST","BA_SST_ANT","BA_SST_ECO","BA_SST_GRY","BA_SST_HIS",
                        "BA_SST_POL","BA_SST_SOC","BS_ACM","BS_AES","BA_AFS","MAT_ACH",
                        "BS_ABI","MAT_ABI","BA_AEN","MAT_AEN","BA_AFR","BA_AEM",
                        "BS_AEM","BS_APH","MAT_APH","BS_APM", "BA_ASP","BS_ECD",
                        "BS_ECD_ELA","BS_ECD_EST","BS_ECD_HUM", "BS_ECD_MAT",
                        "BS_ECD_SOS","BS_ECD_UST","MST_CHD","MS_CSD","MS_CSD_CERT",
                        "MST_HEA_NCRT","BSED_HEC","BSED_HEC_CHP","BSED_HEC_WEL",
                        "BS_ECI","BS_ECI_ELEI","BS_ECI_ESEI","BS_ECI_HMEI","BS_ECI_MTEI",
                        "BS_ECI_SSCH","BS_ECI_SSEI","BS_IEC", "BS_IEC_ELA","BS_IEC_EST",
                        "BS_IEC_HUM","BS_IEC_MAT","BS_IEC_SOS","BSED_PEM", "BSED_PEM_ADP",
                        "BSED_PEM_OAE","MST_PHE", "MST_PHE_PENC","BA_ESL_CERT")

#label as initial cert or not
df <- df %>%  
  mutate(initial_cert =  case_when( 
    program_202460 %in% initial_cert_codes  ~ "yes" , 
    is.na(program_202460) & program_202420 %in% initial_cert_codes ~ "yes", 
    program_202460 == "" & program_202420 %in% initial_cert_codes ~ "yes",
    is.na(program_202460) & is.na(program_202420) & program_202410 %in% initial_cert_codes ~ "yes", 
    program_202460 == "" & program_202420 == "" & program_202410 %in% initial_cert_codes ~ "yes",
    is.na(program_202460) & is.na(program_202420) & is.na(program_202410) & program_202390 %in% initial_cert_codes ~ "yes",
    program_202460 == "" & program_202420 == "" & program_202410 == "" & program_202390 %in% initial_cert_codes ~ "yes",
    PROGRAM %in% initial_cert_codes  ~ "yes" ,
    TRUE ~ "NOT"
  ))

#write to excel to check
library(writexl)
write_xlsx(df, "step_6_add_flag_for_initial_certs.xlsx")

#re-load load data after any manual cleaning at this point if needed
df <-read.csv("step_6_add_flag_for_initial_certs.csv",header=TRUE)

##subset only title ii cohort
df <- subset(df, df$initial_cert == "yes")

##check if anyone who was only in the fall & did not complete
fallonly <- subset(df, !is.na(df$ft_pt_202390)  & is.na(df$ft_pt_202420)  & is.na(df$ft_pt_202460) & df$GRAD_STATUS =="NOT")

#remove people who were only in the fall & did not complete 
df <- anti_join(df, fallonly, by = "id")


#write to excel to check
library(writexl)
write_xlsx(df, "step_7_remove_fall_only_non_completers.xlsx")

##clean up workspace
rm(fallonly)

##columns needed for final worksheet:
## ssn (last 5 digits), last name, first name, mi, DOB (mm/dd/yy)
##program type, reporting group, code 1, cip 1, degree 1 (& 2 & 3)
##years to degree, enrollment status, program level, gender, ethnicity, race, program code

##create column for ssn to last 5 characters
df$ssn5 <- substr(df$ssn, nchar(df$ssn) - 4, nchar(df$ssn))

##create program type = T for everyone
df$program_type <- "T"

##create reporting group column that codes 2 = other enrolled, 3 = completers
df <- df %>%
  mutate(reporting_group =
           case_when(
             GRAD_STATUS == "NOT" ~ "2",
             GRAD_STATUS == "GRADUATED" ~ "3",
             TRUE ~ ""
           ))

##create new column to use for program
#program_new
df <- df %>%
  mutate(program_new =
           case_when(
             GRAD_STATUS == "NOT" & !is.na(df$program_202460) ~ df$program_202460,
             GRAD_STATUS == "NOT" & is.na(df$program_202460) ~ df$program_202420,
             GRAD_STATUS == "NOT" & df$program_202460 == "" ~ df$program_202420,
             GRAD_STATUS == "GRADUATED" ~ df$PROGRAM,
             TRUE ~ ""
           ))

##create new column to use for relevant course level
#course_level_new
df <- df %>%
  mutate(course_level_new =
           case_when(
               substr(program_new, 1, 1) == "B" ~ "UG",
              substr(program_new, 1, 1) == "M" ~ "GR",
             TRUE ~ ""
           ))

#write to excel to check
#library(writexl)
#write_xlsx(df, "check_program_and_course_level_to_use.xlsx")

##CIP codes etc section
##code programs to code 1 & 2 
df <- df %>%
  mutate(code_1 =  
         case_when(
  df$PROGRAM == "BA_SST" ~ "5110",
  df$PROGRAM == "BA_SST_ANT" ~ "5110",
  df$PROGRAM == "BA_SST_ECO" ~ "5110",
  df$PROGRAM == "BA_SST_GRY" ~ "5110",
  df$PROGRAM == "BA_SST_HIS" ~ "5110",
  df$PROGRAM == "BA_SST_POL" ~ "5110",
  df$PROGRAM == "BA_SST_SOC" ~ "5110",
  df$PROGRAM == "BS_ACM" ~ "5030",
  df$PROGRAM == "BS_AES" ~ "5070",
  df$PROGRAM == "BA_AFS" ~ "5140",
  df$PROGRAM == "MAT_ACH" ~ "5030",
  df$PROGRAM == "BS_ABI" ~ "5010",
  df$PROGRAM == "MAT_ABI" ~ "5010",
  df$PROGRAM == "BA_AEN" ~ "5013",
  df$PROGRAM == "MAT_AEN" ~ "5013",
  df$PROGRAM == "BA_AFR" ~ "5140",
  df$PROGRAM == "BA_AEM" ~ "5130",
  df$PROGRAM == "BS_AEM" ~ "5130",
  df$PROGRAM == "BS_APH" ~ "5050",
  df$PROGRAM == "MAT_APH" ~ "5050",  
  df$PROGRAM == "BS_APM" ~ "5050",
  df$PROGRAM == "BA_ASP" ~ "5150",
  df$PROGRAM == "BS_ECD" ~ "3013",
  df$PROGRAM == "BS_ECD_ELA" ~ "3013",
  df$PROGRAM == "BS_ECD_EST" ~ "3013",
  df$PROGRAM == "BS_ECD_HUM" ~ "3013",
  df$PROGRAM == "BS_ECD_MAT" ~ "3013",
  df$PROGRAM == "BS_ECD_SOS" ~ "3013",
  df$PROGRAM == "BS_ECD_UST" ~ "3013",
  df$PROGRAM == "MST_CHD" ~ "3014",
  df$PROGRAM == "MS_CSD" ~ "9021",
  df$PROGRAM == "MS_CSD_CERT" ~ "9021",
  df$PROGRAM == "MST_HEA_NCRT" ~ "6121",
  df$PROGRAM == "BSED_HEC" ~ "6121",
  df$PROGRAM == "BSED_HEC_CHP" ~ "6121",
  df$PROGRAM == "BSED_HEC_WEL" ~ "6121",
  df$PROGRAM == "BS_ECI" ~ "3013",
  df$PROGRAM == "BS_ECI_ELEI" ~ "3013",
  df$PROGRAM == "BS_ECI_ESEI" ~ "3013",
  df$PROGRAM == "BS_ECI_HMEI" ~ "3013",
  df$PROGRAM == "BS_ECI_MTEI" ~ "3013",
  df$PROGRAM == "BS_ECI_SSCH" ~ "3013",
  df$PROGRAM == "BS_ECI_SSEI" ~ "3013",
  df$PROGRAM == "BS_IEC" ~ "9014",
  df$PROGRAM == "BS_IEC_ELA" ~ "9014",
  df$PROGRAM == "BS_IEC_EST" ~ "9014",
  df$PROGRAM == "BS_IEC_HUM" ~ "9014",
  df$PROGRAM == "BS_IEC_MAT" ~ "9014",
  df$PROGRAM == "BS_IEC_SOS" ~ "9014",
  df$PROGRAM == "BSED_PEM" ~ "6160",
  df$PROGRAM == "BSED_PEM_ADP" ~ "6160",
  df$PROGRAM == "BSED_PEM_OAE" ~ "6160",
  df$PROGRAM == "MST_PHE" ~ "6160",
  df$PROGRAM == "MST_PHE_PENC" ~ "6160",
  df$PROGRAM == "BA_ESL_CERT" ~ "7080",
  df$program_new == "BA_SST" ~ "5110",
  df$program_new == "BA_SST_ANT" ~ "5110",
  df$program_new == "BA_SST_ECO" ~ "5110",
  df$program_new == "BA_SST_GRY" ~ "5110",
  df$program_new == "BA_SST_HIS" ~ "5110",
  df$program_new == "BA_SST_POL" ~ "5110",
  df$program_new == "BA_SST_SOC" ~ "5110",
  df$program_new == "BS_ACM" ~ "5030",
  df$program_new == "BS_AES" ~ "5070",
  df$program_new == "BA_AFS" ~ "5140",
  df$program_new == "MAT_ACH" ~ "5030",
  df$program_new == "BS_ABI" ~ "5010",
  df$program_new == "MAT_ABI" ~ "5010",
  df$program_new == "BA_AEN" ~ "5013",
  df$program_new == "MAT_AEN" ~ "5013",
  df$program_new == "BA_AFR" ~ "5140",
  df$program_new == "BA_AEM" ~ "5130",
  df$program_new == "BS_AEM" ~ "5130",
  df$program_new == "BS_APH" ~ "5050",
  df$program_new == "MAT_APH" ~ "5050",  
  df$program_new == "BS_APM" ~ "5050",
  df$program_new == "BA_ASP" ~ "5150",
  df$program_new == "BS_ECD" ~ "3013",
  df$program_new == "BS_ECD_ELA" ~ "3013",
  df$program_new == "BS_ECD_EST" ~ "3013",
  df$program_new == "BS_ECD_HUM" ~ "3013",
  df$program_new == "BS_ECD_MAT" ~ "3013",
  df$program_new == "BS_ECD_SOS" ~ "3013",
  df$program_new == "BS_ECD_UST" ~ "3013",
  df$program_new == "MST_CHD" ~ "3014",
  df$program_new == "MS_CSD" ~ "9021",
  df$program_new == "MS_CSD_CERT" ~ "9021",
  df$program_new == "MST_HEA_NCRT" ~ "6121",
  df$program_new == "BSED_HEC" ~ "6121",
  df$program_new == "BSED_HEC_CHP" ~ "6121",
  df$program_new == "BSED_HEC_WEL" ~ "6121",
  df$program_new == "BS_ECI" ~ "3013",
  df$program_new == "BS_ECI_ELEI" ~ "3013",
  df$program_new == "BS_ECI_ESEI" ~ "3013",
  df$program_new == "BS_ECI_HMEI" ~ "3013",
  df$program_new == "BS_ECI_MTEI" ~ "3013",
  df$program_new == "BS_ECI_SSCH" ~ "3013",
  df$program_new == "BS_ECI_SSEI" ~ "3013",
  df$program_new == "BS_IEC" ~ "9014",
  df$program_new == "BS_IEC_ELA" ~ "9014",
  df$program_new == "BS_IEC_EST" ~ "9014",
  df$program_new == "BS_IEC_HUM" ~ "9014",
  df$program_new == "BS_IEC_MAT" ~ "9014",
  df$program_new == "BS_IEC_SOS" ~ "9014",
  df$program_new == "BSED_PEM" ~ "6160",
  df$program_new == "BSED_PEM_ADP" ~ "6160",
  df$program_new == "BSED_PEM_OAE" ~ "6160",
  df$program_new == "MST_PHE" ~ "6160",
  df$program_new == "MST_PHE_PENC" ~ "6160",
  df$program_new == "BA_ESL_CERT" ~ "7080",
  TRUE ~ ""
))

df <- df %>%
  mutate(code_2 =  case_when(
  df$PROGRAM == "BA_AFS" ~ "5150",
  df$PROGRAM == "BS_APM" ~ "5130",
  df$PROGRAM == "BS_ECD" ~ "3014",
  df$PROGRAM == "BS_ECD_ELA" ~ "3014",
  df$PROGRAM == "BS_ECD_EST" ~ "3014",
  df$PROGRAM == "BS_ECD_HUM" ~ "3014",
  df$PROGRAM == "BS_ECD_MAT" ~ "3014",
  df$PROGRAM == "BS_ECD_SOS" ~ "3014",
  df$PROGRAM == "BS_ECD_UST" ~ "3014",
  df$PROGRAM == "BS_ECI" ~ "0126",
  df$PROGRAM == "BS_ECI_ELEI" ~ "0126",
  df$PROGRAM == "BS_ECI_ESEI" ~ "0126",
  df$PROGRAM == "BS_ECI_HMEI" ~ "0126",
  df$PROGRAM == "BS_ECI_MTEI" ~ "0126",
  df$PROGRAM == "BS_ECI_SSCH" ~ "0126",
  df$PROGRAM == "BS_ECI_SSEI" ~ "0126",
  df$PROGRAM == "BS_IEC" ~ "3014",
  df$PROGRAM == "BS_IEC_ELA" ~ "3014",
  df$PROGRAM == "BS_IEC_EST" ~ "3014",
  df$PROGRAM == "BS_IEC_HUM" ~ "3014",
  df$PROGRAM == "BS_IEC_MAT" ~ "3014",
  df$PROGRAM == "BS_IEC_SOS" ~ "3014",
  df$program_new == "BA_AFS" ~ "5150",
  df$program_new == "BS_APM" ~ "5130",
  df$program_new == "BS_ECD" ~ "3014",
  df$program_new == "BS_ECD_ELA" ~ "3014",
  df$program_new == "BS_ECD_EST" ~ "3014",
  df$program_new == "BS_ECD_HUM" ~ "3014",
  df$program_new == "BS_ECD_MAT" ~ "3014",
  df$program_new == "BS_ECD_SOS" ~ "3014",
  df$program_new == "BS_ECD_UST" ~ "3014",
  df$program_new == "BS_ECI" ~ "0126",
  df$program_new == "BS_ECI_ELEI" ~ "0126",
  df$program_new == "BS_ECI_ESEI" ~ "0126",
  df$program_new == "BS_ECI_HMEI" ~ "0126",
  df$program_new == "BS_ECI_MTEI" ~ "0126",
  df$program_new == "BS_ECI_SSCH" ~ "0126",
  df$program_new == "BS_ECI_SSEI" ~ "0126",
  df$program_new == "BS_IEC" ~ "3014",
  df$program_new == "BS_IEC_ELA" ~ "3014",
  df$program_new == "BS_IEC_EST" ~ "3014",
  df$program_new == "BS_IEC_HUM" ~ "3014",
  df$program_new == "BS_IEC_MAT" ~ "3014",
  df$program_new == "BS_IEC_SOS" ~ "3014",
  TRUE ~ ""
))

##Code Programs to cip codes 1 & 2 
df <- df %>%
  mutate(cip_code_1 =  case_when(
  df$PROGRAM == "BA_SST" ~ "13.1318",
  df$PROGRAM == "BA_SST_ANT" ~ "13.1318",
  df$PROGRAM == "BA_SST_ECO" ~ "13.1318",
  df$PROGRAM == "BA_SST_GRY" ~ "13.1318",
  df$PROGRAM == "BA_SST_HIS" ~ "13.1318",
  df$PROGRAM == "BA_SST_POL" ~ "13.1318",
  df$PROGRAM == "BA_SST_SOC" ~ "13.1318",
  df$PROGRAM == "BS_ACM" ~ "13.1323",
  df$PROGRAM == "BS_AES" ~ "13.1337",
  df$PROGRAM == "BA_AFS" ~ "13.1306",
  df$PROGRAM == "MAT_ACH" ~ "13.1323",
  df$PROGRAM == "BS_ABI" ~ "13.1322",
  df$PROGRAM == "MAT_ABI" ~ "13.1322",
  df$PROGRAM == "BA_AEN" ~ "13.1305",
  df$PROGRAM == "MAT_AEN" ~ "13.1305",
  df$PROGRAM == "BA_AFR" ~ "13.1306",
  df$PROGRAM == "BA_AEM" ~ "13.1311",
  df$PROGRAM == "BS_AEM" ~ "13.1311",
  df$PROGRAM == "BS_APH" ~ "13.1329",
  df$PROGRAM == "MAT_APH" ~ "13.1329",  
  df$PROGRAM == "BS_APM" ~ "13.1329",
  df$PROGRAM == "BA_ASP" ~ "13.1306",
  df$PROGRAM == "BS_ECD" ~ "13.121",
  df$PROGRAM == "BS_ECD_ELA" ~ "13.121",
  df$PROGRAM == "BS_ECD_EST" ~ "13.121",
  df$PROGRAM == "BS_ECD_HUM" ~ "13.121",
  df$PROGRAM == "BS_ECD_MAT" ~ "13.121",
  df$PROGRAM == "BS_ECD_SOS" ~ "13.121",
  df$PROGRAM == "BS_ECD_UST" ~ "13.121",
  df$PROGRAM == "MST_CHD" ~ "13.1202",
  df$PROGRAM == "MS_CSD" ~ "13.1331",
  df$PROGRAM == "MS_CSD_CERT" ~ "13.1331",
  df$PROGRAM == "MST_HEA_NCRT" ~ "13.1307",
  df$PROGRAM == "BSED_HEC" ~ "13.1307",
  df$PROGRAM == "BSED_HEC_CHP" ~ "13.1307",
  df$PROGRAM == "BSED_HEC_WEL" ~ "13.1307",
  df$PROGRAM == "BS_ECI" ~ "13.121",
  df$PROGRAM == "BS_ECI_ELEI" ~ "13.121",
  df$PROGRAM == "BS_ECI_ESEI" ~ "13.121",
  df$PROGRAM == "BS_ECI_HMEI" ~ "13.121",
  df$PROGRAM == "BS_ECI_MTEI" ~ "13.121",
  df$PROGRAM == "BS_ECI_SSCH" ~ "13.121",
  df$PROGRAM == "BS_ECI_SSEI" ~ "13.121",
  df$PROGRAM == "BS_IEC" ~ "13.1",
  df$PROGRAM == "BS_IEC_ELA" ~ "13.1",
  df$PROGRAM == "BS_IEC_EST" ~ "13.1",
  df$PROGRAM == "BS_IEC_HUM" ~ "13.1",
  df$PROGRAM == "BS_IEC_MAT" ~ "13.1",
  df$PROGRAM == "BS_IEC_SOS" ~ "13.1",
  df$PROGRAM == "BSED_PEM" ~ "13.1314",
  df$PROGRAM == "BSED_PEM_ADP" ~ "13.1314",
  df$PROGRAM == "BSED_PEM_OAE" ~ "13.1314",
  df$PROGRAM == "MST_PHE" ~ "13.1314",
  df$PROGRAM == "MST_PHE_PENC" ~ "13.1314",
  df$PROGRAM == "BA_ESL_CERT" ~ "13.14",
  df$program_new == "BA_SST" ~ "13.1318",
  df$program_new == "BA_SST_ANT" ~ "13.1318",
  df$program_new == "BA_SST_ECO" ~ "13.1318",
  df$program_new == "BA_SST_GRY" ~ "13.1318",
  df$program_new == "BA_SST_HIS" ~ "13.1318",
  df$program_new == "BA_SST_POL" ~ "13.1318",
  df$program_new == "BA_SST_SOC" ~ "13.1318",
  df$program_new == "BS_ACM" ~ "13.1323",
  df$program_new == "BS_AES" ~ "13.1337",
  df$program_new == "BA_AFS" ~ "13.1306",
  df$program_new == "MAT_ACH" ~ "13.1323",
  df$program_new == "BS_ABI" ~ "13.1322",
  df$program_new == "MAT_ABI" ~ "13.1322",
  df$program_new == "BA_AEN" ~ "13.1305",
  df$program_new == "MAT_AEN" ~ "13.1305",
  df$program_new == "BA_AFR" ~ "13.1306",
  df$program_new == "BA_AEM" ~ "13.1311",
  df$program_new == "BS_AEM" ~ "13.1311",
  df$program_new == "BS_APH" ~ "13.1329",
  df$program_new == "MAT_APH" ~ "13.1329",  
  df$program_new == "BS_APM" ~ "13.1329",
  df$program_new == "BA_ASP" ~ "13.1306",
  df$program_new == "BS_ECD" ~ "13.121",
  df$program_new == "BS_ECD_ELA" ~ "13.121",
  df$program_new == "BS_ECD_EST" ~ "13.121",
  df$program_new == "BS_ECD_HUM" ~ "13.121",
  df$program_new == "BS_ECD_MAT" ~ "13.121",
  df$program_new == "BS_ECD_SOS" ~ "13.121",
  df$program_new == "BS_ECD_UST" ~ "13.121",
  df$program_new == "MST_CHD" ~ "13.1202",
  df$program_new == "MS_CSD" ~ "13.1331",
  df$program_new == "MS_CSD_CERT" ~ "13.1331",
  df$program_new == "MST_HEA_NCRT" ~ "13.1307",
  df$program_new == "BSED_HEC" ~ "13.1307",
  df$program_new == "BSED_HEC_CHP" ~ "13.1307",
  df$program_new == "BSED_HEC_WEL" ~ "13.1307",
  df$program_new == "BS_ECI" ~ "13.121",
  df$program_new == "BS_ECI_ELEI" ~ "13.121",
  df$program_new == "BS_ECI_ESEI" ~ "13.121",
  df$program_new == "BS_ECI_HMEI" ~ "13.121",
  df$program_new == "BS_ECI_MTEI" ~ "13.121",
  df$program_new == "BS_ECI_SSCH" ~ "13.121",
  df$program_new == "BS_ECI_SSEI" ~ "13.121",
  df$program_new == "BS_IEC" ~ "13.1",
  df$program_new == "BS_IEC_ELA" ~ "13.1",
  df$program_new == "BS_IEC_EST" ~ "13.1",
  df$program_new == "BS_IEC_HUM" ~ "13.1",
  df$program_new == "BS_IEC_MAT" ~ "13.1",
  df$program_new == "BS_IEC_SOS" ~ "13.1",
  df$program_new == "BSED_PEM" ~ "13.1314",
  df$program_new == "BSED_PEM_ADP" ~ "13.1314",
  df$program_new == "BSED_PEM_OAE" ~ "13.1314",
  df$program_new == "MST_PHE" ~ "13.1314",
  df$program_new == "MST_PHE_PENC" ~ "13.1314",
  df$program_new == "BA_ESL_CERT" ~ "13.14",
  TRUE ~ ""
))

df <- df %>%
  mutate(cip_code_2 =  case_when(
  df$PROGRAM == "BA_AFS" ~ "13.1306",
  df$PROGRAM == "BS_APM" ~ "13.1311",
  df$PROGRAM == "BS_ECD" ~ "13.1202",
  df$PROGRAM == "BS_ECD_ELA" ~ "13.1202",
  df$PROGRAM == "BS_ECD_EST" ~ "13.1202",
  df$PROGRAM == "BS_ECD_HUM" ~ "13.1202",
  df$PROGRAM == "BS_ECD_MAT" ~ "13.1202",
  df$PROGRAM == "BS_ECD_SOS" ~ "13.1202",
  df$PROGRAM == "BS_ECD_UST" ~ "13.1202",
  df$PROGRAM == "BS_ECI" ~ "13.1",
  df$PROGRAM == "BS_ECI_ELEI" ~ "13.1",
  df$PROGRAM == "BS_ECI_ESEI" ~ "13.1",
  df$PROGRAM == "BS_ECI_HMEI" ~ "13.1",
  df$PROGRAM == "BS_ECI_MTEI" ~ "13.1",
  df$PROGRAM == "BS_ECI_SSCH" ~ "13.1",
  df$PROGRAM == "BS_ECI_SSEI" ~ "13.1",
  df$PROGRAM == "BS_IEC" ~ "13.1202",
  df$PROGRAM == "BS_IEC_ELA" ~ "13.1202",
  df$PROGRAM == "BS_IEC_EST" ~ "13.1202",
  df$PROGRAM == "BS_IEC_HUM" ~ "13.1202",
  df$PROGRAM == "BS_IEC_MAT" ~ "13.1202",
  df$PROGRAM == "BS_IEC_SOS" ~ "13.1202",
  df$program_new == "BA_AFS" ~ "13.1306",
  df$program_new == "BS_APM" ~ "13.1311",
  df$program_new == "BS_ECD" ~ "13.1202",
  df$program_new == "BS_ECD_ELA" ~ "13.1202",
  df$program_new == "BS_ECD_EST" ~ "13.1202",
  df$program_new == "BS_ECD_HUM" ~ "13.1202",
  df$program_new == "BS_ECD_MAT" ~ "13.1202",
  df$program_new == "BS_ECD_SOS" ~ "13.1202",
  df$program_new == "BS_ECD_UST" ~ "13.1202",
  df$program_new == "BS_ECI" ~ "13.1",
  df$program_new == "BS_ECI_ELEI" ~ "13.1",
  df$program_new == "BS_ECI_ESEI" ~ "13.1",
  df$program_new == "BS_ECI_HMEI" ~ "13.1",
  df$program_new == "BS_ECI_MTEI" ~ "13.1",
  df$program_new == "BS_ECI_SSCH" ~ "13.1",
  df$program_new == "BS_ECI_SSEI" ~ "13.1",
  df$program_new == "BS_IEC" ~ "13.1202",
  df$program_new == "BS_IEC_ELA" ~ "13.1202",
  df$program_new == "BS_IEC_EST" ~ "13.1202",
  df$program_new == "BS_IEC_HUM" ~ "13.1202",
  df$program_new == "BS_IEC_MAT" ~ "13.1202",
  df$program_new == "BS_IEC_SOS" ~ "13.1202",
  TRUE ~ ""
))

##code programs to degree 1 & 2 
df <- df %>%
  mutate(degree_new_1 =  case_when(
  df$PROGRAM == "BA_SST" ~ "B",
  df$PROGRAM == "BA_SST_ANT" ~ "B",
  df$PROGRAM == "BA_SST_ECO" ~ "B",
  df$PROGRAM == "BA_SST_GRY" ~ "B",
  df$PROGRAM == "BA_SST_HIS" ~ "B",
  df$PROGRAM == "BA_SST_POL" ~ "B",
  df$PROGRAM == "BA_SST_SOC" ~ "B",
  df$PROGRAM == "BS_ACM" ~ "B",
  df$PROGRAM == "BS_AES" ~ "B",
  df$PROGRAM == "BA_AFS" ~ "B",
  df$PROGRAM == "MAT_ACH" ~ "M",
  df$PROGRAM == "BS_ABI" ~ "B",
  df$PROGRAM == "MAT_ABI" ~ "M",
  df$PROGRAM == "BA_AEN" ~ "B",
  df$PROGRAM == "MAT_AEN" ~ "M",
  df$PROGRAM == "BA_AFR" ~ "B",
  df$PROGRAM == "BA_AEM" ~ "B",
  df$PROGRAM == "BS_AEM" ~ "B",
  df$PROGRAM == "BS_APH" ~ "B",
  df$PROGRAM == "MAT_APH" ~ "M",  
  df$PROGRAM == "BS_APM" ~ "B",
  df$PROGRAM == "BA_ASP" ~ "B",
  df$PROGRAM == "BS_ECD" ~ "B",
  df$PROGRAM == "BS_ECD_ELA" ~ "B",
  df$PROGRAM == "BS_ECD_EST" ~ "B",
  df$PROGRAM == "BS_ECD_HUM" ~ "B",
  df$PROGRAM == "BS_ECD_MAT" ~ "B",
  df$PROGRAM == "BS_ECD_SOS" ~ "B",
  df$PROGRAM == "BS_ECD_UST" ~ "B",
  df$PROGRAM == "MST_CHD" ~ "M",
  df$PROGRAM == "MS_CSD" ~ "M",
  df$PROGRAM == "MS_CSD_CERT" ~ "M",
  df$PROGRAM == "MST_HEA_NCRT" ~ "M",
  df$PROGRAM == "BSED_HEC" ~ "B",
  df$PROGRAM == "BSED_HEC_CHP" ~ "B",
  df$PROGRAM == "BSED_HEC_WEL" ~ "B",
  df$PROGRAM == "BS_ECI" ~ "B",
  df$PROGRAM == "BS_ECI_ELEI" ~ "B",
  df$PROGRAM == "BS_ECI_ESEI" ~ "B",
  df$PROGRAM == "BS_ECI_HMEI" ~ "B",
  df$PROGRAM == "BS_ECI_MTEI" ~ "B",
  df$PROGRAM == "BS_ECI_SSCH" ~ "B",
  df$PROGRAM == "BS_ECI_SSEI" ~ "B",
  df$PROGRAM == "BS_IEC" ~ "B",
  df$PROGRAM == "BS_IEC_ELA" ~ "B",
  df$PROGRAM == "BS_IEC_EST" ~ "B",
  df$PROGRAM == "BS_IEC_HUM" ~ "B",
  df$PROGRAM == "BS_IEC_MAT" ~ "B",
  df$PROGRAM == "BS_IEC_SOS" ~ "B",
  df$PROGRAM == "BSED_PEM" ~ "B",
  df$PROGRAM == "BSED_PEM_ADP" ~ "B",
  df$PROGRAM == "BSED_PEM_OAE" ~ "B",
  df$PROGRAM == "MST_PHE" ~ "M",
  df$PROGRAM == "MST_PHE_PENC" ~ "M",
  df$PROGRAM == "BA_ESL_CERT" ~ "B",
  df$program_new == "BA_SST" ~ "B",
  df$program_new == "BA_SST_ANT" ~ "B",
  df$program_new == "BA_SST_ECO" ~ "B",
  df$program_new == "BA_SST_GRY" ~ "B",
  df$program_new == "BA_SST_HIS" ~ "B",
  df$program_new == "BA_SST_POL" ~ "B",
  df$program_new == "BA_SST_SOC" ~ "B",
  df$program_new == "BS_ACM" ~ "B",
  df$program_new == "BS_AES" ~ "B",
  df$program_new == "BA_AFS" ~ "B",
  df$program_new == "MAT_ACH" ~ "M",
  df$program_new == "BS_ABI" ~ "B",
  df$program_new == "MAT_ABI" ~ "M",
  df$program_new == "BA_AEN" ~ "B",
  df$program_new == "MAT_AEN" ~ "M",
  df$program_new == "BA_AFR" ~ "B",
  df$program_new == "BA_AEM" ~ "B",
  df$program_new == "BS_AEM" ~ "B",
  df$program_new == "BS_APH" ~ "B",
  df$program_new == "MAT_APH" ~ "M",  
  df$program_new == "BS_APM" ~ "B",
  df$program_new == "BA_ASP" ~ "B",
  df$program_new == "BS_ECD" ~ "B",
  df$program_new == "BS_ECD_ELA" ~ "B",
  df$program_new == "BS_ECD_EST" ~ "B",
  df$program_new == "BS_ECD_HUM" ~ "B",
  df$program_new == "BS_ECD_MAT" ~ "B",
  df$program_new == "BS_ECD_SOS" ~ "B",
  df$program_new == "BS_ECD_UST" ~ "B",
  df$program_new == "MST_CHD" ~ "M",
  df$program_new == "MS_CSD" ~ "M",
  df$program_new == "MS_CSD_CERT" ~ "M",
  df$program_new == "MST_HEA_NCRT" ~ "M",
  df$program_new == "BSED_HEC" ~ "B",
  df$program_new == "BSED_HEC_CHP" ~ "B",
  df$program_new == "BSED_HEC_WEL" ~ "B",
  df$program_new == "BS_ECI" ~ "B",
  df$program_new == "BS_ECI_ELEI" ~ "B",
  df$program_new == "BS_ECI_ESEI" ~ "B",
  df$program_new == "BS_ECI_HMEI" ~ "B",
  df$program_new == "BS_ECI_MTEI" ~ "B",
  df$program_new == "BS_ECI_SSCH" ~ "B",
  df$program_new == "BS_ECI_SSEI" ~ "B",
  df$program_new == "BS_IEC" ~ "B",
  df$program_new == "BS_IEC_ELA" ~ "B",
  df$program_new == "BS_IEC_EST" ~ "B",
  df$program_new == "BS_IEC_HUM" ~ "B",
  df$program_new == "BS_IEC_MAT" ~ "B",
  df$program_new == "BS_IEC_SOS" ~ "B",
  df$program_new == "BSED_PEM" ~ "B",
  df$program_new == "BSED_PEM_ADP" ~ "B",
  df$program_new == "BSED_PEM_OAE" ~ "B",
  df$program_new == "MST_PHE" ~ "M",
  df$program_new == "MST_PHE_PENC" ~ "M",
  df$program_new == "BA_ESL_CERT" ~ "B",
  TRUE ~ ""
))

df <- df %>%
  mutate(degree_new_2 =  case_when(
  df$PROGRAM == "BA_AFS" ~ "B",
  df$PROGRAM == "BS_APM" ~ "B",
  df$PROGRAM == "BS_ECD" ~ "B",
  df$PROGRAM == "BS_ECD_ELA" ~ "B",
  df$PROGRAM == "BS_ECD_EST" ~ "B",
  df$PROGRAM == "BS_ECD_HUM" ~ "B",
  df$PROGRAM == "BS_ECD_MAT" ~ "B",
  df$PROGRAM == "BS_ECD_SOS" ~ "B",
  df$PROGRAM == "BS_ECD_UST" ~ "B",
  df$PROGRAM == "BS_ECI" ~ "B",
  df$PROGRAM == "BS_ECI_ELEI" ~ "B",
  df$PROGRAM == "BS_ECI_ESEI" ~ "B",
  df$PROGRAM == "BS_ECI_HMEI" ~ "B",
  df$PROGRAM == "BS_ECI_MTEI" ~ "B",
  df$PROGRAM == "BS_ECI_SSCH" ~ "B",
  df$PROGRAM == "BS_ECI_SSEI" ~ "B",
  df$PROGRAM == "BS_IEC" ~ "B",
  df$PROGRAM == "BS_IEC_ELA" ~ "B",
  df$PROGRAM == "BS_IEC_EST" ~ "B",
  df$PROGRAM == "BS_IEC_HUM" ~ "B",
  df$PROGRAM == "BS_IEC_MAT" ~ "B",
  df$PROGRAM == "BS_IEC_SOS" ~ "B",
  df$program_new == "BA_SST" ~ "B",
  df$program_new == "BA_AFS" ~ "B",
  df$program_new == "BS_APM" ~ "B",
  df$program_new == "BS_ECD" ~ "B",
  df$program_new == "BS_ECD_ELA" ~ "B",
  df$program_new == "BS_ECD_EST" ~ "B",
  df$program_new == "BS_ECD_HUM" ~ "B",
  df$program_new == "BS_ECD_MAT" ~ "B",
  df$program_new == "BS_ECD_SOS" ~ "B",
  df$program_new == "BS_ECD_UST" ~ "B",
  df$program_new == "BS_ECI" ~ "B",
  df$program_new == "BS_ECI_ELEI" ~ "B",
  df$program_new == "BS_ECI_ESEI" ~ "B",
  df$program_new == "BS_ECI_HMEI" ~ "B",
  df$program_new == "BS_ECI_MTEI" ~ "B",
  df$program_new == "BS_ECI_SSCH" ~ "B",
  df$program_new == "BS_ECI_SSEI" ~ "B",
  df$program_new == "BS_IEC" ~ "B",
  df$program_new == "BS_IEC_ELA" ~ "B",
  df$program_new == "BS_IEC_EST" ~ "B",
  df$program_new == "BS_IEC_HUM" ~ "B",
  df$program_new == "BS_IEC_MAT" ~ "B",
  df$program_new == "BS_IEC_SOS" ~ "B",
  TRUE ~ ""
))

#write to excel to check
library(writexl)
write_xlsx(df, "check_cip_section.xlsx")


##enrollment status
df <- df %>%  
  mutate(enrollment_status =  case_when( 
    ft_pt_202390 == "FT" & ft_pt_202420 == "FT"  ~ "1" ,
    ft_pt_202390 == "PT" & ft_pt_202420 == "PT"  ~ "2",
    ft_pt_202390 == "FT" & ft_pt_202420 == "PT"  ~ "3",
    ft_pt_202390 == "PT" & ft_pt_202420 == "FT"  ~ "3",
    is.na(ft_pt_202390) & ft_pt_202420 == "FT"  ~ "1" ,
    is.na(ft_pt_202390) & ft_pt_202420 == "PT"  ~ "2" ,
    ft_pt_202390 == "FT" & is.na(ft_pt_202420)  ~ "2",
    ft_pt_202390 == "PT" & is.na(ft_pt_202420)  ~ "1" ,
    ft_pt_202390 == "FT" & ft_pt_202420 == ""  ~ "1" ,
    ft_pt_202390 == "PT" & ft_pt_202420 == ""  ~ "2",
    ft_pt_202390 == "" & ft_pt_202420 == "FT"  ~ "1" ,
    ft_pt_202390 == "" & ft_pt_202420 == "PT"  ~ "2",
    is.na(ft_pt_202390) & is.na(ft_pt_202420) & ft_pt_202460 == "FT" ~ "2",
    is.na(ft_pt_202390) & is.na(ft_pt_202420) & ft_pt_202460 == "PT" ~ "2",
    ft_pt_202390 == "" & ft_pt_202420 == "" & ft_pt_202460 == "FT" ~ "2",
    ft_pt_202390 == "" & ft_pt_202420 == ""  & ft_pt_202460 == "PT" ~ "2",
    TRUE ~ ""
    ))
##how to code students who completed but were not enrolled?

##program level
df <- df %>% 
  mutate(program_level =  case_when(
  df$degree_new_1 == "B" ~ "1",
  df$degree_new_1 == "M" ~ "2",
  TRUE ~ ""
))

##new column recoding gender
df <- df %>% 
mutate(gender_new =  case_when(
  df$gender == "M" ~ "1",
  df$gender == "F" ~ "2",
  TRUE ~ ""
))

##new column recoding ethnicity
df <- df %>% 
mutate(ethnicity_new =  case_when(
  df$ipeds_race_eth == "Hispanic/Latino" ~ "1",
  df$ipeds_race_eth == "Black or African American" ~ "2",
  df$ipeds_race_eth == "Asian" ~ "2",
  df$ipeds_race_eth == "American Indian or Alaskan Native" ~ "2",
  df$ipeds_race_eth == "Native Hawaiian or other Pacific Islander" ~ "2",
  df$ipeds_race_eth == "White" ~ "2",
  df$ipeds_race_eth == "Two or more races" ~ "2",
  df$ipeds_race_eth == "NRA" ~ "3",
  df$ipeds_race_eth == "Unknown" ~ "3",
  TRUE ~ "3"
))

##new column recoding race
##leave race blank if hispanic
##code NRA as unknown
df <- df %>% 
mutate(race_new =  case_when(
  df$ipeds_race_eth == "Black or African American" ~ "1",
  df$ipeds_race_eth == "Asian" ~ "2",
  df$ipeds_race_eth == "American Indian or Alaskan Native" ~ "3",
  df$ipeds_race_eth == "Native Hawaiian or other Pacific Islander" ~ "4",
  df$ipeds_race_eth == "White" ~ "5",
  df$ipeds_race_eth == "Two or more races" ~ "6",
  df$ipeds_race_eth == "NRA" ~ "",
  df$ipeds_race_eth == "Unknown" ~ "",
  df$ipeds_race_eth == "Hispanic/Latino" ~ "",
  TRUE ~ ""
))

#column for program codes
df <- df %>% 
  mutate(program_code =  case_when(
  df$PROGRAM == "BA_SST" ~ "22930",
  df$PROGRAM == "BA_SST_ANT" ~ "22930",
  df$PROGRAM == "BA_SST_ECO" ~ "22930",
  df$PROGRAM == "BA_SST_GRY" ~ "22930",
  df$PROGRAM == "BA_SST_HIS" ~ "22930",
  df$PROGRAM == "BA_SST_POL" ~ "22930",
  df$PROGRAM == "BA_SST_SOC" ~ "22930",
  df$PROGRAM == "BS_ACM" ~ "22922",
  df$PROGRAM == "BS_AES" ~ "22924",
  df$PROGRAM == "BA_AFS" ~ "30649",
  df$PROGRAM == "MAT_ACH" ~ "25108",
  df$PROGRAM == "BS_ABI" ~ "22920",
  df$PROGRAM == "MAT_ABI" ~ "25114",
  df$PROGRAM == "BA_AEN" ~ "22929",
  df$PROGRAM == "MAT_AEN" ~ "25106",
  df$PROGRAM == "BA_AFR" ~ "22932",
  df$PROGRAM == "BA_AEM" ~ "22918",
  df$PROGRAM == "BS_AEM" ~ "22919",
  df$PROGRAM == "BS_APH" ~ "22926",
  df$PROGRAM == "MAT_APH" ~ "25122",  
  df$PROGRAM == "BS_APM" ~ "23377",
  df$PROGRAM == "BA_ASP" ~ "22931",
  df$PROGRAM == "BS_ECD" ~ "23373",
  df$PROGRAM == "BS_ECD_ELA" ~ "23373",
  df$PROGRAM == "BS_ECD_EST" ~ "23373",
  df$PROGRAM == "BS_ECD_HUM" ~ "23373",
  df$PROGRAM == "BS_ECD_MAT" ~ "23373",
  df$PROGRAM == "BS_ECD_SOS" ~ "23373",
  df$PROGRAM == "BS_ECD_UST" ~ "23373",
  df$PROGRAM == "MST_CHD" ~ "22928",
  df$PROGRAM == "MS_CSD" ~ "33410",
  df$PROGRAM == "MS_CSD_CERT" ~ "33410",
  df$PROGRAM == "MST_HEA_NCRT" ~ "25112",
  df$PROGRAM == "BSED_HEC" ~ "23375",
  df$PROGRAM == "BSED_HEC_CHP" ~ "23375",
  df$PROGRAM == "BSED_HEC_WEL" ~ "23375",
  df$PROGRAM == "BS_ECI" ~ "23374",
  df$PROGRAM == "BS_ECI_ELEI" ~ "23374",
  df$PROGRAM == "BS_ECI_ESEI" ~ "23374",
  df$PROGRAM == "BS_ECI_HMEI" ~ "23374",
  df$PROGRAM == "BS_ECI_MTEI" ~ "23374",
  df$PROGRAM == "BS_ECI_SSCH" ~ "23374",
  df$PROGRAM == "BS_ECI_SSEI" ~ "23374",
  df$PROGRAM == "BS_IEC" ~ "36629",
  df$PROGRAM == "BS_IEC_ELA" ~ "36629",
  df$PROGRAM == "BS_IEC_EST" ~ "36629",
  df$PROGRAM == "BS_IEC_HUM" ~ "36629",
  df$PROGRAM == "BS_IEC_MAT" ~ "36629",
  df$PROGRAM == "BS_IEC_SOS" ~ "36629",
  df$PROGRAM == "BSED_PEM" ~ "23376",
  df$PROGRAM == "BSED_PEM_ADP" ~ "23376",
  df$PROGRAM == "BSED_PEM_OAE" ~ "23376",
  df$PROGRAM == "MST_PHE" ~ "39290",
  df$PROGRAM == "MST_PHE_PENC" ~ "39290",
  df$PROGRAM == "BA_ESL_CERT" ~ "29720",
  df$program_new == "BA_SST" ~ "22930",
  df$program_new == "BA_SST_ANT" ~ "22930",
  df$program_new == "BA_SST_ECO" ~ "22930",
  df$program_new == "BA_SST_GRY" ~ "22930",
  df$program_new == "BA_SST_HIS" ~ "22930",
  df$program_new == "BA_SST_POL" ~ "22930",
  df$program_new == "BA_SST_SOC" ~ "22930",
  df$program_new == "BS_ACM" ~ "22922",
  df$program_new == "BS_AES" ~ "22924",
  df$program_new == "BA_AFS" ~ "30649",
  df$program_new == "MAT_ACH" ~ "25108",
  df$program_new == "BS_ABI" ~ "22920",
  df$program_new == "MAT_ABI" ~ "25114",
  df$program_new == "BA_AEN" ~ "22929",
  df$program_new == "MAT_AEN" ~ "25106",
  df$program_new == "BA_AFR" ~ "22932",
  df$program_new == "BA_AEM" ~ "22918",
  df$program_new == "BS_AEM" ~ "22919",
  df$program_new == "BS_APH" ~ "22926",
  df$program_new == "MAT_APH" ~ "25122",  
  df$program_new == "BS_APM" ~ "23377",
  df$program_new == "BA_ASP" ~ "22931",
  df$program_new == "BS_ECD" ~ "23373",
  df$program_new == "BS_ECD_ELA" ~ "23373",
  df$program_new == "BS_ECD_EST" ~ "23373",
  df$program_new == "BS_ECD_HUM" ~ "23373",
  df$program_new == "BS_ECD_MAT" ~ "23373",
  df$program_new == "BS_ECD_SOS" ~ "23373",
  df$program_new == "BS_ECD_UST" ~ "23373",
  df$program_new == "MST_CHD" ~ "22928",
  df$program_new == "MS_CSD" ~ "33410",
  df$program_new == "MS_CSD_CERT" ~ "33410",
  df$program_new == "MST_HEA_NCRT" ~ "25112",
  df$program_new == "BSED_HEC" ~ "23375",
  df$program_new == "BSED_HEC_CHP" ~ "23375",
  df$program_new == "BSED_HEC_WEL" ~ "23375",
  df$program_new == "BS_ECI" ~ "23374",
  df$program_new == "BS_ECI_ELEI" ~ "23374",
  df$program_new == "BS_ECI_ESEI" ~ "23374",
  df$program_new == "BS_ECI_HMEI" ~ "23374",
  df$program_new == "BS_ECI_MTEI" ~ "23374",
  df$program_new == "BS_ECI_SSCH" ~ "23374",
  df$program_new == "BS_ECI_SSEI" ~ "23374",
  df$program_new == "BS_IEC" ~ "36629",
  df$program_new == "BS_IEC_ELA" ~ "36629",
  df$program_new == "BS_IEC_EST" ~ "36629",
  df$program_new == "BS_IEC_HUM" ~ "36629",
  df$program_new == "BS_IEC_MAT" ~ "36629",
  df$program_new == "BS_IEC_SOS" ~ "36629",
  df$program_new == "BSED_PEM" ~ "23376",
  df$program_new == "BSED_PEM_ADP" ~ "23376",
  df$program_new == "BSED_PEM_OAE" ~ "23376",
  df$program_new == "MST_PHE" ~ "39290",
  df$program_new == "MST_PHE_PENC" ~ "39290",
  df$program_new == "BA_ESL_CERT" ~ "29720",
  TRUE ~ ""
))

#write to excel to check
library(writexl)
write_xlsx(df, "step_8_crosswalking_and_adding_title_ii_data_elements.xlsx")

##Years to Degree
##only count fall & spring
##only count enrolled semesters
##go back until HEH = 1 2, or 6 
##load ess data back 6 years
ess_201790 <-read.csv("orion-ess-201790-1101-official.csv",header=TRUE)
ess_201820 <-read.csv("orion-ess-201820_0406_official.csv",header=TRUE)
ess_201890 <-read.csv("orion_ess_201890_official.csv",header=TRUE)
ess_201920 <-read.csv("orion_ess_201920_0327_OFFICIAL.csv",header=TRUE)
ess_201990 <-read.csv("orion_ess_fall2019_official.csv",header=TRUE)
ess_202020 <-read.csv("orion_ess_sprg2020_official.csv",header=TRUE)
ess_202090 <-read.csv("orion_fall2020_ess_official.csv",header=TRUE)
ess_202120 <-read.csv("orion_sprg2021_ess_official.csv",header=TRUE)
ess_202190 <-read.csv("Fall2021ess_official.csv",header=TRUE)
ess_202220 <-read.csv("orion-sds-ess-202220-0401_official.csv",header=TRUE)
ess_202290 <-read.csv("orion-SDS-202290ESS_official.csv",header=TRUE)
ess_202320 <-read.csv("orion-ess-202320-official.csv",header=TRUE)

##pull only HEH and ID from the ess files (also grab gender, name, DOB, ipeds race/eth to use to back-fill completers who weren't enrolled)
ess_201790 <- ess_201790[, c( "Campus_ID" , "Higher_Ed_Hist", "Last_Name", "First_Name", "Mi", "Dob", "Gender", "IPEDS_RaceEth")]
ess_201820 <- ess_201820[, c( "Campus_ID" , "Higher_Ed_Hist", "Last_Name", "First_Name", "Mi", "Dob", "Gender", "IPEDS_RaceEth")]
ess_201890 <- ess_201890[, c( "LOCAL_ID" , "HIGHER_ED_HIST", "LAST_NAME", "FIRST_NAME", "MI", "DOB", "GENDER", "IPEDS_RaceEth")]
ess_201920 <- ess_201920[, c( "LOCAL_ID" , "HIGHER_ED_HIST", "LAST_NAME", "FIRST_NAME", "MI", "DOB", "GENDER", "ipeds_race")]
ess_201990 <- ess_201990[, c( "LOCAL_ID" , "HIGHER_ED_HIST", "LAST_NAME", "FIRST_NAME", "MI", "DOB", "GENDER", "ipeds_race")]
ess_202020 <- ess_202020[, c( "LOCAL_ID" , "HIGHER_ED_HIST", "LAST_NAME", "FIRST_NAME", "MI", "DOB", "GENDER", "ipeds_race")]
ess_202090 <- ess_202090[, c( "LOCAL_ID" , "HIGHER_ED_HIST", "LAST_NAME", "FIRST_NAME", "MI", "DOB", "GENDER", "ipeds_race")]
ess_202120 <- ess_202120[, c( "LOCAL_ID" , "HIGHER_ED_HIST", "LAST_NAME", "FIRST_NAME", "MI", "DOB", "GENDER", "ipeds_race")]
ess_202190 <- ess_202190[, c( "LOCAL_ID" , "HIGHER_ED_HIST", "LAST_NAME", "FIRST_NAME", "MI", "DOB", "GENDER", "ipeds_race")]
ess_202220 <- ess_202220[, c( "LOCAL_ID" , "HIGHER_ED_HIST", "LAST_NAME", "FIRST_NAME", "MI", "DOB", "GENDER", "IPEDS.Race.Ethnicity")]
ess_202290 <- ess_202290[, c( "CAMPUS_ID" , "HIGHER_ED_HIST", "LAST_NAME", "FIRST_NAME", "MI", "DOB", "GENDER", "IPEDS.Race.Ethnicity")]
ess_202320 <- ess_202320[, c( "CAMPUS_ID" , "HIGHER_ED_HIST", "LAST_NAME", "FIRST_NAME", "MI", "DOB", "GENDER", "IPEDS.Race.Ethnicity")]

#rename id & HEH for join
ess_201790 <- ess_201790 %>% rename(id = Campus_ID, heh_201790 = Higher_Ed_Hist)
ess_201820 <- ess_201820 %>% rename(id = Campus_ID, heh_201820 = Higher_Ed_Hist)
ess_201890 <- ess_201890 %>% rename(id = LOCAL_ID, heh_201890 = HIGHER_ED_HIST)
ess_201920 <- ess_201920 %>% rename(id = LOCAL_ID, heh_201920 = HIGHER_ED_HIST)
ess_201990 <- ess_201990 %>% rename(id = LOCAL_ID, heh_201990 = HIGHER_ED_HIST)
ess_202020 <- ess_202020 %>% rename(id = LOCAL_ID, heh_202020 = HIGHER_ED_HIST)
ess_202090 <- ess_202090 %>% rename(id = LOCAL_ID, heh_202090 = HIGHER_ED_HIST)
ess_202120 <- ess_202120 %>% rename(id = LOCAL_ID, heh_202120 = HIGHER_ED_HIST)
ess_202190 <- ess_202190 %>% rename(id = LOCAL_ID, heh_202190 = HIGHER_ED_HIST)
ess_202220 <- ess_202220 %>% rename(id = LOCAL_ID, heh_202220 = HIGHER_ED_HIST)
ess_202290 <- ess_202290 %>% rename(id = CAMPUS_ID, heh_202290 = HIGHER_ED_HIST)
ess_202320 <- ess_202320 %>% rename(id = CAMPUS_ID, heh_202320 = HIGHER_ED_HIST)

#join needed ess columns
df <- df %>%
  left_join(ess_201790, by = "id")%>%
  left_join(ess_201820, by = "id")%>%
  left_join(ess_201890, by = "id")%>%
  left_join(ess_201920, by = "id")%>%
  left_join(ess_201990, by = "id")%>%
  left_join(ess_202020, by = "id")%>%
  left_join(ess_202090, by = "id")%>%
  left_join(ess_202120, by = "id")%>%
  left_join(ess_202190, by = "id")%>%
  left_join(ess_202220, by = "id")%>%
  left_join(ess_202290, by = "id")%>%
  left_join(ess_202320, by = "id")

##move heh columns to be next to each other
df <- df %>% 
  relocate(heh_201820, .after = heh_201790) %>% 
  relocate(heh_201890, .after = heh_201820) %>% 
  relocate(heh_201920, .after = heh_201890) %>% 
  relocate(heh_201990, .after = heh_201920) %>% 
  relocate(heh_202020, .after = heh_201990) %>% 
  relocate(heh_202090, .after = heh_202020) %>% 
  relocate(heh_202120, .after = heh_202090) %>% 
  relocate(heh_202190, .after = heh_202120) %>% 
  relocate(heh_202220, .after = heh_202190) %>% 
  relocate(heh_202290, .after = heh_202220) %>% 
  relocate(heh_202320, .after = heh_202290) %>% 
  relocate(heh_202390, .after = heh_202320) %>%
  relocate(heh_202420, .after = heh_202390) 


#write to excel to check
library(writexl)
write_xlsx(df, "step_9_join_heh_last_6_years.xlsx")
 
#clean up workspace
rm(ess_201790,ess_201820,  ess_201890, ess_201920, ess_201990, ess_202020,
   ess_202090, ess_202120, ess_202190, ess_202220, ess_202290, ess_202320)

#create column to count enrolled semesters
##look at course_level_new column,
#if course_level_new = UG then 
#search all heh columns for when heh = 1 or 2 
#count all instances of heh = 4 after the 1 or 2
#if course_level_new = GR then
#search all heh columns for when heh = 6
#count all instances of heh = 7 after the 6
#column should add 1 to the count of 4s or 6s 
#if heh is ever 1/2 for UG or 6 for GR more than once then flag check
#if never 1/2 or 6 then fill in "check admit term"

##calculate semesters enrolled

##define heh columns to search 
enrollment_cols <- c("heh_201790", "heh_201820", "heh_201890", "heh_201920", "heh_201990",
                 "heh_202020", "heh_202090", "heh_202120", "heh_202190", "heh_202220", 
                 "heh_202290", "heh_202320", "heh_202390", "heh_202420")

#make sure needed columns are in data
enrollment_cols <- enrollment_cols[enrollment_cols %in% names(df)]

##create function to count by the rules above 
calculate_semesters_enrolled_count <- function(
    
  course_level, enrollment_data) {

  enrollment_values <- rev(enrollment_data)
  
  if (course_level == "UG") {
    start_vals <- c(1, 2)
    count_val <- 4
  } else if (course_level == "GR") {
    start_vals <- c(6)
    count_val <- 7
  } else {
    return(as.character(NA))  
  }
  
  #find first occurrence of 1, 2, or 6
  start_idx <- which(enrollment_data %in% start_vals)
  
  if (length(start_idx) == 0) {
    return("check admit term")
  }
  
  #flag as "check" if more than one occurrence of 1, 2, or 6 
  if (length(start_idx) > 1) {
    return("check")
  }
  
  #find count of count_val after start_idx
  count_after <- sum(enrollment_data[(start_idx + 1):length(enrollment_data)] == count_val, na.rm = TRUE)
  
  return(as.character(count_after + 1))
}

#apply function to each row
df <- df %>%
  rowwise() %>%
  mutate(semesters_enrolled_count = calculate_semesters_enrolled_count(
    course_level_new,
    c_across(all_of(enrollment_cols))
  )) %>%
  ungroup() %>%
  mutate(
    semesters_enrolled_count = as.character(semesters_enrolled_count)
  )

#move new column to the end of the heh columns
df <- df %>% 
  relocate(semesters_enrolled_count, .after = heh_202420)

#write to excel to check
library(writexl)
write_xlsx(df, "step_10_check_semesters_enrolled_sum.xlsx")

##add column to translate semesters attended to years to degree
df <- df %>% 
  mutate(
    years_to_degree = case_when(
      semesters_enrolled_count == "1" ~ "1",
      semesters_enrolled_count == "2" ~ "1",
      semesters_enrolled_count == "3" ~ "2",
      semesters_enrolled_count == "4" ~ "2",
      semesters_enrolled_count == "5" ~ "3",
      semesters_enrolled_count == "6" ~ "3",
      semesters_enrolled_count == "7" ~ "4",
      semesters_enrolled_count == "8" ~ "4",
      semesters_enrolled_count == "9" ~ "5",
      semesters_enrolled_count == "10" ~ "5",
      semesters_enrolled_count == "11" ~ "6",
      semesters_enrolled_count == "12" ~ "6",
      TRUE ~ "enter manually"
    )
  )

#move new column next to the semesters enrolled column
df <- df %>% 
  relocate(years_to_degree, .after = semesters_enrolled_count)

#write to excel to check
library(writexl)
write_xlsx(df, "step_11_check_years_to_degree_conversion.xlsx")


##at this point do any manual cleaning/edits that need to be done
##will likely need to go back and add demographic info for a few completers who 
##were not enrolled during the year
##will likely need to check/manually enter the semesters enrolled & years to degree
##for a few students (started > 6 years ago or in a winter/summer term)

##reload data after manual check for final cleanup 
#install.packages("readr")
library(readr)
df <-read_csv("cohort_all_data_elements_incl_notes.csv",
              col_types = cols(
                ssn5 = 
               col_character(),
              dob = 
                col_character(),
              code_1 = 
                col_character(),
              cip_code_1 = 
                col_character(),
              code_2 = 
                col_character(),
              cip_code_2 = 
                col_character(),
              program_code = 
                col_character()))

##create blank columns as placeholders so things will line up correctly
df$code_3 <- NA
df$cip_code_3 <- NA
df$degree_new_3 <- NA
df$code_4 <- NA
df$cip_code_4 <- NA
df$degree_new_4 <- NA

##select only needed columns in order matching title ii data collection worksheet
df <- df[, c( "ssn5" , "last_name" , "first_name", "mi", "dob",
              "program_type", "reporting_group", "code_1", "cip_code_1", "degree_new_1",
              "code_2", "cip_code_2", "degree_new_2", "code_3" , "cip_code_3", "degree_new_3",
              "code_4", "cip_code_4", "degree_new_4", "years_to_degree", "enrollment_status",
              "program_level", "gender_new", "ethnicity_new", "race_new", "program_code")]

#write to excel to check
library(writexl)
write_xlsx(df, "title_ii_draft_20250129.xlsx")