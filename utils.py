   
def create_table(result):
    max = 0
    for data in result:
        if len(str(data[0]))> max:
            max = len(str(data[0]))

    table = '\n| Place |   Name' + (max-6)*' '+ ' | Score |   Date    |'
    for i,data in enumerate(result): 
        table = table + '\n' + '|  ' + str(i+1) + (4-len(str(i+1)))*' '+' | ' + str(data[0]) + ' | ' + str(data[1]) + ' | ' + str(data[2])[:2]+'/'+str(data[2])[2:4]+'/'+str(data[2])[5:] + ' |'

    return table
