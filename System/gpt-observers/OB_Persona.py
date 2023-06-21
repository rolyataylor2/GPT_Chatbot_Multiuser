
import functions_helper as file
def get(userUUID):
    current_state = file.open_file('Profiles/' + userUUID + '.txt')
    return current_state
