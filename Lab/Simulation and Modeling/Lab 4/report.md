# Lab Report

## Title
**Simulation and Modeling — Markov Chains, Markov Decision Processes & Q-Learning**

**Name:** Manu Sharan Kumar
**Roll No:** ACE080BCT037

---

## Objectives

1. To study and simulate a **Markov Chain** and observe convergence to a stationary distribution.
2. To understand the **Markov Decision Process (MDP)** framework of states, actions, transitions, and rewards.
3. To implement the **Q-learning** algorithm and train an agent to find the optimal path through a grid-world with obstacles.

---

## Part 1: Markov Chains

**Theory:** A Markov Chain is a stochastic model where the probability of the next state depends only on the current state (the **memoryless / Markov property**):
$$ P(X_{n+1}=x \mid X_n=x_n,\dots,X_0=x_0) = P(X_{n+1}=x \mid X_n=x_n) $$
Its behaviour is described by a transition matrix $P$, with distribution updates $\pi_{n+1}=\pi_n P$. For many chains this converges to a unique **stationary distribution** $\pi=\pi P$.

**Example:** A 3-state weather model (Sunny, Cloudy, Rainy) with transition matrix:
```python
P = np.array([
    [0.6, 0.3, 0.1],   # from Sunny
    [0.3, 0.4, 0.3],   # from Cloudy
    [0.2, 0.3, 0.5],   # from Rainy
])
pi = np.array([1.0, 0.0, 0.0])   # start deterministically Sunny
for step in range(15):
    pi = pi @ P
```

**Output** (distribution after 15 steps, starting from Sunny):
```
Sunny = 0.3889, Cloudy = 0.3333, Rainy = 0.2778
```

The plot of each state's probability against step number shows all three curves converging smoothly to these fixed values, regardless of the starting state — demonstrating the predictive power of the transition matrix.

---

## Part 2: Markov Decision Processes & Q-Learning

**Theory:** An MDP extends a Markov Chain with **actions** and **rewards**, defined by $(S,A,P,R,\gamma)$. **Q-learning** is a model-free, trial-and-error reinforcement learning algorithm that learns the long-term value of taking an action in a state, using a lookup **Q-table**. The update rule is:
$$ Q(s,a) \leftarrow Q(s,a) + \alpha\left[R + \gamma \max_{a'}Q(s',a') - Q(s,a)\right] $$
where $\alpha$ is the learning rate, $\gamma$ the discount factor, $R$ the immediate reward, and $\max_{a'}Q(s',a')$ the best estimated future value from the next state $s'$.

---

## Part 3: Grid-World Q-Learning Simulation

A $4\times4$ grid (states $S_0$–$S_{15}$) with the agent starting at $S_0$, goal at $S_{15}$, and obstacles at $S_5, S_9$. Actions are `UP/DOWN/LEFT/RIGHT`; moves off the grid keep the agent in place. Reward function: $+10$ for reaching the goal, $-10$ for an obstacle (both end the episode), $-1$ for a normal step.

**Manual Q-update walkthrough** (with $\alpha=0.5$, $\gamma=0.9$) confirmed the update rule matches expected values, e.g. $Q(S_0,\text{RIGHT})=-0.5$ after one normal step, and $Q(S_{14},\text{RIGHT})=5.0$ after reaching the goal directly.

**Training:** An epsilon-greedy policy ($\epsilon=0.2$) was trained over 500 episodes (max 50 steps/episode):
```python
def choose_action(Q_table, s, epsilon):
    if random.random() < epsilon:
        return random.choice(ACTIONS)      # explore
    return ACTIONS[np.argmax(Q_table[s])]  # exploit
```

**Output** (representative run):
```
Average total reward, first 20 episodes : -8.6
Average total reward, last 20 episodes  : +2.1

Learned optimal policy (G = goal, X = obstacle):
 >  |  >  |  v  |  v
 v  |  X  |  v  |  v
 v  |  X  |  >  |  v
 >  |  >  |  >  |  G
```

The reward-per-episode plot (with a 20-episode rolling average) rises steeply from strongly negative rewards in early episodes to a stable positive value, showing the agent learning. The final policy grid shows arrows routing the agent down and around both obstacle cells toward the goal.

---

## Discussion

The Markov Chain example demonstrated the memoryless property: regardless of the starting state, the weather distribution converged to a fixed stationary distribution (Sunny ≈ 0.39, Cloudy ≈ 0.33, Rainy ≈ 0.28) after about 15 steps. The grid-world simulation extended this into a full MDP by adding actions and rewards. Early in training the agent's episode rewards were strongly negative, reflecting frequent random exploration into obstacles or long wandering paths; as training progressed, the epsilon-greedy policy increasingly exploited the learned Q-values, and the rolling-average reward rose to a stable positive value. The final learned policy consistently steers the agent around both obstacle cells toward the goal, confirming that the Q-table converged to a sensible action-value estimate for each state.

## Conclusion

The Markov Chain provides a mathematical framework for modeling stochastic state transitions, while the Markov Decision Process extends this by incorporating actions and rewards. Q-learning enables an agent to learn an optimal policy purely through trial-and-error interaction with its environment, without requiring a model of the environment's dynamics — by repeatedly applying the Bellman-style update rule, the agent discovers the sequence of actions that maximizes long-term cumulative reward.
