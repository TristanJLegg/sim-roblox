from gymnasium.envs.registration import register

register(
     id="SimRoblox-v0",
     entry_point="sim_roblox.envs:SimRoblox",
)