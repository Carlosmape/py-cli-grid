
import os
import sys
from time import sleep, time
sys.path.append("../../../") # added!
from pj_render import character_render
from env_render import env_render

pj_render1 = character_render()
pj_render1.update_equipment(False, None, None)
pj_render2 = character_render()
pj_render2.update_equipment(True, True, True)
pj_render3 = character_render()
pj_render3.update_equipment(True, False, False)

grass_render1 = env_render()
grass_render2 = env_render()
grass_render3 = env_render()
flower_render1 = env_render()
flower_render2 = env_render()

pjrendered = []
pjrendered_sword = []
pjrendered_staff = []

time_to_change = 5
last_change_time = 0
change_animation = False
last_run_east = True
last_iddle = False

while (True):
    
    if(time()-last_change_time >= time_to_change):
        last_change_time=time()
        if change_animation:
            change_animation = False
            last_run_east = not last_run_east
        elif not change_animation:
            change_animation = True
            last_iddle = not last_iddle

    attack = False
    running = False
    if(change_animation):
        if last_iddle:
            print("Characters: attack")
            attack = True
        else:
            print("Characters: iddle")
    else:
        if last_run_east:
            print("Characters: running to the east")
            running = True
        else:
            print("Characters: running to the west")
            running = True

    pj_render1.update_state(last_run_east,running, attack)
    pj_render2.update_state(last_run_east,running, attack)
    pj_render3.update_state(not last_run_east, False, True)


    pjrendered =        pj_render1.render()
    pjrendered_sword =  pj_render2.render()
    pjrendered_staff =  pj_render3.render()

    print(" ======="*3)
    print("|"+pjrendered[0]+"|"+pjrendered_sword[0]+"|"+pjrendered_staff[0]+"|") 
    print("|"+pjrendered[1]+"|"+pjrendered_sword[1]+"|"+pjrendered_staff[1]+"|") 
    print("|"+pjrendered[2]+"|"+pjrendered_sword[2]+"|"+pjrendered_staff[2]+"|") 
    print(" ======="*3)
   
    print("Environment: flowers iddle")
    print(" ======="*3)
    print("|"+flower_render1.render()[0]+"|"+flower_render2.render()[0]+"|") 
    print("|"+flower_render1.render()[1]+"|"+flower_render2.render()[1]+"|") 
    print("|"+flower_render1.render()[2]+"|"+flower_render2.render()[2]+"|") 
    print(" ======="*3)

    print("Environment: grass iddle")
    print(" ======="*3)
    print("|"+grass_render1.render()[0]+"|"+grass_render2.render()[0]+"|"+grass_render3.render()[0]+"|") 
    print("|"+grass_render1.render()[1]+"|"+grass_render2.render()[1]+"|"+grass_render3.render()[1]+"|") 
    print("|"+grass_render1.render()[2]+"|"+grass_render2.render()[2]+"|"+grass_render3.render()[2]+"|") 
    print(" ======="*3)


    print('\n' * int(os.get_terminal_size().lines-11), end='\r')
    sleep(1/25)
