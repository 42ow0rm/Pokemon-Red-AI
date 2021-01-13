import retro
import gym
import os
import time
import sys

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.policies import MlpLnLstmPolicy
from stable_baselines import A2C
from stable_baselines.common.env_checker import check_env
from stable_baselines.common.cmd_util import make_vec_env
from stable_baselines.common.policies import FeedForwardPolicy, register_policy
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.vec_env import VecNormalize
from skipWrapper import SkipLimit


#Not Used
class CustomPolicy(FeedForwardPolicy):
    def __init__(self, *args, **kwargs):
        super(CustomPolicy, self).__init__(*args, **kwargs,
                                           net_arch=[dict(pi=[128, 128, 128],
                                                          vf=[128, 128, 128])],
                                           feature_extraction="cnn")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def train_model(n_vec = 4, time_steps = 2000):
        retro.data.Integrations.add_custom_path(
                os.path.join(SCRIPT_DIR, "custom_integrations")
        )
        print("PokemonRed-GameBoy" in retro.data.list_games(inttype=retro.data.Integrations.ALL))
        env = retro.make("PokemonRed-GameBoy", inttype=retro.data.Integrations.ALL, obs_type=retro.Observations.RAM, use_restricted_actions=retro.Actions.DISCRETE) #, use_restricted_actions=retro.Actions.DISCRETE
        print(env)
        
        env = SkipLimit(env=env, time_between_steps=5)

        vec_env = make_vec_env(lambda: env, n_envs=n_vec)
        vec_env = VecNormalize(vec_env, norm_obs=True, norm_reward=True, clip_obs=10)
        # time.sleep(3)    

        model = A2C(MlpPolicy, vec_env, verbose=1, tensorboard_log="./pokemon-red-tensorboard/")

        start_time = time.time()
        model.learn(total_timesteps=time_steps, tb_log_name="a2c-MLP_5M")
        print("TRAINING COMPLETE! Time elapsed: ", str(time.time()-start_time))
        
        #Save model
        print("Saving model...")
        model.save("a2c_mlp_5M")

        #Save env stats
        print("Saving env stats...")
        vec_env.save("a2c_env_stats_pkmn.pk1")

def main():
     if len(sys.argv) < 2:
             train_model()
     else:
             train_model(n_vec=32, time_steps=int(sys.argv[1]))
if __name__ == "__main__":
        main()