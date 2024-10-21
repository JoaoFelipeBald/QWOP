from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from envqwop import QWOPEnv
import random
import time
from functools import partial

def make_env(v1, v2, v4, v5, v6, v7, v8, v9,v11, screen=False):
    return QWOPEnv(v1=v1, v2=v2, v4=v4, v5=v5, v6=v6, v7=v7, v8=v8, v9=v9,v11=v11, screen=screen)

if __name__ == '__main__':
        start_time = time.time() 
        print("_________")
        num_envs = 5  
        v1=random.randint(200, 201) 
        v2=round(random.random() * 2 + 1, 2)
        v3=round(random.random() * 5 + 1, 2)
        v4=round(random.random() * 1.5 + 2, 2)
        v5=round(random.random() * 1.5 + 2, 2)
        v6=round(random.random() * 1.5 + 1, 2)
        v7=round(random.random() * 1.5 + 1, 2)
        v8=round(random.random() * 1.5 + 1, 2)
        v9=round(random.random() * 8 + 1, 2)    
        v11=round(random.random() * 1.5 + 1, 2) 
        if random.random()>0.8:
            v11=1   
            
        env = SubprocVecEnv([
            partial(
                make_env,
                v1,v2,v4,v5,v6,v7,v8,v9,v11,
                screen=False
            ) for _ in range(num_envs)
        ])
        custom_objects = {
            "clip_range": 0.2,  # Default PPO clip range
            "lr_schedule": 0.0003  # Default learning rate schedule
        }
        env=QWOPEnv( screen=False)
        model=PPO.load("basis2.zip", env=env)
        model.learn(total_timesteps=10000000)
        end_time = time.time()  
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        

        model.save(f"checkpoints3/basis3")
        

        env.close()
