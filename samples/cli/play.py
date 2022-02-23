
import os
from time import sleep, time
from pj_render import render


render.initialize()
pjrendered = []

time_to_change = 5
last_change_time = 0
change_animation = False
last_run_east = True
while (True):
    
    if(time()-last_change_time >= time_to_change):
        last_change_time=time()
        if change_animation:
            change_animation = False
            last_run_east = not last_run_east
        elif not change_animation:
            change_animation = True

    if(change_animation):
        print("iddle")
        pjrendered = render.render()
    else:
        if last_run_east:
            print("running to the east")
        else:
            print("running to the west")
        pjrendered = render.render_run(last_run_east)

    print(pjrendered[0])
    print(pjrendered[1])
    print(pjrendered[2], end='\r')

    print('\n' * int(os.get_terminal_size().lines-4), end='\r')
    sleep(1/25)
