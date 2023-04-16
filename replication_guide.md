#Replication Guide
##Obtaining Kuhn poker results
These are instructions for replicating the results obtained in the accompanying research article: You gotta know when to fold'em, know when to reinforcement learn'em.

Please note that the final results for this project were obtained using a Raspberry Pi 2 model B 1GB device. Performing the same action on a laptop will most likely converge in less time.

1. Install the entire project using the information in the install.md file.
2. Naviagte to the root of the project i.e. texasholdem-gym-env
3. Open the 'kuhn_cfr.py' file, and change the number of iterations on line 154 to suit a given parameter.
4. Run the file using the command 
```
python kuhn_cfr.py
```
5. In some cases the file may take a while to finish running depending on how many iterations are set, but the output should look similar to the following:

```
Start Time = 16:27:21:916
player 1 expected value (Nash Equilibrium): -0.05266115736564762
player 2 expected value (Nash Equilibrium): 0.05266115736564762

Player 1 strategies:
0      ['0.76', '0.24']
0 pb   ['1.00', '0.00']
1      ['0.99', '0.01']
1 pb   ['0.41', '0.59']
2      ['0.26', '0.74']
2 pb   ['0.00', '1.00']

Player 2 strategies:
0 b    ['1.00', '0.00']
0 p    ['0.67', '0.33']
1 b    ['0.64', '0.36']
1 p    ['1.00', '0.00']
2 b    ['0.00', '1.00']
2 p    ['0.00', '1.00']
Number of iterations:50000
End Time = 16:27:27:867
```

##Undertsanding the results
The results above show (in order) an approximation of Nash equilibrium for player 1 and 2. Due to the zero sum nature of the game, one player will always have a positive value and the other a negative value. This basically shows the approximation for both strategies of both players. 

Below that are the individual strategies for player 1 and 2. These are presented in a table with the leftmost column showing the 'state' in the game tree (provided in research article) which includes the card they could be dealt followed by any actions made by either player, i.e. 0 pb   ['1.00', '0.00'] means that player 1 has been dealt a J card and they are at a point in the game were they have previously passed and player 2 has bet. 

The numbers in the following two columns represent the probability that that player will chose that action and is based on a reward value over several iterations. 

For more information on Kuhn poker and CFR, please refer to the accompanying research article and software development report for this project. 

Kuhn_CFR was adapted from a tutorial by Ian Sullivan, the original repository is available at [IanSullivan/PokerCFR (github.com)](https://github.com/IanSullivan/PokerCFR "IanSullivan/PokerCFR (github.com)").
