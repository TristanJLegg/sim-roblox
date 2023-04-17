import random
from typing import Optional

import numpy as np

import gymnasium as gym
from gymnasium import logger, spaces
from gymnasium.envs.classic_control import utils
from gymnasium.error import DependencyNotInstalled

import pygame

class Agent:
    def __init__(self, x, y, radius=1):
        self.x = x
        self.y = y
        self.radius = radius

class Apple:
    def __init__(self, x, y, radius=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.eaten = False

    def eat(self):
        self.eaten = True

class SimRoblox(gym.Env):
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 50,
    }

    def __init__(self, render_mode: Optional[str] = None):
        low = -17
        high = 17
        # actions: 0 = up, 1 = right, 2 = down, 3 = left
        self.action_space = spaces.Discrete(4)
        # observations: agent x, agent y, apple x, apple y
        self.observation_space = spaces.Box(low, high, shape=(4,),dtype=np.float32)

        self.render_mode = render_mode

        self.screen_width = 600
        self.screen_height = 600
        self.screen = None
        self.clock = None
        self.isopen = True
        self.state = None

    def step(self, action):
        err_msg = f"{action!r} ({type(action)}) invalid"
        assert self.action_space.contains(action), err_msg
        assert self.state is not None, "Call reset before using step method."

        # Place the step logic here

        self.current_step = self.current_step + 1

        # check if the agent has reached the apple
        if self.apple.eaten:
            terminated = True
            reward = 5

        # check if max steps has been reached
        max_steps = 256
        if max_steps > self.current_step:
            truncated =  True

        if self.render_mode == "human":
            self.render()

        self.state = np.array([self.agent.x, self.agent.y, self.apple.x, self.apple.y], dtype=np.float32)

        return self.state, reward, terminated, truncated, {}

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)

        self.current_step = 0

        self.apple = Apple(
            x = 14,
            y = 14,
        )
        self.agent = Agent(
            x = (random.random() * 34) - 17, # random number between -17 and 17
            y = (random.random() * 34) - 17, # random number between -17 and 17
        )

        self.state = np.array([self.agent.x, self.agent.y, self.apple.x, self.apple.y], dtype=np.float32)

        if self.render_mode == "human":
            self.render()

        return self.state, {}

    def render(self):
        if self.render_mode is None:
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym("{self.spec.id}", render_mode="rgb_array")'
            )
            return

        try:
            from pygame import gfxdraw
        except ImportError:
            raise DependencyNotInstalled(
                "pygame is not installed, run `pip install pygame`"
            )

        if self.screen is None:
            pygame.init()
            if self.render_mode == "human":
                pygame.display.init()
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height)
                )
            else:  # mode == "rgb_array"
                self.screen = pygame.Surface((self.screen_width, self.screen_height))
        if self.clock is None:
            self.clock = pygame.time.Clock()

        if self.state is None:
            return None

        self.surf = pygame.Surface((self.screen_width, self.screen_height))
        self.surf.fill((255, 255, 255))

        pixel_multiplier = self.screen_width / 34 # this assumes the screen width==height

        apple_coord_x = int((self.apple.x + 17) * pixel_multiplier)
        apple_coord_y = int((self.apple.y + 17) * pixel_multiplier)

        agent_coord_x = int((self.agent.x + 17) * pixel_multiplier)
        agent_coord_y = int((self.agent.y + 17) * pixel_multiplier)

        apple_radius = int(self.apple.radius * pixel_multiplier)
        agent_radius = int(self.agent.radius * pixel_multiplier)

        color_red = (255,0,0)
        color_blue = (0,0,255)

        gfxdraw.filled_circle(self.surf, apple_coord_x, apple_coord_y, apple_radius, color_red)
        gfxdraw.filled_circle(self.surf, agent_coord_x, agent_coord_y, agent_radius, color_blue)

        self.surf = pygame.transform.flip(self.surf, False, True)
        self.screen.blit(self.surf, (0, 0))
        if self.render_mode == "human":
            pygame.event.pump()
            self.clock.tick(self.metadata["render_fps"])
            pygame.display.flip()

        elif self.render_mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )

    def close(self):
        if self.screen is not None:
            import pygame

            pygame.display.quit()
            pygame.quit()
            self.isopen = False