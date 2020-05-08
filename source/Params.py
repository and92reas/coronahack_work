from . import *

class Params:
    
    PATIENT_FILE_LOCATION = "projection.json"
    
    PATIENT_FILE_LOCATION_NEW = "External Data/patient_info.csv"
    
    PATIENT_ROUTES_FILE_LOCATION = "External Data/patientRoutes.csv"
    
    CASE_FILE_LOCATION = "External Data/Case.csv"
    
    REGION_FILE_LOCATION = "External Data/Region.csv"
    
    SEARCH_TREND_FILE_LOCATION = "External Data/SearchTrend.csv"
    
    TIME_FILE_LOCATION = "External Data/Time.csv"
    
    TIME_AGE_FILE_LOCATION = "External Data/TimeAge.csv"
    
    TIME_GENDER_FILE_LOCATION = "External Data/TimeGender.csv"
    
    TIME_PROVINCE_FILE_LOCATION = "External Data/TimeProvince.csv"
    
    GRAPH_DATA_FILE_LOCATION = "External Data/graphMetricsInfectionProximity.pkl"
    
    SAVED_FILES_FOLDER = "Saved Data/"
    
    MOST_RECENT_DATE_RECORDED = datetime.datetime(2020, 4, 13)
    
    CURRENT_YEAR = 2020
    
    CITY = "city"
    PROVINCE = "province"
    AGE = "age"
    SEX = "sex"
    PATIENT_ID = "patient_id"
    INFECTOR_ID = "infector_id"
    CONFIRMED_DATE = "comfirmed_date"
    STATE = "state"
    DEATH_DATE = "death_date"
    RELEASED_DATE = "released_date"
    ADMISSION_DATE = "admission_date"
    SYMPTOM_ONSET_DATE = "symptom_onset_date"
    OTHER_DISEASE = "other_disease"
    INFECTION_CASE = "infection_case"
    NUMBER_OF_CONTACTS = "number_of_contacts"
    DAYS_BETWEEN_SYMPTOMS_AND_ADMISSION = "days_between_symptoms_and_admissions"
    INFECTOR_AGE = "infector_age"
    INFECTOR_SEX = "infector_sex"
    
    REGION_COLUMNS_USED = ["elementary_school_count",
                           "kindergarten_count",
                           "university_count",
                           "academy_ratio",
                           "elderly_population_ratio",
                           "elderly_alone_ratio",
                           "nursing_home_count"
                          ]
    
    GRAPH_COLUMNS_TO_BE_USED = [#'infectionDC',
                                #'infectionCC',
                                #'infectionBC',
                                #'infectionSPL',
                                #'infectionDeg',
                                'proximityDC',
                                #'proximityCC',
                                #'proximityBC',
                                #'proximitySPL',
                                #'proximityDeg',
                                'trafficDC',
                                #'trafficCC',
                                #'trafficBC',
                                #'trafficSPL',
                                #'trafficDeg'
                                ]
    
    INFECTOR_COLUMNS_USED = [
                            AGE,
                            SEX
                            ]
    
    SEVERE_CASES_DAY_THRES = 40
    
    SEVERE = "severe"
    MILD = "mild"
    
    
    COLUMNS_NOT_USED_FOR_MODELLING = [
                                      'patient_id',
                                      'province',
                                      'city',
                                      'other_disease',
                                      'infector_id',
                                      'comfirmed_date',
                                      'released_date',
                                      'death_date',
                                      'symptom_onset_date',
                                      'number_of_contacts',
                                      'admission_date'
                                      ]
    
    
    COLUMN_RENAME_DICT = {
        "elementary_school_count" : "elementary_school_count_in_city",
         "kindergarten_count" : "kindergarten_count_in_city",
         "university_count" : "university_count_in_city",
         "academy_ratio" : "academy_ratio_in_city",
          "elderly_population_ratio" : "elderly_population_ratio_in_city",
         "elderly_alone_ratio" : "elderly_alone_ratio_in_city",
         "nursing_home_count" : "nursing_home_count_in_city",
    }
    
    CATEG_COL_TO_PREFIX = {
        INFECTION_CASE : "INFECTION_LOCATION_",
        SEX : "SEX_",
        #INFECTOR_AGE: "INF_AGE_",
        #INFECTOR_SEX: "INF_SEX_",
        #DAYS_BETWEEN_SYMPTOMS_AND_ADMISSION: "ADM_SYMPT_DIFF_",
    }
    
    
    RANDOM_STATE = 2020
    
    TEST_PERC = 0.2
    
    CV_SPLITS = 5
    
    
    RFC_N_ESTIMATORS = 500
    RFC_CRITERION = "gini"
    RFC_MAX_DEPTH = 11
    
    
    
