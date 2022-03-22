# Correcting user queries to recieve the right answers using  minimum edit distance algorithm (Levenshtein distance)

#Levenshtein Distance is found in bottom right corner of each matrix

# 1 for each insertion, 1 for deletion and 1 for substitution

"""
 Distance -> Minimum number of edits (operations) required to convert ‘str1’ into ‘str2’:
 1. Insert -> Cost =1 
 2. Remove -> Cost =1 
 3. Replace -> Cost =1
"""
def minEditDistance(a, b, rows, cols):
    
    #Build empty matrix of correct size to store results
    distance = arr = [[0 for i in range(cols+1)] for j in range(rows+1)]

    for i in range(rows + 1):
        for j in range(cols + 1):

            # First string is empty, insert all characters of second string
            if i == 0:
                distance[i][j] = j    

            # Second string is empty, remove all characters of second string
            elif j == 0:
                distance[i][j] = i  

            # If last characters are same, ignore last char and recur for remaining string
            elif a[i-1] == b[j-1]:
                distance[i][j] = distance[i-1][j-1]

            # If last character are different, consider all possibilities and find minimum
            else:
                distance[i][j] = min( 1+distance[i-1][j],  # Remove
                                1+distance[i][j-1],        # Insert
                                1+distance[i-1][j-1])      # Replace

    return distance[rows][cols]