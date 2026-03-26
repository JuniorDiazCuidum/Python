
text = "RRRRRRJJJJJjjjjjrrrrrr"

def check_balance(text):
    text = text.upper()
    count_r = text.count("R")
    count_j = text.count("J")
    
    print(f"Count of R: {count_r} count of J: {count_j}")

    
    # if count_r == count_j:
    #     return True
    # else:
    #     return False
    
    return count_r == count_j
    
print(check_balance("RRJJ"))
print(check_balance("RRRRJJJJ"))
print(check_balance("RRJJJJ"))
print(check_balance("asdagasfasqwdqwd"))


    