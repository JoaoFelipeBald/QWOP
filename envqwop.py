from qwop import Game, GameWindow
import pyglet
import numpy as np
import gym
from gym.spaces import Tuple,Box,Discrete,MultiDiscrete
import random
import threading
import time
from collections import deque


class QWOPEnv(gym.Env):
    def __init__(self, screen=False):
        super().__init__()
        
        self.screen = screen
        self.createGame()
        
        # Possible movements are activations for all 4 limbs (thighL, thighR, calfL, calfR)
        self.action_space = Box(low=-1, high=1, shape=(4,), dtype=np.float32)
        

        # matches getInputs()
        self.observation_space = Box(low=-np.inf, high=np.inf, shape=(10,), dtype=np.float32)
        # 0  character x position
        # 1  character y position
        # 2  head x position
        # 3  head y position
        # 4  torso x position
        # 5  torso y position
        # 6  left foot x position
        # 7  left foot y position
        # 8  right foot x position
        # 9  right foot y position
        
        # It's suggested to scale position by 1.25/200
        self.startPos = self.game.get_character_position()*1.25/200
        
        self.x = 0
        
        self.last=0
        self.time=0
        self.positions = deque([0] * 20, maxlen=20)
        self.lpositions_feet = deque([0] * 1, maxlen=1)
        self.rpositions_feet = deque([0] * 1, maxlen=1)
        self.foot="left"
        self.samepos=0
        ### These are not included in the observation space but can be used for your solution
        
        # Head angle relative to torso in radians
        # headAngle = np.arctan2(game.character.head.position[1]-game.character.torso.position[1], game.character.head.position[0]-game.character.torso.position[0])
        
        # Positional difference between feet
        #legDeltaX = [game.character.footR.position[0] - game.character.footL.position[0]]
        #legDeltaY = [game.character.footR.position[1] - game.character.footL.position[1]]
        
        # Distance between head and feet
        #headToRightFoot = np.linalg.norm(game.character.head.position - game.character.footR.position)
        #headToLeftFoot = np.linalg.norm(game.character.head.position - game.character.footL.position)
        
        # Maximum body length
        #bodyDelta = max(headToRightFoot, headToLeftFoot)

            
    def step(self, action):
        action = np.clip(action, -1, 1)  # Ensure actions are within the [-1, 1] range
        action *= 9000  # Scale the action to match the force range
        self.time += 1
        # Apply the actions to the limbs
        self.game.character.move_thighL(action[0])
        self.game.character.move_thighR(action[1])
        self.game.character.move_calfL(action[2])
        self.game.character.move_calfR(action[3])
        
        # Step the game forward
        self.game.step()

        # Update the observation and reward
        curPos = self.game.get_character_position() * 1.25 / 200


        obs = self.getInputs()
        obs = np.array(obs).flatten()
        cx,cy,hx,hy,tx,ty,lx,ly,rx,ry=obs

        self.positions.append(curPos)    
        self.lpositions_feet.append(ly)    
        self.rpositions_feet.append(ry) 
        reward = curPos - self.startPos
        '''   
        if self.x<self.v1:
            reward = curPos - self.startPos
        if self.x>=self.v1:
            reward = curPos - self.positions[0]
        '''    
        pos=False
        if reward>0:
          pos=True


        reward*=3
        if self.x>=10 and ty>245 and ty<420 and 1==0:
            result = [a - b  for a, b in zip(self.lpositions_feet, self.rpositions_feet)]
            if abs(max(result)-min(result))>100:
              reward*=1.1

           
        if hx>lx and hx<rx and pos:
            reward*=1.5
                
        if 1==0:
            reward*=3

        if self.foot=="left" and rx>lx+60 and pos and 1==0:
             reward*=1.3
             self.foot="right"
             
        elif self.foot=="right" and lx>rx+60 and pos and 1==0: 
             reward*=1.3
             self.foot=="left"
             
        if ty>310 and pos and 1==0:
            reward*=1.1
        if ty<310 and pos and 1==0:
            reward/=1.3
        if ty>420 and pos:
            reward/=6
        if ly<80 and ry<80 and pos and 1==0:
            reward/=1.2
        if ly>100 and ry<80 and pos and 1==0:
            reward*=1.2
        if ry>100 and ly<80 and pos and 1==0:
            reward*=1.2

        self.steps += 1
        self.x += 1
        done=False
                
        if self.x%3==0:
            ...
        if self.x>2500 or hy<160:
            print("---------")
            print("curpos",curPos)
            print("---------")
            self.foot="left"
            
            
            if hy<160 and self.x>300:
                reward-=20
            elif hy<160:
                reward-=10
            
            done=True
            self.time=0
            self.x =0
        truncated = False
        
        if self.x%200==0:
          print("---------")
          print("reward",reward)
          print("---------")
            
            
            
        info = {}
        return obs, reward, done, info


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # use same parameters from last game
        self.createGame()
        self.steps = 0

        obs = self.getInputs()
        info = {}

        return obs

    def render(self):
        if not self.screen:
            return
        
    def createGame(self):
        self.steps = 0
        
        self.game = Game()
        
        if self.screen:
            self.gameWindow = GameWindow(self.game)
            
    def getInputs(self):
        inputs = np.array([self.game.character.get_position()[0],
        self.game.character.get_position()[1],
        self.game.character.head.position[0],
        self.game.character.head.position[1],
        self.game.character.torso.position[0],
        self.game.character.torso.position[1],
        self.game.character.footL.position[0],
        self.game.character.footL.position[1],
        self.game.character.footR.position[0],
        self.game.character.footR.position[1]])
        return inputs
