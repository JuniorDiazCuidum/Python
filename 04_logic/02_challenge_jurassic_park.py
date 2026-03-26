

def count_carnivore_dinosaur_eegs(egg_list) -> int:
    
    total_carnivore_eggs = 0
    
    for eggs in egg_list:
        if eggs % 2 == 0:
            total_carnivore_eggs += eggs
    
    return total_carnivore_eggs
egg_list = [2, 3, 4, 5, 6, 7, 8]
print(count_carnivore_dinosaur_eegs(egg_list))


