import pyglet
import numpy as np
from envqwop import QWOPEnv
from bot import Bot
import threading
import time
import os
import random

all_files=[]
def runLoop(env):
    for dirpath, dirnames, filenames in os.walk("checkpoints3"):
        for file in filenames:
            all_files.append(os.path.join(dirpath, file))
    r=random.randint(0,7)
    if all_files:
        random_file = all_files[0]
            
    bot = Bot(env,random_file)
    
    # Simulate for 10 seconds
    for _ in range(20000):
        action = bot.act()
        
        obs, reward, done, info = env.step(action)
        
        bot.observe(obs)
        

        time.sleep(0.01)

def main():
    env = QWOPEnv(screen=True)
    
    # Create separate thread for logic updates
    threading.Thread(target=runLoop, args=(env,)).start()
    
    # Graphics thread
    pyglet.app.run()

if __name__ == "__main__":
    main()
    