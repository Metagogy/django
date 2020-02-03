import tensorflow as tf
import gym
import ShAl
import numpy as np
from AandC import *
#from TrainOrTest import *


def testDDPG(sess, env, actor, critic, newth):


    # test for max_episodes number of episodes
    # for i in range(int(1)):

    s = env.reset()

    ep_reward = 0
    ep_ave_max_q = 0

    #if action =='store_true':
        #env.render()
    

    a = actor.predict(np.reshape(s, (1, actor.s_dim))) 

   
    s2, r, terminal, info = env.step(a[0], newth)

   
    s = s2
    ep_reward += r

        # if terminal:
        #     print('| Episode: {:d} | Reward: {:d} |'.format(i, int(ep_reward)))
        #     break
    print("************************ new value****************")
    print(a)
    print("************************ new value****************")
    return (a)
    # return a
    
def test(newth):

    with tf.Session() as sess:

        env = gym.make('shal-v0')
        np.random.seed(258)
        tf.set_random_seed(258)
        env.seed(258)
        env._max_episode_steps = 1000

        state_dim = env.observation_space.shape[0]
        action_dim = env.action_space.shape[0]
        action_bound = env.action_space.high

        actor = ActorNetwork(sess, state_dim, action_dim, action_bound,
                float(0.0001), float(0.001), int(64))

        critic = CriticNetwork(sess, state_dim, action_dim,
                 float(0.001), float(0.001), float(0.99), actor.get_num_trainable_vars())

        saver = tf.train.Saver()
        saver.restore(sess, "ckpt/model")

        #testDDPG(sess, env, args, actor, critic)
        ping = testDDPG(sess, env, actor, critic, newth)


#test()



'''if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='provide arguments for DDPG agent')

    # agent parameters
    parser.add_argument('--actor-lr', help='actor network learning rate', default=0.0001)
    parser.add_argument('--critic-lr', help='critic network learning rate', default=0.001)
    parser.add_argument('--gamma', help='discount factor for Bellman updates', default=0.99)
    parser.add_argument('--tau', help='target update parameter', default=0.001)
    parser.add_argument('--buffer-size', help='max size of the replay buffer', default=1000000)
    parser.add_argument('--minibatch-size', help='size of minibatch', default=64)

    # run parameters
    parser.add_argument('--env', help='gym env', default='shal-v0')
    parser.add_argument('--random-seed', help='random seed', default=258)
    parser.add_argument('--max-episodes', help='max num of episodes', default=250)
    parser.add_argument('--max-episode-len', help='max length of each episode', default=1000)
    parser.add_argument('--render-env', help='render gym env', action='store_true')
    parser.add_argument('--mode', help='train/test', default='train')
    
    
    args = vars(parser.parse_args())
    
    pp.pprint(args)

    if (args['mode'] == 'train'):
      train(args)
    elif (args['mode'] == 'test'):
      test(args)
'''

# test()
    

