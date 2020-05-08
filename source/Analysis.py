from . import *

class Analysis:
    
    def perc_of_infectors_who_are_patients(data):
        '''
        return the percentage of infectors that are also presented as patients in the dataset
        *data*: pandas dataframe containing the dataset
        '''
        all_patient_ids = set(data[Params.PATIENT_ID])
        all_infector_ids = set(data[Params.INFECTOR_ID])
        patients_and_infectors = all_patient_ids & all_infector_ids
        return len(patients_and_infectors) / len(all_infector_ids)
    
    
    def get_avg_of_staying_in_hospital_per_state(data, print_lengths = True):
        '''
        returns a ditionary of the form (status --> average of days staying in the hospital)
        *data*: pandas dataframe
        *print_lengths*: boolean denoting whether the lengths should be printed
        '''
        def print_length(status, date_col, length):
            '''
            prints the length of the records where the date corresponding to a particular status is available
            '''
            print("Number of {} with '{}' available: {}".format(status, date_col, length))
        
        released_data = data[data[Params.STATE] == "released"]
        deceased_data = data[data[Params.STATE] == "deceased"]
        if print_lengths:
            print_length("released", Params.RELEASED_DATE, len(released_data))
            print_length("deceased", Params.DEATH_DATE, len(deceased_data))
        
        released_data["number_of_days"] = (Processing.convert_column_to_datetime(released_data[Params.RELEASED_DATE]) - released_data[Params.ADMISSION_DATE]).dt.days
        deceased_data["number_of_days"] = (Processing.convert_column_to_datetime(deceased_data[Params.DEATH_DATE]) - deceased_data[Params.ADMISSION_DATE]).dt.days
        
        avg_days_dict = {
            "released": released_data["number_of_days"].mean(),
            "deceased": deceased_data["number_of_days"].mean()
        }
                  
        return avg_days_dict
    
    
    def deceased_and_feat_not_null(data, feat):
        '''
        prints the number of records of the dataset that correspond to deceased patients and the corresponding feature is not null
        *data*: pandas dataframe
        *feat*: the name of the feature of interest
        '''
        print(len(data[(data["state"] == "deceased") & (~data[feat].isnull())]))
        
