

# def find_first_sum(nums, goal):
#     for i in range(len(nums)):
#         for j in range(i +1, len(nums)):
#             if nums[i]+ nums[j] == goal:
#                 return [i, j]
            
#     return None        
    
def find_first_sum (nums, goal):
    seen = {}
    
    for index, value in enumerate(nums):
        missing = goal - value
        if missing in seen: return [seen[missing], index]
        seen[value] = index
        
    return None
    
    
nums = [4, 5, 6, 2]
goal = 8
result = find_first_sum(nums, goal)
print(result)
