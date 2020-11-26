import nltk
import monpa

def seg_pos(text):
    return monpa.pseg(text)

def calculate_edit_cost(orig, cor):
    '''
    M是Match
    I是insert cost
    D是delete cost
    R是replace cost
    I/D是insert和delete相加的cost
    '''
    o_len = len(orig) #5
    c_len = len(cor) #4
    # Create the cost_matrix and the op_matrix
    cost_matrix = [[0 for j in range(c_len+1)] for i in range(o_len+1)]
    op_matrix = [["O" for j in range(c_len+1)] for i in range(o_len+1)]
    # Fill in the edges
    for i in range(1, o_len+1):
        cost_matrix[i][0] = nltk.edit_distance(orig[i-1][1] + orig[i-1][0], '')
        op_matrix[i][0] = "D"
    for j in range(1, c_len+1):
        cost_matrix[0][j] = nltk.edit_distance('', cor[j-1][1] + cor[j-1][0])
        op_matrix[0][j] = "I"

    # Loop through the cost_matrix
    for i in range(o_len):
        for j in range(c_len):
            # Matches
            if orig[i] == cor[j]:
                cost_matrix[i+1][j+1] = 0
                op_matrix[i+1][j+1] = "M"
            # Non-matches
            else:
                sub_cost = get_sub_cost(orig[i], cor[j]) + nltk.edit_distance(orig[i], cor[j])
                if sub_cost < (cost_matrix[0][i] + cost_matrix[j][0]):
                    cost_matrix[i+1][j+1] = sub_cost
                    op_matrix[i+1][j+1] = "R"
                else:
                    cost_matrix[i+1][j+1] = cost_matrix[0][i] + cost_matrix[j][0]
                    op_matrix[i+1][j+1] = "I/D"
    # Return the matrices
    return cost_matrix, op_matrix

def get_sub_cost(o, c):
    if o == c: 
        return 0
    cost = 0
    cost = len(o[0]) - len(c[0])
    if o[1][0] == c[1][0]:
        cost += 2
    else:
        cost += 5
    return cost

if __name__ == '__main__':
    sent_orig = seg_pos('這也間接突顯出鴻海')
    sent_correct = seg_pos('也直接透露出鴻海')
    cost_matrix, op_matrix = calculate_edit_cost(sent_orig, sent_correct)
    for c in cost_matrix:
        print(c)
    for o in op_matrix:
        print(o)