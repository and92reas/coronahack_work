from . import *

class Processing:
    
    def json_to_df(file_location = Params.PATIENT_FILE_LOCATION):
        '''
        returns a pandas dataframe containing the information in the South Korean dataset
        *file_location*: the location of the file containing the corona information
        '''
        def update_df_dict(df_dict, subject):
            '''
            returns the dataframe dictionary updated with the information of a certain subject
            *df_dict*: dictionary of the form (col_name: list of values) 
            *subject*: dictionary containining the information of one particular subject 
            '''
            df_dict[Params.CITY].append(subject["entityTypeAttributes"]["City"]["name"] if "City" in subject["entityTypeAttributes"].keys() else None)
            
            df_dict[Params.PROVINCE].append(subject["entityTypeAttributes"]["Province"]["name"] if "Province" in subject["entityTypeAttributes"].keys() else None)
            
            if "Birth_year" in subject["entityTypeAttributes"].keys():
                 df_dict[Params.AGE].append((Params.CURRENT_YEAR - subject["entityTypeAttributes"]["Birth_year"]) if subject["entityTypeAttributes"]["Birth_year"] != None else None)
            else:
                df_dict[Params.AGE].append(None)
                
            df_dict[Params.SEX].append(subject["entityTypeAttributes"]["Sex"]["name"] if "Sex" in subject["entityTypeAttributes"].keys() else None)
            
            df_dict[Params.PATIENT_ID].append(str(subject["entityTypeAttributes"]["Patient_Id"]) if "Patient_Id" in subject["entityTypeAttributes"].keys() else None)
            
            df_dict[Params.INFECTOR_ID].append(str(subject["entityTypeAttributes"]["Infected_by_patient"]) if "Infected_by_patient" in subject["entityTypeAttributes"].keys() else None)
            
            if "State" in subject["episodes"][0]["entityTypeAttributes"].keys():
                df_dict[Params.STATE_DATE].append(subject["episodes"][0]["entityTypeAttributes"]["State"]["timestamp"] if "timestamp" in subject["episodes"][0]["entityTypeAttributes"]["State"].keys() else None)
                df_dict[Params.STATE].append(subject["episodes"][0]["entityTypeAttributes"]["State"]["name"] if "name" in subject["episodes"][0]["entityTypeAttributes"]["State"].keys() else None)
            else:
                df_dict[Params.STATE_DATE].append(None)
                df_dict[Params.STATE].append(None)
            
            df_dict[Params.DEATH_DATE].append(subject["episodes"][0]["entityTypeAttributes"]["Deceased_date"] if "Deceased_date" in subject["episodes"][0]["entityTypeAttributes"].keys() else None)
            
            df_dict[Params.RELEASED_DATE].append(subject["episodes"][0]["entityTypeAttributes"]["Release_date"] if "Deceased_date" in subject["episodes"][0]["entityTypeAttributes"].keys() else None)
            return df_dict
        
        with open(file_location) as f:
            sk_corona_data = json.load(f)
        subjects = sk_corona_data["subjects"]
        df_dict = reduce(lambda df_dict, subj: update_df_dict(df_dict, subj), subjects, {
                              Params.CITY : [],
                              Params.PROVINCE: [],
                              Params.AGE: [],
                              Params.SEX: [],
                              Params.PATIENT_ID : [],
                              Params.INFECTOR_ID : [],
                              Params.STATE_DATE: [],
                              Params.STATE: [],
                              Params.DEATH_DATE: [],
                              Params.RELEASED_DATE: []
                               })
        df = pd.DataFrame(df_dict)
        return df
    
    
    def discard_missing_values_of_columns(data, column_list):
        '''
        returns the pandas dataframe without the records corresponding to missing values for the specified columns
        *data*: pandas dataframe
        *column_list*: list of the columns whose missing values are going to be discarded
        '''
        def discard_missing_values_for_col(data, col):
            '''
            returns the pandas dataframe without the missing values of a particular column
            *data*: pandas dataframe
            *col*: thec column of interest
            '''
            data = data.dropna(subset = [col])
            data = data[data[col] != "None"]
            return data
        data = reduce(lambda data, col: discard_missing_values_for_col(data, col), column_list, data)
        return data
    
    
    def convert_column_to_datetime(date_series):
        '''
        returns a pandas series containing the date column converted to datetime
        *date_series*: the pandas series containing the date information as a string
        '''
        
        return pd.to_datetime(date_series, errors = "coerce").dt.to_pydatetime()
    
    
    def get_patient_to_hospital_admission_df(hospital_routes):
        '''
        returns a pandas dataframe containing the hospital admission days per patient
        *hospital_routes*: pandas dataframe containing all the routes that involve a hospital per patient
        '''
        hospital_routes = hospital_routes.groupby(Params.PATIENT_ID)[["date"]].max()
        hospital_routes[Params.PATIENT_ID] = hospital_routes.index.astype(str)
        hospital_routes.columns = [Params.ADMISSION_DATE, Params.PATIENT_ID]
        return hospital_routes.rename_axis(None)
    
    
    def enhance_patient_info_with_admission_date_info(patient_data, patient_routes):
        '''
        returns the dataframe containing the patient information also containing the admission date for each of the patients
        *patient_data*: pandas dataframe containing the patient information
        *patient_routes*: pandas dataframe containing the patient routes information
        '''
        patient_routes["date"] = Processing.convert_column_to_datetime(patient_routes["date"])
        hospital_routes = patient_routes[patient_routes["type"] == "hospital"]
        hospital_routes = Processing.get_patient_to_hospital_admission_df(hospital_routes)
        joined_data = pd.merge(patient_data, hospital_routes, how = "left", on = Params.PATIENT_ID)
        joined_data[Params.ADMISSION_DATE] = joined_data[Params.ADMISSION_DATE].fillna(joined_data[Params.CONFIRMED_DATE])
        return joined_data
    
    
    def group_infected_cases(data):
        '''
        returns the dataframe with the infector_case column being re-grouped accordingly
        *data*: pandas dataframe
        '''
        def modify_case_group(case):
            '''
            returns a mapping of a particular infection case
            *case*: the infection case of a particular record
            '''
            case = case.lower()
            if "hospital" in case:
                return "hospital"
            elif case == "contact with patient":
                return case
            #elif "church" in case:
                #return "church"
            #elif "gym" in case:
                #return "gym"
            elif "nursing home" in case:
                return "nursing_home"
            elif case == "overseas inflow":
                return case
            elif case == "unknown":
                return case
            else:
                return "other"
                
        data[Params.INFECTION_CASE] = data[Params.INFECTION_CASE].fillna("unknown")
        data[Params.INFECTION_CASE] = data[Params.INFECTION_CASE].apply(modify_case_group)
        return data
    
    
    def create_diff_between_symptoms_and_admission_feature(data):
        '''
        returns the pandas dataframe containing the difference_between_symptoms_and_admission feature
        *data*: pandas dataframe containing the patients information
        '''
        def generate_days_diff_groups(days):
            '''
            returns a mapping of the corresponding number of days to a certain group
            *days*: admission date - symptom_onset_date in days
            '''
            if np.isnan(days):
                return "unknown"
            elif days < 0:
                return "no_symptoms_at_admission"
            elif days <= 2:
                return "symptoms_1_to_2_days_before_admission"
            elif days <= 5:
                return "symptoms_3_to_5_days_before_admission"
            elif days <= 10:
                return "symptoms_6_to_10_days_before_admission"
            else:
                return "symptoms_more_than_10_days_before_admission"
            
        days_diff = (data[Params.ADMISSION_DATE] - data[Params.SYMPTOM_ONSET_DATE]).dt.days
        data[Params.DAYS_BETWEEN_SYMPTOMS_AND_ADMISSION] = days_diff.apply(generate_days_diff_groups)
        return data
    
    
    def join_and_proc_patient_data_with_region_data(patient_data, region_data, region_columns_used = Params.REGION_COLUMNS_USED):
        '''
        returns the pandas dataframe containing the joined and processed patient infomation
        *patient_data*: pandas dataframe containing the patient information
        *region_data*: pandas dataframe containing the region information
        *region_columns_used*: list containing the names of the columns used for the region dataset
        '''
        def fill_na_of_province_data(province_data):
            '''
            returns the dataframe with the missing values of the region-originating column filled with the mean
            *provinced_data* : tuple of the form (joined_patient data for particular province with missing values, region data about a particular province without the center of the province)
            '''
            patient_data, region_data = province_data
            patient_data[region_columns_used] = patient_data[region_columns_used].fillna(region_data.mean())
            return patient_data
            
            
        
        patient_data = patient_data.fillna({Params.CITY: patient_data[Params.PROVINCE]})
        region_data = region_data[[Params.CITY, Params.PROVINCE] + region_columns_used]
        patient_data = pd.merge(patient_data, region_data , how = "left", on = [Params.CITY, Params.PROVINCE])    
        
        data_with_null_values = patient_data[patient_data[region_columns_used[0]].isnull()]
        provinces_with_null = list(data_with_null_values.groupby(Params.PROVINCE).groups.keys())
        
        data_of_center_plus_provinces_without_null = patient_data[(patient_data[Params.CITY] == patient_data[Params.PROVINCE]) | (~patient_data[Params.PROVINCE].isin(provinces_with_null))]
        rest_data = patient_data[~(patient_data[Params.CITY] == patient_data[Params.PROVINCE]) | (~patient_data[Params.PROVINCE].isin(provinces_with_null))]
        province_data_list = list(map(lambda province: rest_data[rest_data[Params.PROVINCE] == province], provinces_with_null))
        region_data_list = list(map(lambda province: region_data[region_columns_used][(region_data[Params.PROVINCE] == province) & (region_data[Params.PROVINCE] != region_data[Params.CITY])], provinces_with_null))
        province_data_list = list(zip(province_data_list, region_data_list))
        filled_province_data = list(map(lambda province_data: fill_na_of_province_data(province_data), province_data_list))
        
        joined_data = pd.concat(filled_province_data + [data_of_center_plus_provinces_without_null])
        joined_data[region_columns_used] = joined_data[region_columns_used].fillna(region_data[region_data[Params.CITY] == "Jeju-do"][region_columns_used].mean())
        
        return joined_data
        
        
    def join_patient_data_with_infector_data(patient_data, infector_columns_used = Params.INFECTOR_COLUMNS_USED):
        '''
        returns the pandas dataframe containing the join between the patient and the infectors' information
        *patient_data*: pandas dataframe containing the patient information
        *infector_columns_used*: list containing the infector columns that will be used
        '''
        def generate_age_groups(age):
            '''
            returns the age group where a certain age belongs to
            *age*: the age of a particular infector
            '''
            if np.isnan(age):
                return "unknown"
            elif age < 20:
                return "child"
            elif age < 40:
                return "20s_30s"
            elif age < 60:
                return "50s_60s"
            elif age < 75:
                return "60s_70s"
            else:
                return "elderly"
        
        infector_data = patient_data[[Params.PATIENT_ID] + Params.INFECTOR_COLUMNS_USED]
        infector_data.columns = [Params.INFECTOR_ID] + list(map(
        lambda col: "infector_{}".format(col), Params.INFECTOR_COLUMNS_USED))
        joined_data = pd.merge(patient_data, infector_data, on = Params.INFECTOR_ID, how = "left")
        joined_data["infector_{}".format(Params.AGE)] = joined_data["infector_{}".format(Params.AGE)].apply(generate_age_groups)
        joined_data["infector_{}".format(Params.SEX)] = joined_data["infector_{}".format(Params.SEX)].fillna("unknown")
        return joined_data
    
    
    
    def map_state_to_severity(patient_data, severe_case_day_thres = Params.SEVERE_CASES_DAY_THRES, current_date = Params.MOST_RECENT_DATE_RECORDED):
        '''
        returns the patient data with the state mapped to either a severe or non-severe case
        *patient_data*: pandas dataframe
        *severe_case_day_thres*: the number of days threshold determining whether a case should be considerd severe or not
        *current_date*: the latest recorded date in the dataset (representing the present)
        '''
        def map_released_cases_to_severity_level(released_patients):
            '''
            returns the pandas dataframe of released patients with their case being mapped to a severity level
            *released_patients*: pandas dataframe containing information regarding the released patients
            '''
            released_patients["days_in_hospital"] = (released_patients[Params.RELEASED_DATE] - released_patients[Params.ADMISSION_DATE]).dt.days
            released_patients.loc[released_patients["days_in_hospital"] > severe_case_day_thres, Params.STATE] = Params.SEVERE
            released_patients.loc[released_patients["days_in_hospital"] <= severe_case_day_thres, Params.STATE] = Params.MILD
            return released_patients.drop("days_in_hospital", axis = 1)
            
        def map_isolated_cases_to_severity_level(isolated_patients):
            '''
            returns the pandas dataframe of isolated patients with their case being mapped to a severity level
            *isolated_patients*: pandas dataframe containing information regarding the isolated patients
            '''
            isolated_patients["days_in_hospital"] = (current_date - isolated_patients[Params.ADMISSION_DATE]).dt.days
            isolated_patients.loc[isolated_patients["days_in_hospital"] > severe_case_day_thres, Params.STATE] = Params.SEVERE
            return isolated_patients[isolated_patients[Params.STATE] != "isolated"].drop("days_in_hospital", axis = 1)
        
        
        deceased_patients = patient_data[patient_data[Params.STATE] == "deceased"]
        isolated_patients = patient_data[patient_data[Params.STATE] == "isolated"]
        released_patients = patient_data[(patient_data["state"] == "released") & (~patient_data["released_date"].isnull())]
        
        deceased_patients[Params.STATE] = Params.SEVERE
        isolated_patients = map_isolated_cases_to_severity_level(isolated_patients)
        released_patients = map_released_cases_to_severity_level(released_patients)
        
        patients_data = pd.concat([deceased_patients, isolated_patients, released_patients])
        return patients_data
        
        
     
    def add_prefix_to_values_of_categorical_columns(data, categorical_columns_to_prefix_dict = Params.CATEG_COL_TO_PREFIX):
        '''
        returns a pandas dataframe with the values of the categorical columns acquiring a distinguishing prefix
        *data*: pandas dataframe 
        *categorical_columns_to_prefix_dict*: dictionary of the form (categorical column --> distinguishing prefix)
        '''
        def add_pref_to_col_values(data, col):
            '''
            returns a pandas dataframe with a certain column values being added a prefix
            *data*: pandas dataframe
            *col*: categorical colunn name
            '''
            data[col] = categorical_columns_to_prefix_dict[col] + data[col]
            return data
        
        data = reduce(lambda data, col: add_pref_to_col_values(data, col), list(categorical_columns_to_prefix_dict.keys()), data)
        return data
    
    
    def perform_one_hot_encoding(data, categorical_columns = list(Params.CATEG_COL_TO_PREFIX.keys())):
        '''
        returns the pandas dataframe with all the categorical columns being one-hot encoded
        *data*: pandas dataframe
        *categorical_columns*: list containing the names of the categorical columns
        '''
        def perform_one_hot_encoding_of_col(data, categ_predictor):
            '''
            returns a pandas dataframe containing the existing columns plus the one-hot encoded columns of a particular categorical column
            *data*: pandas dataframe
            *categ_predictor*: the name of the column to be one-hot-encoded
            '''
            one_hot_col = pd.get_dummies(data[categ_predictor])
            data = data.join(one_hot_col)
            data = data.drop([categ_predictor],axis=1)
            return data
        
        data = reduce(lambda data, col: perform_one_hot_encoding_of_col(data, col), categorical_columns, data)
        return data
    
    
    def map_state_to_binary_labels(state_series):
        '''
        returns pandas series containing the state column mapped to binary labels
        *state_series*: pandas series containing the contents of the state column 
        '''
        def map_state_to_binary(state):
            '''
            returns a binary label depending on the state's value
            *state*: the state of a particular patient
            '''
            return 1 if state == Params.SEVERE else 0
        return state_series.apply(map_state_to_binary)
        
            
            
        
        
        
        
        

