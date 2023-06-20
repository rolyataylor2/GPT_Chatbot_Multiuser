#
#   Imports
#
import functions_helper as file
import functions_chatbot as chatbot
userProfileDirectory = 'Profiles'

#
#   Manage Profiles
#
def get(profile_name, create_default=False):
    data = file.open_file(userProfileDirectory + '/' + profile_name + '.txt')
    if data == '' and create_default == True:
        return file.open_file(userProfileDirectory + '/_new_profile.txt')
    return data

def set(profile_name, data):
    file.save_file(userProfileDirectory + '/' + profile_name + '.txt', data)
    return data
