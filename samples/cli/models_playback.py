


#We supposed that we are inside a document column
#Each figure pose is 7 chars width

#We should read the file, store each pose and finally
#Animate them

import io
import os
from time import sleep


print("Thi is a test to view the models.cli.sample ascii animations")
mod_east = open('models_attack_east.cli.sample', 'r')
mod_west = open('models_attack_west.cli.sample', 'r')
mod_run_e = open('models_run_east.cli.sample', 'r')
mod_run_w = open('models_run_west.cli.sample', 'r')
rawAE = mod_east.readlines()
rawRE = mod_run_e.readlines()
rawAW = mod_west.readlines()
rawRW = mod_run_w.readlines()

step = -1
while (True):
    step += 1
    fi = step * 7
    fe = (step * 7 + 1) + 6
    print("Frame %d:%d"%(fi, fe)+"| Step %d/%d"%(step, len(rawAE[2])/7 -1))
    print("ATTACK to the EAST")
    print(rawAE[1][fi:fe]+" "+rawAE[5][fi:fe]+" "+rawAE[9 ][fi:fe]+" "+rawAE[13][fi:fe]+" "+rawAE[17][fi:fe]+" "+rawAE[21][fi:fe])
    print(rawAE[2][fi:fe]+" "+rawAE[6][fi:fe]+" "+rawAE[10][fi:fe]+" "+rawAE[14][fi:fe]+" "+rawAE[18][fi:fe]+" "+rawAE[22][fi:fe])
    print(rawAE[3][fi:fe]+" "+rawAE[7][fi:fe]+" "+rawAE[11][fi:fe]+" "+rawAE[15][fi:fe]+" "+rawAE[19][fi:fe]+" "+rawAE[23][fi:fe])
    print("RUN to the EAST")
    print(rawRE[1][fi:fe]+" "+rawRE[5][fi:fe]+" "+rawRE[9 ][fi:fe]+" "+rawRE[13][fi:fe]+" "+rawRE[17][fi:fe]+" "+rawRE[21][fi:fe])
    print(rawRE[2][fi:fe]+" "+rawRE[6][fi:fe]+" "+rawRE[10][fi:fe]+" "+rawRE[14][fi:fe]+" "+rawRE[18][fi:fe]+" "+rawRE[22][fi:fe])
    print(rawRE[3][fi:fe]+" "+rawRE[7][fi:fe]+" "+rawRE[11][fi:fe]+" "+rawRE[15][fi:fe]+" "+rawRE[19][fi:fe]+" "+rawRE[23][fi:fe])
    print("ATTACK to the WEST")
    print(rawAW[1][fi:fe]+" "+rawAW[5][fi:fe]+" "+rawAW[9 ][fi:fe]+" "+rawAW[13][fi:fe]+" "+rawAW[17][fi:fe]+" "+rawAW[21][fi:fe])
    print(rawAW[2][fi:fe]+" "+rawAW[6][fi:fe]+" "+rawAW[10][fi:fe]+" "+rawAW[14][fi:fe]+" "+rawAW[18][fi:fe]+" "+rawAW[22][fi:fe])
    print(rawAW[3][fi:fe]+" "+rawAW[7][fi:fe]+" "+rawAW[11][fi:fe]+" "+rawAW[15][fi:fe]+" "+rawAW[19][fi:fe]+" "+rawAW[23][fi:fe])
    print("RUN to the WEST")
    print(rawRW[1][fi:fe]+" "+rawRW[5][fi:fe]+" "+rawRW[9 ][fi:fe]+" "+rawRW[13][fi:fe]+" "+rawRW[17][fi:fe]+" "+rawRW[21][fi:fe])
    print(rawRW[2][fi:fe]+" "+rawRW[6][fi:fe]+" "+rawRW[10][fi:fe]+" "+rawRW[14][fi:fe]+" "+rawRW[18][fi:fe]+" "+rawRW[22][fi:fe])
    print(rawRW[3][fi:fe]+" "+rawRW[7][fi:fe]+" "+rawRW[11][fi:fe]+" "+rawRW[15][fi:fe]+" "+rawRW[19][fi:fe]+" "+rawRW[23][fi:fe])

    print('\n' * int(os.get_terminal_size().lines-17), end='\r')
    if step == 0:
        #sleep(1/5)
        sleep(0.04)
    else:
        sleep(0.04)
    if step+1 >= len(rawAE[2])/7 - 1:
        step = -1

