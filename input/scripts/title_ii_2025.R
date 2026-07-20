##title ii 2025 

##load libraries
library(dplyr)
library(stringr)
library(lubridate)
library(stringdist)
library(tidyr)
library(tidyverse) 
library(purrr)
library(writexl)

##load data
eot_2490 <-read.csv("eot_202490_20250305_final_w_race.csv",header=TRUE)
eot_2510 <-read.csv("eot_202510_20250507_final_w_race.csv",header=TRUE)
eot_2520 <-read.csv("eot_202520_20260126_final_w_race.csv",header=TRUE)
eot_2560 <-read.csv("eot_202560_20260126_final.csv",header=TRUE)
csf_2490 <-read.csv("student_202490_20250306.csv",header=TRUE)
csf_2510 <-read.csv("student_202510_20250306.csv",header=TRUE)
csf_2520 <-read.csv("student_eot_20250606.csv",header=TRUE)
csf_2560 <-read.csv("student_list_202560_20250730.csv",header=TRUE)

##clean data & select only needed columns

#add ft_pt columns
eot_2490 <- eot_2490 %>%
  mutate(
    ft_pt = 
      case_when(
        COURSE_LEVEL == "UG" & TOTAL_CREDITS >= 12 ~ "FT",
        COURSE_LEVEL == "UG" & TOTAL_CREDITS < 12 ~ "PT",
        COURSE_LEVEL == "GR" & TOTAL_CREDITS >= 9 ~ "FT",
        COURSE_LEVEL == "GR" & TOTAL_CREDITS < 9 ~ "PT",
        TRUE ~ NA
      )
  )
eot_2510 <- eot_2510 %>%
  mutate(
    ft_pt = 
      case_when(
        COURSE_LEVEL == "UG" & TOTAL_CREDITS >= 12 ~ "FT",
        COURSE_LEVEL == "UG" & TOTAL_CREDITS < 12 ~ "PT",
        COURSE_LEVEL == "GR" & TOTAL_CREDITS >= 9 ~ "FT",
        COURSE_LEVEL == "GR" & TOTAL_CREDITS < 9 ~ "PT",
        TRUE ~ NA
      )
  )
eot_2520 <- eot_2520 %>%
  mutate(
    ft_pt = 
      case_when(
        COURSE_LEVEL == "UG" & TOTAL_CREDITS >= 12 ~ "FT",
        COURSE_LEVEL == "UG" & TOTAL_CREDITS < 12 ~ "PT",
        COURSE_LEVEL == "GR" & TOTAL_CREDITS >= 9 ~ "FT",
        COURSE_LEVEL == "GR" & TOTAL_CREDITS < 9 ~ "PT",
        TRUE ~ NA
      )
  )
eot_2560 <- eot_2560 %>%
  mutate(
    ft_pt = 
      case_when(
        COURSE_LEVEL == "UG" & total_credits >= 12 ~ "FT",
        COURSE_LEVEL == "UG" & total_credits < 12 ~ "PT",
        COURSE_LEVEL == "GR" & total_credits >= 9 ~ "FT",
        COURSE_LEVEL == "GR" & total_credits < 9 ~ "PT",
        TRUE ~ NA
      )
  )

#eot
#make all eot columns lowercase
e_names <- ls(envir = .GlobalEnv)[ grepl("^eot_", ls(envir = .GlobalEnv)) ]
for (nm in e_names) {
  tmp <- get(nm, envir = .GlobalEnv)
  names(tmp) <- tolower(names(tmp))
  assign(nm, tmp, envir = .GlobalEnv)
}
rm(tmp)

#rename local_id and campus_id to id
for (nm in e_names) {
  tmp <- get(nm, envir = .GlobalEnv)
  
  #find which of the two old names exist
  rename_cols <- intersect(c("local_id", "campus_id"), names(tmp))
  
  #rename each to id
  for (old in rename_cols) {
    names(tmp)[names(tmp) == old] <- "id"
  }
  
  #write it back
  assign(nm, tmp, envir = .GlobalEnv)
}
rm(tmp)

##rename columns to consistent names across all 
#eot datasets & select only needed columns
select_eot_cols_fuzzy <- function(df) {
  #standard name -> regex for its variants
  patterns <- list(
    id             = "^id$",
    ssn             = "^ssn$",
    first_name      = "^first[_\\.]name$",
    mi              = "^mi$",
    last_name       = "^m[_\\.]i$",
    dob             = "^dob$",
    gender          = "^gender$",
    ipeds_race      = "^ipeds(?:[_\\.-](race(?:_ethnicity)?|race_eth|race\\.ethnicity|ethnicity|raceth|raceeth|race(?:_eth)?))$",
    course_level    = "^course[\\._]*level$",
    ft_pt           = "^(ft[_\\.]?pt|full[_\\.]?time|part[_\\.]?time|fpt|ftpt|fp)$",
    higher_ed_hist  = "^(higher[\\._]*ed[\\._]*(hist(ory)?)?|heh)$",
    prim_award_lvl  = "^(prim_award_lvl|prim_aw.ard_lvl)$"
  )
  
  for (std_name in names(patterns)) {
    pat  <- patterns[[std_name]]
    cols <- names(df)
    
    #find all matches to the regex
    hits <- grep(pat, cols, ignore.case = TRUE, value = TRUE)
    #drop any that are already the standard name
    to_rename <- setdiff(hits, std_name)
    
    if (length(to_rename) > 0) {
      #rename the first unmatched variant
      df <- df %>% rename(!!std_name := !!sym(to_rename[1]))
    }
  }
  
  #select only the standardized column names that exist
  df %>% select(any_of(names(patterns)))
}

#apply it to every eot
for (nm in e_names) {
  assign(
    nm,
    select_eot_cols_fuzzy(get(nm, envir = .GlobalEnv)),
    envir = .GlobalEnv
  )
}

##csf
#make all csf columns lowercase
c_names <- ls(envir = .GlobalEnv)[ grepl("^csf_", ls(envir = .GlobalEnv)) ]
for (nm in c_names) {
  tmp <- get(nm, envir = .GlobalEnv)
  names(tmp) <- tolower(names(tmp))
  assign(nm, tmp, envir = .GlobalEnv)
}
rm(tmp)

#csf datasets & select only needed columns
select_csf_cols_fuzzy <- function(df) {
  #standard name -> regex for its variants
  patterns <- list(
    id             = "^id$",
    admit_term      = "^admit[_\\.]term$",
    catalog_term    = "^catalog[_\\.]term$",
    school          = "^(schl|school|college|schl-csf)$",
    department      = "^(department|dept|first_dept|dept-csf)$", 
    degree          = "^(degree|deg|dgr|dgr-csf)$",
    major           = "^(major|majr|majr-csf)$",
    program         = "^(program|pgm|progrm|program-csf)$",
    school_2        = "^(schl2|school2|college2|schl[\\._]*2|school[\\._]*2|college[\\._]*2|schl2)$",
    department_2    = "^(department2|dept2|dept[\\._]*2|department[\\._]*2|sec_dept|dept2-csf)$", 
    major_2         = "^(major2|majr2|majr[\\._]*2|major[\\._]*2|sec_major|majr2-csf)$"
  )
  
  for (std_name in names(patterns)) {
    pat  <- patterns[[std_name]]
    cols <- names(df)
    
    #find all matches to the regex
    hits <- grep(pat, cols, ignore.case = TRUE, value = TRUE)
    #drop any that are already the standard name
    to_rename <- setdiff(hits, std_name)
    
    if (length(to_rename) > 0) {
      #rename the first unmatched variant
      df <- df %>% rename(!!std_name := !!sym(to_rename[1]))
    }
  }
  
  #select only the standardized column names that exist
  df %>% select(any_of(names(patterns)))
}

#apply it to every csf
for (nm in c_names) {
  assign(
    nm,
    select_csf_cols_fuzzy(get(nm, envir = .GlobalEnv)),
    envir = .GlobalEnv
  )
}


#join corresponding eot & csf
eot_2490 <- eot_2490 %>% left_join(csf_2490, by = "id")
eot_2510 <- eot_2510 %>% left_join(csf_2510, by = "id")
eot_2520 <- eot_2520 %>% left_join(csf_2520, by = "id")
eot_2560 <- eot_2560 %>% left_join(csf_2560, by = "id")

#clean up workspace
rm(csf_2490, csf_2510, csf_2520, csf_2560)

#remove Ws from major codes 
#loop through each data frame
for (df_name in e_names) {
  df <- get(df_name)
  
  #check that it has major column
  if ("major" %in% names(df)) {
    #remove trailing "W" 
    df$major <- sub("W$", "", df$major)
    
    #assign back to environment
    assign(df_name, df)
  }
}

#define TED major codes
ted_codes <- c(
  "ABI","ACH","ACM","AEM", "APH","APM", "AES",
  "AEN","AFR","AFS","ASP", "SST",
  "CHD", "ECD", "ECI", "IEC", "TDA","TSD",
  "CSD", "SHS",
  "ESL", "SLED",
  "HEA","HEC",
  "LTE",
  "PEL","PEM","PHE",
  "SBL","SDBL","SDL"  
)

#create new column labeling TED or not - first major
for (nm in e_names) {
  df <- get(nm, inherits = TRUE)
  if ("major" %in% names(df)) {
    #compare (coerce to character; treat NA as NOT)
    majors <- as.character(df$major)
    is_ted <- !is.na(majors) & majors %in% ted_codes
    df$TED <- ifelse(is_ted, "TED", "NOT")
    assign(nm, df)
  }
}

#create new column labeling TED or not - second major
for (nm in e_names) {
  df <- get(nm, inherits = TRUE)
  if ("major" %in% names(df)) {
    #compare (coerce to character; treat NA as NOT)
    majors <- as.character(df$major_2)
    is_ted <- !is.na(majors) & majors %in% ted_codes
    df$TED_2 <- ifelse(is_ted, "TED", "NOT")
    assign(nm, df)
  }
}

#add term as suffix to columns before joining
for (nm in e_names) {
  df <- get(nm, inherits = TRUE)
  
  #extract the number that comes after eot_
  suffix <- sub("^eot_", "", nm)
  
  #columns that should NOT be renamed
  exclude <- c("id", "first_name", "last_name", "mi", "ssn", "dob", "gender", "ipeds_race")
  
  #determine which columns to rename
  rename_cols <- setdiff(names(df), exclude)
  
  #create the new names
  new_names <- names(df)
  new_names[names(df) %in% rename_cols] <- paste0(rename_cols, "_", suffix)
  
  #apply the new column names
  names(df) <- new_names
  
  #assign back to the environment
  assign(nm, df)
}

#join all terms for full year cohort
cohort <- eot_2490 %>%
  full_join(eot_2510, by = "id") %>%
  full_join(eot_2520, by = "id") %>%
  full_join(eot_2560, by = "id") 

#collapse name, ssn, dob, gender, ipeds_race columns
cohort <- cohort %>%
  mutate(
    first_name = coalesce(first_name.x, first_name.y, first_name.x.x, first_name.y.y),
    last_name  = coalesce(last_name.x, last_name.y, last_name.x.x, last_name.y.y),
    mi  = coalesce(mi.x, mi.y, mi.x.x, mi.y.y),
    ssn  = coalesce(ssn.x, ssn.y, ssn.x.x, ssn.y.y),
    dob  = coalesce(dob.x, dob.y, dob.x.x, dob.y.y),
    gender  = coalesce(gender.x, gender.y, gender.x.x, gender.y.y),
    ipeds_race  = coalesce(ipeds_race.x, ipeds_race.y, ipeds_race.x.x, ipeds_race.y.y)
  ) %>%
  select(-first_name.x, -first_name.y, -first_name.x.x, -first_name.y.y,
         -last_name.x, -last_name.y, -last_name.x.x, -last_name.y.y,
         -mi.x, -mi.y, -mi.x.x, -mi.y.y,
         -ssn.x, -ssn.y, -ssn.x.x, -ssn.y.y,
         -dob.x, -dob.y, -dob.x.x, -dob.y.y,
         -gender.x, -gender.y, -gender.x.x, -gender.y.y,
         -ipeds_race.x, -ipeds_race.y, -ipeds_race.x.x, -ipeds_race.y.y
         )

#move name, ssn, dob, gender, ipeds_race columns back to front of dataframe
cohort <- cohort %>%
  relocate(ssn, first_name, mi, last_name, dob, gender, ipeds_race, .after = id)

#ensure no duplicates
cohort <- unique(cohort)

#clean up environment
rm(df, eot_2490, eot_2510, eot_2520, eot_2560)
rm(e_names, c_names, exclude, df_name, is_ted, majors, new_names, nm, old, rename_cols, suffix)
rm(select_csf_cols_fuzzy, select_eot_cols_fuzzy)

#make ssn column character columns 
cohort$ssn <- as.character(cohort$ssn)

#format DOB correctly
cohort$dob <- sprintf("%08d", as.numeric(cohort$dob))
cohort$dob <- as.Date(cohort$dob, format = "%m%d%Y")
cohort$dob <- format(cohort$dob, "%m/%d/%y")

#write to excel to check
write_xlsx(cohort, "step_1_eot_csf_all_terms_all_students_labeled_ted.xlsx")


##------------STEP 2: SUBSET TO TED ONLY----------------------------------------
#subset down to only TED cohort
cohort <- cohort[
  apply(cohort[ , grepl("^TED_", names(cohort))], 1, function(x) any(x == "TED")),
]

#clear out blanked rows
cohort <- cohort[!apply(is.na(cohort) | cohort == "", 1, all), ]

#write to excel to check
write_xlsx(cohort, "step_2_ted_only.xlsx")


##------------STEP 3: TAG COURSE LEVEL CHANGES----------------------------------
##create a column to check for course lvl changes
cohort <- cohort %>%
  rowwise() %>%
  mutate(
    course_lvl_change = {
      levels <- c(course_level_2490, course_level_2510, course_level_2520, 
                  course_level_2560)
      levels_clean <- na.omit(levels[levels != ""])
      if (length(unique(levels_clean)) == 1) {
        "no course lvl change"
      } else {
        change_year <- c("2490", "2510", "2520", "2560")[which(levels_clean != levels_clean[1])[1]]
        change_year
      }
    }
  ) %>%
  ungroup()

#write to excel to check
write_xlsx(cohort, "step_3_flag_for_course_level_changes_added.xlsx")

##------------STEP 4: TAG ENDED YEAR IN TED OR NOT----------------------------------
##create a column to tag if they ended the year in a TED major
cohort <- cohort %>%  
  mutate(TED_year_end =  case_when( 
    TED_2560 == "TED"  ~ "yes" , 
    is.na(TED_2560) & TED_2520 == "TED" ~ "yes", 
    TED_2560 == "" & TED_2520 == "TED" ~ "yes",
    is.na(TED_2560) & is.na(TED_2520) & TED_2510 == "TED" ~ "yes", 
    TED_2560 == "" & TED_2520 == "" & TED_2510 == "TED" ~ "yes",
    is.na(TED_2560) & is.na(TED_2520) & is.na(TED_2510) & TED_2490 == "TED" ~ "yes",
    TED_2560 == "" & TED_2520 == "" & TED_2510 == "" & TED_2490 == "TED" ~ "yes",
    TED_2560 == "TED" | TED_2520 == "TED" | TED_2510 == "TED" | TED_2490 == "TED"  ~ "check",
    TRUE ~ "NOT"
  ))

write_xlsx(cohort, "step_4_flag_for_last_semester_TED.xlsx")


##------------STEP 5: ADD COMPLETERS INFO---------------------------------------
#need TED completers between 9/1/24 & 8/31/25
#load data
dcl <- read.csv("Degree Completer Listing_20260127_082131.csv",header=TRUE)

#clean column names
names(dcl) <- gsub("^(SHRDGMR\\.SHRDGMR_|SPRIDEN\\.SPRIDEN_|SPBPERS_|STVMAJR\\.STVMAJR_)", "", names(dcl))

#select only needed columns
dcl <- dcl[, c( "ID" , "GRAD_DATE" , "PROGRAM" , "DEGC_CODE","COLL_CODE_1", 
                "MAJR_CODE_1" , "DEGS_CODE")]
#rename columns
dcl <- dcl %>% rename(id = ID,  
                      grad_degree = DEGC_CODE,
                      grad_school = COLL_CODE_1,  
                      grad_major = MAJR_CODE_1, 
                      grad_program = PROGRAM)

#remove Ws from grad majors
dcl$grad_major <- sub("W$", "", dcl$grad_major)

#remove students who didn't graduate
dcl <- subset(dcl, dcl$DEGS_CODE == "UA" | dcl$DEGS_CODE == "GA")

##remove non-TED degrees
dcl <- subset(dcl, dcl$grad_major %in% ted_codes)

#join DCL to cohort
cohort <- cohort %>%
  full_join(dcl, by = "id")

#cleanup workspace & remove old things
rm(dcl)

#make column to mark graduates
cohort <- cohort %>%
  mutate(GRAD_STATUS =
           if_else(is.na(GRAD_DATE), "NOT",
                   "GRADUATED"))

write_xlsx(cohort, "step_5_add_completer_info.xlsx")


##------------STEP 6: TAG INITIAL CERTS---------------------------------------

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
cohort <- cohort %>%  
  mutate(initial_cert =  case_when( 
    program_2560 %in% initial_cert_codes  ~ "yes" , 
    is.na(program_2560) & program_2520 %in% initial_cert_codes ~ "yes", 
    program_2560 == "" & program_2520 %in% initial_cert_codes ~ "yes",
    is.na(program_2560) & is.na(program_2520) & program_2510 %in% initial_cert_codes ~ "yes", 
    program_2560 == "" & program_2520 == "" & program_2510 %in% initial_cert_codes ~ "yes",
    is.na(program_2560) & is.na(program_2520) & is.na(program_2510) & program_2490 %in% initial_cert_codes ~ "yes",
    program_2560 == "" & program_2520 == "" & program_2510 == "" & program_2490 %in% initial_cert_codes ~ "yes",
    grad_program %in% initial_cert_codes  ~ "yes" ,
    TRUE ~ "NOT"
  ))

write_xlsx(cohort, "step_6_add_flag_for_initial_certs.xlsx")


##------------STEP 7: FILTER TO TITLE II COHORT---------------------------------------

##subset only title ii cohort
cohort <- subset(cohort, cohort$initial_cert == "yes")

##check if anyone who was only in the fall & did not complete
fallonly <- subset(cohort, !is.na(cohort$ft_pt_2490)  & is.na(cohort$ft_pt_2520)  & is.na(cohort$ft_pt_2560) & cohort$GRAD_STATUS =="NOT")

#remove people who were only in the fall & did not complete 
cohort <- anti_join(cohort, fallonly, by = "id")

write_xlsx(cohort, "step_7_title_ii_cohort_filter.xlsx")

##clean up workspace
rm(fallonly)

##manually check that there isn't anyone  left who didn't finish the year in TED
##or at least graduate with a TED degree
#double check for any dupes too 
##and check double majors - found 2 who were added to cohort

#-------STEP 8: Title ii Data Elements- SSN5, PROGRAM TYPE, REPORTING GROUP, PROGRAM, COURSE LEVEL -----------------------------------------
##columns needed for final worksheet:
## ssn (last 5 digits), last name, first name, mi, DOB (mm/dd/yy)
##program type, reporting group, code 1, cip 1, degree 1 (& 2 & 3)
##years to degree, enrollment status, program level, gender, 
#ethnicity, race, program code

#re-load load data after manual cleaning & adding any TED second majors etc. 
df <-read.csv("step_7_title_ii_cohort_filter_20260127.csv",header=TRUE)

#remove blank col
df$X <- NULL

#make ssn column character columns 
df$ssn <- as.character(df$ssn)

##create column for ssn to last 5 characters
df$ssn5 <- substr(df$ssn, nchar(df$ssn) - 4, nchar(df$ssn))

##add X to start of ssn column so that it doesn't get turned into an int. 
##and get any leading zeroes cut off when going back and forth our of R 
df$ssn5 <- paste0("X", df$ssn5)

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
df <- df %>%
  mutate(program_new =
           case_when(
             GRAD_STATUS == "NOT" & df$program_2560 != "" ~ df$program_2560,
             GRAD_STATUS == "NOT" & df$program_2560 == "" ~ df$program_2520,
             GRAD_STATUS == "GRADUATED" ~ df$grad_program,
             TRUE ~ "CHECK"
           ))

##create new column to use for relevant course level
df <- df %>%
  mutate(course_level_new =
           case_when(
             substr(program_new, 1, 1) == "B" ~ "UG",
             substr(program_new, 1, 1) == "M" ~ "GR",
             TRUE ~ "CHECK"
           ))

#write to excel to check
write_xlsx(df, "step_8_check_program_course_level.xlsx")


#-------STEP 9: Title ii Data Elements- PROGRAM CIPS -----------------------------------------

##code programs to code 1 & 2 
df <- df %>%
  mutate(code_1 =  
           case_when(
             df$grad_program == "BA_SST" ~ "5110",
             df$grad_program == "BA_SST_ANT" ~ "5110",
             df$grad_program == "BA_SST_ECO" ~ "5110",
             df$grad_program == "BA_SST_GRY" ~ "5110",
             df$grad_program == "BA_SST_HIS" ~ "5110",
             df$grad_program == "BA_SST_POL" ~ "5110",
             df$grad_program == "BA_SST_SOC" ~ "5110",
             df$grad_program == "BS_ACM" ~ "5030",
             df$grad_program == "BS_AES" ~ "5070",
             df$grad_program == "BA_AFS" ~ "5140",
             df$grad_program == "MAT_ACH" ~ "5030",
             df$grad_program == "BS_ABI" ~ "5010",
             df$grad_program == "MAT_ABI" ~ "5010",
             df$grad_program == "BA_AEN" ~ "5013",
             df$grad_program == "MAT_AEN" ~ "5013",
             df$grad_program == "BA_AFR" ~ "5140",
             df$grad_program == "BA_AEM" ~ "5130",
             df$grad_program == "BS_AEM" ~ "5130",
             df$grad_program == "BS_APH" ~ "5050",
             df$grad_program == "MAT_APH" ~ "5050",  
             df$grad_program == "BS_APM" ~ "5050",
             df$grad_program == "BA_ASP" ~ "5150",
             df$grad_program == "BS_ECD" ~ "3013",
             df$grad_program == "BS_ECD_ELA" ~ "3013",
             df$grad_program == "BS_ECD_EST" ~ "3013",
             df$grad_program == "BS_ECD_HUM" ~ "3013",
             df$grad_program == "BS_ECD_MAT" ~ "3013",
             df$grad_program == "BS_ECD_SOS" ~ "3013",
             df$grad_program == "BS_ECD_UST" ~ "3013",
             df$grad_program == "MST_CHD" ~ "3014",
             df$grad_program == "MS_CSD" ~ "9021",
             df$grad_program == "MS_CSD_CERT" ~ "9021",
             df$grad_program == "MST_HEA_NCRT" ~ "6121",
             df$grad_program == "BSED_HEC" ~ "6121",
             df$grad_program == "BSED_HEC_CHP" ~ "6121",
             df$grad_program == "BSED_HEC_WEL" ~ "6121",
             df$grad_program == "BS_ECI" ~ "3013",
             df$grad_program == "BS_ECI_ELEI" ~ "3013",
             df$grad_program == "BS_ECI_ESEI" ~ "3013",
             df$grad_program == "BS_ECI_HMEI" ~ "3013",
             df$grad_program == "BS_ECI_MTEI" ~ "3013",
             df$grad_program == "BS_ECI_SSCH" ~ "3013",
             df$grad_program == "BS_ECI_SSEI" ~ "3013",
             df$grad_program == "BS_IEC" ~ "9014",
             df$grad_program == "BS_IEC_ELA" ~ "9014",
             df$grad_program == "BS_IEC_EST" ~ "9014",
             df$grad_program == "BS_IEC_HUM" ~ "9014",
             df$grad_program == "BS_IEC_MAT" ~ "9014",
             df$grad_program == "BS_IEC_SOS" ~ "9014",
             df$grad_program == "BSED_PEM" ~ "6160",
             df$grad_program == "BSED_PEM_ADP" ~ "6160",
             df$grad_program == "BSED_PEM_OAE" ~ "6160",
             df$grad_program == "MST_PHE" ~ "6160",
             df$grad_program == "MST_PHE_PENC" ~ "6160",
             df$grad_program == "BA_ESL_CERT" ~ "7080",
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
    df$grad_program == "BA_AFS" ~ "5150",
    df$grad_program == "BS_APM" ~ "5130",
    df$grad_program == "BS_ECD" ~ "3014",
    df$grad_program == "BS_ECD_ELA" ~ "3014",
    df$grad_program == "BS_ECD_EST" ~ "3014",
    df$grad_program == "BS_ECD_HUM" ~ "3014",
    df$grad_program == "BS_ECD_MAT" ~ "3014",
    df$grad_program == "BS_ECD_SOS" ~ "3014",
    df$grad_program == "BS_ECD_UST" ~ "3014",
    df$grad_program == "BS_ECI" ~ "0126",
    df$grad_program == "BS_ECI_ELEI" ~ "0126",
    df$grad_program == "BS_ECI_ESEI" ~ "0126",
    df$grad_program == "BS_ECI_HMEI" ~ "0126",
    df$grad_program == "BS_ECI_MTEI" ~ "0126",
    df$grad_program == "BS_ECI_SSCH" ~ "0126",
    df$grad_program == "BS_ECI_SSEI" ~ "0126",
    df$grad_program == "BS_IEC" ~ "3014",
    df$grad_program == "BS_IEC_ELA" ~ "3014",
    df$grad_program == "BS_IEC_EST" ~ "3014",
    df$grad_program == "BS_IEC_HUM" ~ "3014",
    df$grad_program == "BS_IEC_MAT" ~ "3014",
    df$grad_program == "BS_IEC_SOS" ~ "3014",
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

##code programs to cip codes 1 & 2 
df <- df %>%
  mutate(cip_code_1 =  case_when(
    df$grad_program == "BA_SST" ~ "13.1318",
    df$grad_program == "BA_SST_ANT" ~ "13.1318",
    df$grad_program == "BA_SST_ECO" ~ "13.1318",
    df$grad_program == "BA_SST_GRY" ~ "13.1318",
    df$grad_program == "BA_SST_HIS" ~ "13.1318",
    df$grad_program == "BA_SST_POL" ~ "13.1318",
    df$grad_program == "BA_SST_SOC" ~ "13.1318",
    df$grad_program == "BS_ACM" ~ "13.1323",
    df$grad_program == "BS_AES" ~ "13.1337",
    df$grad_program == "BA_AFS" ~ "13.1306",
    df$grad_program == "MAT_ACH" ~ "13.1323",
    df$grad_program == "BS_ABI" ~ "13.1322",
    df$grad_program == "MAT_ABI" ~ "13.1322",
    df$grad_program == "BA_AEN" ~ "13.1305",
    df$grad_program == "MAT_AEN" ~ "13.1305",
    df$grad_program == "BA_AFR" ~ "13.1306",
    df$grad_program == "BA_AEM" ~ "13.1311",
    df$grad_program == "BS_AEM" ~ "13.1311",
    df$grad_program == "BS_APH" ~ "13.1329",
    df$grad_program == "MAT_APH" ~ "13.1329",  
    df$grad_program == "BS_APM" ~ "13.1329",
    df$grad_program == "BA_ASP" ~ "13.1306",
    df$grad_program == "BS_ECD" ~ "13.121",
    df$grad_program == "BS_ECD_ELA" ~ "13.121",
    df$grad_program == "BS_ECD_EST" ~ "13.121",
    df$grad_program == "BS_ECD_HUM" ~ "13.121",
    df$grad_program == "BS_ECD_MAT" ~ "13.121",
    df$grad_program == "BS_ECD_SOS" ~ "13.121",
    df$grad_program == "BS_ECD_UST" ~ "13.121",
    df$grad_program == "MST_CHD" ~ "13.1202",
    df$grad_program == "MS_CSD" ~ "13.1331",
    df$grad_program == "MS_CSD_CERT" ~ "13.1331",
    df$grad_program == "MST_HEA_NCRT" ~ "13.1307",
    df$grad_program == "BSED_HEC" ~ "13.1307",
    df$grad_program == "BSED_HEC_CHP" ~ "13.1307",
    df$grad_program == "BSED_HEC_WEL" ~ "13.1307",
    df$grad_program == "BS_ECI" ~ "13.121",
    df$grad_program == "BS_ECI_ELEI" ~ "13.121",
    df$grad_program == "BS_ECI_ESEI" ~ "13.121",
    df$grad_program == "BS_ECI_HMEI" ~ "13.121",
    df$grad_program == "BS_ECI_MTEI" ~ "13.121",
    df$grad_program == "BS_ECI_SSCH" ~ "13.121",
    df$grad_program == "BS_ECI_SSEI" ~ "13.121",
    df$grad_program == "BS_IEC" ~ "13.1",
    df$grad_program == "BS_IEC_ELA" ~ "13.1",
    df$grad_program == "BS_IEC_EST" ~ "13.1",
    df$grad_program == "BS_IEC_HUM" ~ "13.1",
    df$grad_program == "BS_IEC_MAT" ~ "13.1",
    df$grad_program == "BS_IEC_SOS" ~ "13.1",
    df$grad_program == "BSED_PEM" ~ "13.1314",
    df$grad_program == "BSED_PEM_ADP" ~ "13.1314",
    df$grad_program == "BSED_PEM_OAE" ~ "13.1314",
    df$grad_program == "MST_PHE" ~ "13.1314",
    df$grad_program == "MST_PHE_PENC" ~ "13.1314",
    df$grad_program == "BA_ESL_CERT" ~ "13.14",
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
    df$grad_program == "BA_AFS" ~ "13.1306",
    df$grad_program == "BS_APM" ~ "13.1311",
    df$grad_program == "BS_ECD" ~ "13.1202",
    df$grad_program == "BS_ECD_ELA" ~ "13.1202",
    df$grad_program == "BS_ECD_EST" ~ "13.1202",
    df$grad_program == "BS_ECD_HUM" ~ "13.1202",
    df$grad_program == "BS_ECD_MAT" ~ "13.1202",
    df$grad_program == "BS_ECD_SOS" ~ "13.1202",
    df$grad_program == "BS_ECD_UST" ~ "13.1202",
    df$grad_program == "BS_ECI" ~ "13.1",
    df$grad_program == "BS_ECI_ELEI" ~ "13.1",
    df$grad_program == "BS_ECI_ESEI" ~ "13.1",
    df$grad_program == "BS_ECI_HMEI" ~ "13.1",
    df$grad_program == "BS_ECI_MTEI" ~ "13.1",
    df$grad_program == "BS_ECI_SSCH" ~ "13.1",
    df$grad_program == "BS_ECI_SSEI" ~ "13.1",
    df$grad_program == "BS_IEC" ~ "13.1202",
    df$grad_program == "BS_IEC_ELA" ~ "13.1202",
    df$grad_program == "BS_IEC_EST" ~ "13.1202",
    df$grad_program == "BS_IEC_HUM" ~ "13.1202",
    df$grad_program == "BS_IEC_MAT" ~ "13.1202",
    df$grad_program == "BS_IEC_SOS" ~ "13.1202",
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
    df$grad_program == "BA_SST" ~ "B",
    df$grad_program == "BA_SST_ANT" ~ "B",
    df$grad_program == "BA_SST_ECO" ~ "B",
    df$grad_program == "BA_SST_GRY" ~ "B",
    df$grad_program == "BA_SST_HIS" ~ "B",
    df$grad_program == "BA_SST_POL" ~ "B",
    df$grad_program == "BA_SST_SOC" ~ "B",
    df$grad_program == "BS_ACM" ~ "B",
    df$grad_program == "BS_AES" ~ "B",
    df$grad_program == "BA_AFS" ~ "B",
    df$grad_program == "MAT_ACH" ~ "M",
    df$grad_program == "BS_ABI" ~ "B",
    df$grad_program == "MAT_ABI" ~ "M",
    df$grad_program == "BA_AEN" ~ "B",
    df$grad_program == "MAT_AEN" ~ "M",
    df$grad_program == "BA_AFR" ~ "B",
    df$grad_program == "BA_AEM" ~ "B",
    df$grad_program == "BS_AEM" ~ "B",
    df$grad_program == "BS_APH" ~ "B",
    df$grad_program == "MAT_APH" ~ "M",  
    df$grad_program == "BS_APM" ~ "B",
    df$grad_program == "BA_ASP" ~ "B",
    df$grad_program == "BS_ECD" ~ "B",
    df$grad_program == "BS_ECD_ELA" ~ "B",
    df$grad_program == "BS_ECD_EST" ~ "B",
    df$grad_program == "BS_ECD_HUM" ~ "B",
    df$grad_program == "BS_ECD_MAT" ~ "B",
    df$grad_program == "BS_ECD_SOS" ~ "B",
    df$grad_program == "BS_ECD_UST" ~ "B",
    df$grad_program == "MST_CHD" ~ "M",
    df$grad_program == "MS_CSD" ~ "M",
    df$grad_program == "MS_CSD_CERT" ~ "M",
    df$grad_program == "MST_HEA_NCRT" ~ "M",
    df$grad_program == "BSED_HEC" ~ "B",
    df$grad_program == "BSED_HEC_CHP" ~ "B",
    df$grad_program == "BSED_HEC_WEL" ~ "B",
    df$grad_program == "BS_ECI" ~ "B",
    df$grad_program == "BS_ECI_ELEI" ~ "B",
    df$grad_program == "BS_ECI_ESEI" ~ "B",
    df$grad_program == "BS_ECI_HMEI" ~ "B",
    df$grad_program == "BS_ECI_MTEI" ~ "B",
    df$grad_program == "BS_ECI_SSCH" ~ "B",
    df$grad_program == "BS_ECI_SSEI" ~ "B",
    df$grad_program == "BS_IEC" ~ "B",
    df$grad_program == "BS_IEC_ELA" ~ "B",
    df$grad_program == "BS_IEC_EST" ~ "B",
    df$grad_program == "BS_IEC_HUM" ~ "B",
    df$grad_program == "BS_IEC_MAT" ~ "B",
    df$grad_program == "BS_IEC_SOS" ~ "B",
    df$grad_program == "BSED_PEM" ~ "B",
    df$grad_program == "BSED_PEM_ADP" ~ "B",
    df$grad_program == "BSED_PEM_OAE" ~ "B",
    df$grad_program == "MST_PHE" ~ "M",
    df$grad_program == "MST_PHE_PENC" ~ "M",
    df$grad_program == "BA_ESL_CERT" ~ "B",
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
    df$grad_program == "BA_AFS" ~ "B",
    df$grad_program == "BS_APM" ~ "B",
    df$grad_program == "BS_ECD" ~ "B",
    df$grad_program == "BS_ECD_ELA" ~ "B",
    df$grad_program == "BS_ECD_EST" ~ "B",
    df$grad_program == "BS_ECD_HUM" ~ "B",
    df$grad_program == "BS_ECD_MAT" ~ "B",
    df$grad_program == "BS_ECD_SOS" ~ "B",
    df$grad_program == "BS_ECD_UST" ~ "B",
    df$grad_program == "BS_ECI" ~ "B",
    df$grad_program == "BS_ECI_ELEI" ~ "B",
    df$grad_program == "BS_ECI_ESEI" ~ "B",
    df$grad_program == "BS_ECI_HMEI" ~ "B",
    df$grad_program == "BS_ECI_MTEI" ~ "B",
    df$grad_program == "BS_ECI_SSCH" ~ "B",
    df$grad_program == "BS_ECI_SSEI" ~ "B",
    df$grad_program == "BS_IEC" ~ "B",
    df$grad_program == "BS_IEC_ELA" ~ "B",
    df$grad_program == "BS_IEC_EST" ~ "B",
    df$grad_program == "BS_IEC_HUM" ~ "B",
    df$grad_program == "BS_IEC_MAT" ~ "B",
    df$grad_program == "BS_IEC_SOS" ~ "B",
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
write_xlsx(df, "step_9_check_cip_section.xlsx")


#----------STEP 10: CODE ENROLLMENT STATUS, PROGRAM LEVEL, GENDER, ETHNICITY, RACE---------------------------------------
##enrollment status
cohort <- cohort %>%  
  mutate(enrollment_status =  case_when( 
    ft_pt_2490 == "FT" & ft_pt_2520 == "FT"  ~ "1" ,
    ft_pt_2490 == "PT" & ft_pt_2520 == "PT"  ~ "2",
    ft_pt_2490 == "FT" & ft_pt_2520 == "PT"  ~ "3",
    ft_pt_2490 == "PT" & ft_pt_2520 == "FT"  ~ "3",
    ft_pt_2490 == "FT" & ft_pt_2520 == ""  ~ "1" ,
    ft_pt_2490 == "PT" & ft_pt_2520 == ""  ~ "2",
    ft_pt_2490 == "" & ft_pt_2520 == "FT"  ~ "1" ,
    ft_pt_2490 == "" & ft_pt_2520 == "PT"  ~ "2",
    ft_pt_2490 == "" & ft_pt_2520 == "" & ft_pt_2560 == "FT" ~ "2",
    ft_pt_2490 == "" & ft_pt_2520 == ""  & ft_pt_2560 == "PT" ~ "2",
    TRUE ~ ""
  ))

##how to code students who completed but were not enrolled?
##leave blank if upload accepts that
##if upload does not accept that, then code as FT 

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
    df$ipeds_race == "Hispanic" ~ "1",
    df$ipeds_race == "Black or African American" ~ "2",
    df$ipeds_race == "Asian" ~ "2",
    df$ipeds_race == "American Indian or Alaskan Native" ~ "2",
    df$ipeds_race == "Native Hawaiian or other Pacific Islander" ~ "2",
    df$ipeds_race == "White" ~ "2",
    df$ipeds_race == "Two or more races" ~ "2",
    df$ipeds_race == "NR" ~ "3",
    df$ipeds_race == "Unknown" ~ "3",
    TRUE ~ "3"
  ))

##new column recoding race
##leave race blank if hispanic
##code NR/NRA as unknown (blank)
df <- df %>% 
  mutate(race_new =  case_when(
    df$ipeds_race == "Black or African American" ~ "1",
    df$ipeds_race == "Asian" ~ "2",
    df$ipeds_race == "American Indian or Alaskan Native" ~ "3",
    df$ipeds_race == "Native Hawaiian or other Pacific Islander" ~ "4",
    df$ipeds_race == "White" ~ "5",
    df$ipeds_race == "Two or more races" ~ "6",
    df$ipeds_race == "NR" ~ "",
    df$ipeds_race == "Unknown" ~ "",
    df$ipeds_race == "Hispanic" ~ "",
    TRUE ~ ""
  ))


#column for program codes
df <- df %>% 
  mutate(program_code =  case_when(
    df$grad_program == "BA_SST" ~ "22930",
    df$grad_program == "BA_SST_ANT" ~ "22930",
    df$grad_program == "BA_SST_ECO" ~ "22930",
    df$grad_program == "BA_SST_GRY" ~ "22930",
    df$grad_program == "BA_SST_HIS" ~ "22930",
    df$grad_program == "BA_SST_POL" ~ "22930",
    df$grad_program == "BA_SST_SOC" ~ "22930",
    df$grad_program == "BS_ACM" ~ "22922",
    df$grad_program == "BS_AES" ~ "22924",
    df$grad_program == "BA_AFS" ~ "30649",
    df$grad_program == "MAT_ACH" ~ "25108",
    df$grad_program == "BS_ABI" ~ "22920",
    df$grad_program == "MAT_ABI" ~ "25114",
    df$grad_program == "BA_AEN" ~ "22929",
    df$grad_program == "MAT_AEN" ~ "25106",
    df$grad_program == "BA_AFR" ~ "22932",
    df$grad_program == "BA_AEM" ~ "22918",
    df$grad_program == "BS_AEM" ~ "22919",
    df$grad_program == "BS_APH" ~ "22926",
    df$grad_program == "MAT_APH" ~ "25122",  
    df$grad_program == "BS_APM" ~ "23377",
    df$grad_program == "BA_ASP" ~ "22931",
    df$grad_program == "BS_ECD" ~ "23373",
    df$grad_program == "BS_ECD_ELA" ~ "23373",
    df$grad_program == "BS_ECD_EST" ~ "23373",
    df$grad_program == "BS_ECD_HUM" ~ "23373",
    df$grad_program == "BS_ECD_MAT" ~ "23373",
    df$grad_program == "BS_ECD_SOS" ~ "23373",
    df$grad_program == "BS_ECD_UST" ~ "23373",
    df$grad_program == "MST_CHD" ~ "22928",
    df$grad_program == "MS_CSD" ~ "33410",
    df$grad_program == "MS_CSD_CERT" ~ "33410",
    df$grad_program == "MST_HEA_NCRT" ~ "25112",
    df$grad_program == "BSED_HEC" ~ "23375",
    df$grad_program == "BSED_HEC_CHP" ~ "23375",
    df$grad_program == "BSED_HEC_WEL" ~ "23375",
    df$grad_program == "BS_ECI" ~ "23374",
    df$grad_program == "BS_ECI_ELEI" ~ "23374",
    df$grad_program == "BS_ECI_ESEI" ~ "23374",
    df$grad_program == "BS_ECI_HMEI" ~ "23374",
    df$grad_program == "BS_ECI_MTEI" ~ "23374",
    df$grad_program == "BS_ECI_SSCH" ~ "23374",
    df$grad_program == "BS_ECI_SSEI" ~ "23374",
    df$grad_program == "BS_IEC" ~ "36629",
    df$grad_program == "BS_IEC_ELA" ~ "36629",
    df$grad_program == "BS_IEC_EST" ~ "36629",
    df$grad_program == "BS_IEC_HUM" ~ "36629",
    df$grad_program == "BS_IEC_MAT" ~ "36629",
    df$grad_program == "BS_IEC_SOS" ~ "36629",
    df$grad_program == "BSED_PEM" ~ "23376",
    df$grad_program == "BSED_PEM_ADP" ~ "23376",
    df$grad_program == "BSED_PEM_OAE" ~ "23376",
    df$grad_program == "MST_PHE" ~ "39290",
    df$grad_program == "MST_PHE_PENC" ~ "39290",
    df$grad_program == "BA_ESL_CERT" ~ "29720",
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
write_xlsx(df, "step_10_crosswalking_title_ii_data_elements.xlsx")

#----------STEP 11: CALCULATE SEMESTERS ENROLLED---------------------------------------
##only count fall & spring
##only count enrolled semesters
##go back until HEH = 1 2, or 6 

##load ess data back 6 years
ess_1890 <-read.csv("siris_ess_201890_official.csv",header=TRUE)
ess_1920 <-read.csv("siris_ess_201920_0327_OFFICIAL.csv",header=TRUE)
ess_1990 <-read.csv("siris_ess_fall2019_official.csv",header=TRUE)
ess_2020 <-read.csv("siris_ess_sprg2020_official.csv",header=TRUE)
ess_2090 <-read.csv("siris_fall2020_ess_official.csv",header=TRUE)
ess_2120 <-read.csv("siris_sprg2021_ess_official.csv",header=TRUE)
ess_2190 <-read.csv("Fall2021ess_official.csv",header=TRUE)
ess_2220 <-read.csv("siris-sds-ess-202220-0401_official.csv",header=TRUE)
ess_2290 <-read.csv("SIRIS-SDS-202290ESS_official.csv",header=TRUE)
ess_2320 <-read.csv("siris-ess-202320-official.csv",header=TRUE)
ess_2390 <-read.csv("SIRIS-SDS-202390ESS_1101official.csv",header=TRUE)
ess_2420 <-read.csv("SIRIS202420ess_0401Official.csv",header=TRUE)

#clean ess
#make all ess columns lowercase
e_names <- ls(envir = .GlobalEnv)[ grepl("^ess_", ls(envir = .GlobalEnv)) ]
for (nm in e_names) {
  tmp <- get(nm, envir = .GlobalEnv)
  names(tmp) <- tolower(names(tmp))
  assign(nm, tmp, envir = .GlobalEnv)
}
rm(tmp)

#rename local_id and campus_id to id
for (nm in e_names) {
  tmp <- get(nm, envir = .GlobalEnv)
  
  #find which of the two old names exist
  rename_cols <- intersect(c("local_id", "campus_id"), names(tmp))
  
  #rename each to id
  for (old in rename_cols) {
    names(tmp)[names(tmp) == old] <- "id"
  }
  
  #write it back
  assign(nm, tmp, envir = .GlobalEnv)
}
rm(tmp)

#clean up column names and only pull needed columns 
select_ess_cols_fuzzy <- function(df) {
  #standard name -> regex for its variants
  patterns <- list(
    id             = "^id$",
    ssn             = "^ssn$",
    first_name      = "^first[_\\.]name$",
    last_name       = "^last[_\\.]name$",
    mi              = "^mi$",
    dob             = "^dob$",
    gender          = "^gender(?:$|\\W.*)$",
    ipeds_race      = "^ipeds(?:[_\\.-](race(?:_ethnicity)?|race_eth|race\\.ethnicity|ethnicity|raceth|raceeth|race(?:_eth)?))$",
    heh             = "^(higher[\\._]*ed[\\._]*(hist(ory)?)?|heh)$"
  )
  
  for (std_name in names(patterns)) {
    pat  <- patterns[[std_name]]
    cols <- names(df)
    
    #find all matches to the regex
    hits <- grep(pat, cols, ignore.case = TRUE, value = TRUE)
    #drop any that are already the standard name
    to_rename <- setdiff(hits, std_name)
    
    if (length(to_rename) > 0) {
      #rename the first unmatched variant
      df <- df %>% rename(!!std_name := !!sym(to_rename[1]))
    }
  }
  
  #select only the standardized column names that exist
  df %>% select(any_of(names(patterns)))
}

#apply it to every ess_
e_names <- ls(envir = .GlobalEnv)[ grepl("^ess_", ls(envir = .GlobalEnv)) ]

for (nm in e_names) {
  assign(
    nm,
    select_ess_cols_fuzzy(get(nm, envir = .GlobalEnv)),
    envir = .GlobalEnv
  )
}

#add term as suffix to columns before joining
for (nm in e_names) {
  df <- get(nm, inherits = TRUE)
  
  #extract the number that comes after ess_
  suffix <- sub("^ess_", "", nm)
  
  #columns that should NOT be renamed
  exclude <- c("id", "first_name", "last_name", "mi", "ssn", "dob", "gender", "ipeds_race")
  
  #determine which columns to rename
  rename_cols <- setdiff(names(df), exclude)
  
  #create the new names
  new_names <- names(df)
  new_names[names(df) %in% rename_cols] <- paste0(rename_cols, "_", suffix)
  
  #apply the new column names
  names(df) <- new_names
  
  #assign back to the environment
  assign(nm, df)
}

#join needed ess columns
cohort <- cohort %>%
  left_join(ess_1890, by = "id")%>%
  left_join(ess_1920, by = "id")%>%
  left_join(ess_1990, by = "id")%>%
  left_join(ess_2020, by = "id")%>%
  left_join(ess_2090, by = "id")%>%
  left_join(ess_2120, by = "id")%>%
  left_join(ess_2190, by = "id")%>%
  left_join(ess_2220, by = "id")%>%
  left_join(ess_2290, by = "id")%>%
  left_join(ess_2320, by = "id")%>%
  left_join(ess_2390, by = "id")%>%
  left_join(ess_2420, by = "id")


##move heh columns to be next to each other
cohort <- cohort %>% 
  relocate(heh_1920, .after = heh_1890)%>% 
  relocate(heh_1990, .after = heh_1920)%>% 
  relocate(heh_2020, .after = heh_1990)%>% 
  relocate(heh_2090, .after = heh_2020)%>% 
  relocate(heh_2120, .after = heh_2090)%>% 
  relocate(heh_2190, .after = heh_2120)%>% 
  relocate(heh_2220, .after = heh_2190)%>% 
  relocate(heh_2290, .after = heh_2220)%>% 
  relocate(heh_2320, .after = heh_2290)%>% 
  relocate(heh_2390, .after = heh_2320)%>%
  relocate(heh_2420, .after = heh_2390)%>%
  relocate(higher_ed_hist_2490, .after = heh_2420)%>%
  relocate(higher_ed_hist_2520, .after = higher_ed_hist_2490)
  
#collapse name, ssn, dob, gender, ipeds_race columns
cohort <- cohort %>%
  mutate(
    first_name_g = coalesce(first_name, first_name.y, first_name.x.x, first_name.y.y,
                            first_name.x.x.x, first_name.y.y.y,
                            first_name.x.x.x.x, first_name.y.y.y.y,
                            first_name.x.x.x.x.x,first_name.y.y.y.y.y,
                            first_name.x.x.x.x.x.x, first_name.y.y.y.y.y.y),
    last_name_g  = coalesce(last_name, last_name.y, last_name.x.x, last_name.y.y,
                            last_name.x.x.x, last_name.y.y.y,
                            last_name.x.x.x.x, last_name.y.y.y.y,
                            last_name.x.x.x.x.x,last_name.y.y.y.y.y,
                            last_name.x.x.x.x.x.x, last_name.y.y.y.y.y.y),
    mi_g  = coalesce(mi, mi.y, mi.x.x, mi.y.y,
                     mi.x.x.x, mi.y.y.y,
                     mi.x.x.x.x, mi.y.y.y.y,
                     mi.x.x.x.x.x,mi.y.y.y.y.y,
                     mi.x.x.x.x.x.x, mi.y.y.y.y.y.y),
    ssn_g  = coalesce(ssn.y, ssn.x.x, ssn.y.y,
                      ssn.x.x.x, ssn.y.y.y,
                      ssn.x.x.x.x, ssn.y.y.y.y,
                      ssn.x.x.x.x.x,ssn.y.y.y.y.y,
                      ssn.x.x.x.x.x.x, ssn.y.y.y.y.y.y),
    dob_g  = coalesce(dob, dob.y, dob.x.x, dob.y.y,
                      dob.x.x.x, dob.y.y.y,
                      dob.x.x.x.x, dob.y.y.y.y,
                      dob.x.x.x.x.x,dob.y.y.y.y.y,
                      dob.x.x.x.x.x.x, dob.y.y.y.y.y.y),
    gender_g  = coalesce(gender, gender.y, gender.x.x, gender.y.y,
                         gender.x.x.x, gender.y.y.y,
                         gender.x.x.x.x, gender.y.y.y.y,
                         gender.x.x.x.x.x,gender.y.y.y.y.y,
                         gender.x.x.x.x.x.x, gender.y.y.y.y.y.y),
    ipeds_race_g  = coalesce(ipeds_race, ipeds_race.y, ipeds_race.x.x, ipeds_race.y.y,
                             ipeds_race.x.x.x, ipeds_race.y.y.y,
                             ipeds_race.x.x.x.x, ipeds_race.y.y.y.y,
                             ipeds_race.x.x.x.x.x,ipeds_race.y.y.y.y.y,
                             ipeds_race.x.x.x.x.x.x, ipeds_race.y.y.y.y.y.y)
  ) %>%
  select(-first_name, -first_name.y, -first_name.x.x, -first_name.y.y,
         -first_name.x.x.x, -first_name.y.y.y, -first_name.x.x.x.x, -first_name.y.y.y.y,
         -first_name.x.x.x.x.x, -first_name.y.y.y.y.y, -first_name.x.x.x.x.x.x, -first_name.y.y.y.y.y.y,
         -last_name, -last_name.y, -last_name.x.x, -last_name.y.y,
         -last_name.x.x.x, -last_name.y.y.y, -last_name.x.x.x.x, -last_name.y.y.y.y,
         -last_name.x.x.x.x.x, -last_name.y.y.y.y.y, -last_name.x.x.x.x.x.x, -last_name.y.y.y.y.y.y,
         -mi, -mi.y, -mi.x.x, -mi.y.y,
         -mi.x.x.x, -mi.y.y.y, -mi.x.x.x.x, -mi.y.y.y.y,
         -mi.x.x.x.x.x,-mi.y.y.y.y.y, -mi.x.x.x.x.x.x, -mi.y.y.y.y.y.y,
          -ssn.y, -ssn.x.x, -ssn.y.y,
         -ssn.x.x.x, -ssn.y.y.y, -ssn.x.x.x.x, -ssn.y.y.y.y,
         -ssn.x.x.x.x.x,-ssn.y.y.y.y.y, -ssn.x.x.x.x.x.x, -ssn.y.y.y.y.y.y,
         -dob, -dob.y, -dob.x.x, -dob.y.y,
         -dob.x.x.x, -dob.y.y.y, -dob.x.x.x.x, -dob.y.y.y.y,
         -dob.x.x.x.x.x,-dob.y.y.y.y.y, -dob.x.x.x.x.x.x, -dob.y.y.y.y.y.y,
         -gender, -gender.y, -gender.x.x, -gender.y.y,
         -gender.x.x.x, -gender.y.y.y, -gender.x.x.x.x, -gender.y.y.y.y,
         -gender.x.x.x.x.x,-gender.y.y.y.y.y, -gender.x.x.x.x.x.x, -gender.y.y.y.y.y.y,
         -ipeds_race, -ipeds_race.y, -ipeds_race.x.x, -ipeds_race.y.y,
         -ipeds_race.x.x.x, -ipeds_race.y.y.y, -ipeds_race.x.x.x.x, -ipeds_race.y.y.y.y,
         -ipeds_race.x.x.x.x.x,-ipeds_race.y.y.y.y.y, -ipeds_race.x.x.x.x.x.x, -ipeds_race.y.y.y.y.y.y
  )

cohort <- cohort %>% rename(
  ssn = ssn.x,
  first_name = first_name.x,
  mi = mi.x,
  last_name = last_name.x,
  dob = dob.x,
  gender = gender.x,
  ipeds_race = ipeds_race.x
)

#clean up workspace
rm(ess_1890, ess_1920, ess_1990, ess_2020,
   ess_2090, ess_2120, ess_2190, ess_2220, ess_2290, ess_2320, 
   ess_2390, ess_2420 ,df)
rm(e_names, exclude, initial_cert_codes, new_names, nm, old, rename_cols,
   suffix, ted_codes)
rm(select_ess_cols_fuzzy)

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
enrollment_cols <- c("heh_1890", "heh_1920", "heh_1990",
                     "heh_2020", "heh_2090", "heh_2120", "heh_2190", "heh_2220", 
                     "heh_2290", "heh_2320", "heh_2390", "heh_2420", 
                     "higher_ed_hist_2490", "higher_ed_hist_2520")

#make sure needed columns are in data
enrollment_cols <- enrollment_cols[enrollment_cols %in% names(cohort)]

##create function to count by the rules above 
calculate_semesters_enrolled_count <- function(
    
  course_level_new, enrollment_data) {
  
  enrollment_values <- rev(enrollment_data)
  
  if (course_level_new == "UG") {
    start_vals <- c(1, 2)
    count_val <- 4
  } else if (course_level_new == "GR") {
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
cohort <- cohort %>%
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
cohort <- cohort %>% 
  relocate(semesters_enrolled_count, .after = higher_ed_hist_2520)


write_xlsx(cohort, "step_11_check_semesters_enrolled_count.xlsx")

##check that these calculated correctly
#manually fill/clean odd cases and add notes
#add x to keep leading 0 on any relevant codes
#backfill info for completers but not enrolled if relevant 

##if admit term is most recent summer (202560 in this case) - count 1 semester enrolled
##if admit term is most recent summer (202560 in this case) - looks like counted 1 YTD last year 

#----------STEP 12: CALCULATE YEARS TO DEGREE---------------------------------------

#re-load cleaned data
cohort <-read.csv("step_11_check_semesters_enrolled_count_20260127.csv",header=TRUE)


##add column to translate semesters attended to years to degree
cohort <- cohort %>% 
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
cohort <- cohort %>% 
  relocate(years_to_degree, .after = semesters_enrolled_count)

#write to excel to check
write_xlsx(cohort, "step_12_check_years_to_degree_conversion.xlsx")

cohort$X <- NULL
cohort$X.1 <- NULL
cohort$X.2 <- NULL
cohort$X.3 <- NULL
cohort$X.4 <- NULL
cohort$X.5 <- NULL
cohort$X.6 <- NULL
cohort$X.7 <- NULL
cohort$X.8 <- NULL

#----------STEP 13: FORMAT/ALIGN TO TEMPLATE---------------------------------------

#re-load cleaned data
cohort <-read.csv("title_ii_workfile_w_notes.csv",header=TRUE)

##create blank columns as placeholders so things will line up correctly
cohort$code_3 <- NA
cohort$cip_code_3 <- NA
cohort$degree_new_3 <- NA
cohort$code_4 <- NA
cohort$cip_code_4 <- NA
cohort$degree_new_4 <- NA
cohort$program_start_date <- cohort$admit_term
cohort$date_of_program_completion <- cohort$GRAD_DATE

##select only needed columns in order matching title ii data collection worksheet (& id) 
cohort <- cohort[, c( "id", "ssn5" , "last_name" , "first_name", "mi", "dob",
              "program_type", "reporting_group", "code_1", "cip_code_1", "degree_new_1",
              "code_2", "cip_code_2", "degree_new_2", "code_3" , "cip_code_3", "degree_new_3",
              "code_4", "cip_code_4", "degree_new_4", "years_to_degree", "enrollment_status",
              "program_level", "gender_new", "ethnicity_new", "race_new", 
              "program_start_date" , "date_of_program_completion" , "program_code")]

#write to excel to check
write_xlsx(cohort, "title_ii_draft_20260128.xlsx")

###will still need to crosswalk admit term to start date
##use the following per Stuart:
##Fall = 9/1
##Winter = 1/1
##Spring = 2/1
##Summer = 6/1 





#re-load cleaned data
cohort <-read.csv("title_ii_draft_20260202.csv",header=TRUE)

##crosswalking admit term to start date:

cohort$admit_term <- cohort$program_start_date

cohort <- cohort %>%
  mutate(
    year = substr(admit_term, 1, 4),
    term = substr(admit_term, 5, 6),
    start_date = as.Date(
      paste0(
        case_when(
          term == "90" ~ "09/01/",
          term == "20" ~ "02/01/",
          term == "10" ~ "01/01/",
          term == "60" ~ "06/01/",
          TRUE ~ NA_character_
        ),
        year
      ),
      format = "%m/%d/%Y"
    )
  ) %>%
  select(-year, -term)

cohort$program_start_date <- format(cohort$start_date, "%m/%d/%Y")

cohort$admit_term <- NULL
cohort$start_date <- NULL

#write to excel to check
write_xlsx(cohort, "title_ii_draft_20260202.xlsx")

##may need to add anticipated completion date for enrollees 
##Stuart submitted ticket to Ray on 1/28 to see if we can get from Banner
##going to try to upload with it blank for non-completers

##final clean-up that will be needed:
##make sure the T for traditional in program type doesn't get changed to logical (TRUE)
##change back if it does 
##get rid of the leading Xs in ssn5 & the one program 
##there to force character type so csv doesn't cut leading 0s 
##do this cleanup last thing  before submitting 



