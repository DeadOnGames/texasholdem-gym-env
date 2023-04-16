##Installation guide
This is a more in-depth installation guide for texasholdem-gym-env that the steps included in README.md.

1. Clone the repository from GitHub / GitLab:
[GitHub repo](https://github.com/DeadOnGames/texasholdem-gym-env/blob/main/gym_examples/envs/HUNLTH_env.py "GitHub repo")
    Using a terminal / windows command shell, navigate to your cloned folder

2. Inside the folder, run
```
    virtualenv -p python3 venv
    venv\Scripts\activate.bat
	```
to create and run a virtual environment. You will know if this has been successful if the (venv) flag appears on your terminal as shown below:

    (venv) C:\Users\username\...\texasholdem-gym-env>
3. Use the following command to install all required dependencies and libraries 
```
pip install .
```

If this installs all requirements without error, then you can move on. Otherwise, you may need to update your version of pip or there may be a problem with how the project has been imported. Please note that the file structure should follow the same format as that of the original gym-examples API which can be found here: [ Make your own custom environment - Gym Documentation (gymlibrary.dev)](http://https://www.gymlibrary.dev/content/environment_creation/ " Make your own custom environment - Gym Documentation (gymlibrary.dev)")

Now you should be ready to either run a class that makes use of an instance of the environment variable or run unit tests from the ‘tests’ folder as shown below

```
python gym_examples\tests\<filename>
```

##Usage guide
A user can create an instance of the texasholdem-gym-env as shown below
```
import gym

#Create an instance of the HUNLTH environment
env = gym.make('gym_examples/HUNLTH-v0')
env.reset() #Note that the env must be reset before starting a new game
```

This will create a new game of HUNL Texas hold’em which can be used to perform actions, render the game to the command line and return observations. Let’s trace through the game and look at exactly what is happening.

Actions can be made in the game using the step() function call with an input parameter that corresponds to the id of the action enum value. Note that for each action, the player number (i.e. player 1 or player 2) will need to be set and the flag for whether they are the dealer or not. This can be performed in a loop for actual reinforcement learning iterations but for this representation, they will need to be set before each step() function call.

The following code snippet shows how actions can be sent to the environment for two stages of poker:
```
    #-----------Prepreflop-------
    env.set_dealer(True)
    env.set_player_num(1)
    env.step(7) #Player1 makes a SB to start

    env.set_dealer(False)
    env.set_player_num(2)
    env.step(8) #Player2 makes a BB

    #-----------Flop-------------
    env.set_dealer(True)
    env.set_player_num(1)
    env.step(4) #Player1 raises by pot

    env.set_dealer(False)
    env.set_player_num(2)
    env.step(2) #Player2 calls
```

At this stage, not much will be output to the command line to inform us if our actions are being registered or what is actually happening in the game, to do that we used the render() function call.
```
    #-----------Turn-------------
    render() #First render call

    env.set_dealer(True)
    env.set_player_num(1)
    env.step(4) #Player1 raises by pot
    render() #Second render call

    env.set_dealer(False)
    env.set_player_num(2)
    env.step(2) #Player2 calls
    env.render() #Third render call
```

##Expected outcomes
At any point, in any stage, the render() call can be made which will output information in the format shown below. Note that some information may not be displayed for every stage i.e. community cards are not dealt until the flop.

```
                       ♣ ♥ ♦ ♠ POKERBOT ♣ ♥ ♦ ♠
                    ┌──────────────────────────────────────┐
                        Stage: RIVER   Pot: £ 405
                    └──────────────────────────────────────┘
┌──────────────────────────────────────┐ ┌──────────────────────────────────────┐
  Player 1 wealth: £ 9800                   Player 2 wealth: £ 9795
└──────────────────────────────────────┘ └──────────────────────────────────────┘
Community cards:
┌─────────┐
│5        │
│         │
│    ♣    │
│         │
│        5│
└─────────┘
┌─────────┐
│3        │
│         │
│    ♦    │
│         │
│        3│
└─────────┘
┌─────────┐
│10       │
│         │
│    ♥    │
│         │
│       10│
└─────────┘
Player 1 hand:
┌─────────┐
│4        │
│         │
│    ♦    │
│         │
│        4│
└─────────┘
┌─────────┐
│2        │
│         │
│    ♥    │
│         │
│        2│
└─────────┘
Player 2 hand:
┌─────────┐
│2        │
│         │
│    ♣    │
│         │
│        2│
└─────────┘
┌─────────┐
│Q        │
│         │
│    ♣    │
│         │
│        Q│
└─────────┘
Player 1 : RAISE_POT £405
Player 2 : CALL £405
```
