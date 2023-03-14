
# texasholdem-gym-env

A Gym environment for Heads Up No Limit Texas Hold'em that an be used to develop and compare reinforcement learning algorithms.

This project was created as a component of test software for a MEng Computer Science research and development project. 


## Dependencies
```
gym==0.26.0
pygame==2.1.0
PyHamcrest (required for unit testing only)
numpy
pandas
```
## Installation


1. Clone the repository from GitHub: 
[texasholdem_gym_env](https://github.com/DeadOnGames/texasholdem-gym-env)

2. Using a terminal / windows command shell, navigate to your cloned folder. Inside the folder, run
```bash
virtualenv -p python3 venv
venv\Scripts\activate.bat
```

to create and run a virtual environment. You will know if this has been successful if the (venv) flag appears on your terminal as shown below:
```bash
(venv) C:\Users\username\...\texasholdem-gym-env>
```
3. Use the following command to install all required dependencies and libraries 
```bash
pip install .
```
If this installs all requirements without error, then you can move on to step 4. Otherwise, you may need to update your version of pip or there may be a problem with how the project has been imported. Please note that the file structure should follow the same format as that of the original gym-examples API which can be found here:  [Gym Documentation](https://www.gymlibrary.dev/content/environment_creation/)

4. Now you should be ready to either run a class that makes use of an instance of the environment variable or run unit tests from the ‘tests’ folder.

    
## Usage/Examples

You can create an instance of this Gym environment as so
```python
import gym_examples
import gym

#Create an instance of the HUNLTH environment
env = gym.make('gym_examples/HUNLTH-v0')
```
Then, you can carry out actions (note that actions are stored as enum variables)
```python
action = 3
env.step(action)
```
## Acknowledgements

 - [Example code for the Gym documentation](https://github.com/Farama-Foundation/gym-examples)
 - [Gym documentation](https://www.gymlibrary.dev/content/environment_creation/)

The author would like to thank Dr Pantelis Sopasakis as supervisor for this project.


## Authors

- [@deadongames](https://github.com/DeadOnGames)

