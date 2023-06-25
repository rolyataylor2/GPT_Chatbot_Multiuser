
import functions_helper as file
def get(userUUID):
    current_state = file.open_file('Profiles/' + userUUID + '.txt')
    return current_state

def observe(userUUID, chatUUID):
    # Collect as many mannerisms as possilbe
    # compare the chatlog to the mannerisms and take the relavant ones and put them in the persona
    return ''