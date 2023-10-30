from collections import defaultdict
import random
import typing as t
import numpy as np
import gymnasium as gym


Action = int
State = int
Info = t.TypedDict("Info", {"prob": float, "action_mask": np.ndarray})
QValues = t.DefaultDict[int, t.DefaultDict[Action, float]]


class SarsaAgent:
    def __init__(
        self,
        learning_rate: float,
        gamma: float,
        legal_actions: t.List[Action],
    ):
        """
        SARSA  Agent

        You shoud not use directly self._qvalues, but instead of its getter/setter.
        """
        self.legal_actions = legal_actions
        self._qvalues: QValues = defaultdict(lambda: defaultdict(int))
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.exploration_bonus = 0.5
        self.state_action_counts = defaultdict(lambda: defaultdict(int))

    def get_qvalue(self, state: State, action: Action) -> float:
        """
        Returns Q(state,action)
        """
        return self._qvalues[state][action]

    def set_qvalue(self, state: State, action: Action, value: float):
        """
        Sets the Qvalue for [state,action] to the given value
        """
        self._qvalues[state][action] = value

    def get_value(self, state: State) -> float:
        """
        Compute your agent's estimate of V(s) using current q-values
        V(s) = max_a Q(s, a) over possible actions.
        """
        value = -np.inf
        # BEGIN SOLUTION
        #value = np.max([self.get_qvalue(state, action) for action in self.legal_actions])
        for action in self.legal_actions:
            q_value = self.get_qvalue(state, action)
            if q_value > value:
                value = q_value
        # END SOLUTION
        return value

    def update(
        self, state: State, action: Action, reward: t.SupportsFloat, next_state: State
    ):
        """
        You should do your Q-Value update here (s'=next_state):
           TD_target(s') = R(s, a) + gamma * V(s')
           TD_error(s', a) = TD_target(s') - Q(s, a)
           Q_new(s, a) := Q(s, a) + alpha * TD_error(s', a)
        """
        q_value = 0.0
        # BEGIN SOLUTION
        # Increment the count for the visited state-action pair
        self.state_action_counts[state][action] += 1
        
        # Modify the reward with the exploration bonus
        modified_reward = reward + self.get_exploration_bonus(state, action)

        td_target = modified_reward + self.gamma * self.get_value(next_state)
        td_error = td_target - self.get_qvalue(state, action)
        q_value = self.get_qvalue(state, action) + self.learning_rate * td_error
        # END SOLUTION

        self.set_qvalue(state, action, q_value)

    def get_best_action(self, state: State) -> Action:
        """
        Compute the best action to take in a state (using current q-values).
        """
        possible_q_values = [
            self.get_qvalue(state, action) for action in self.legal_actions
        ]
        index = np.argmax(possible_q_values)
        best_action = self.legal_actions[index]
        return best_action

    def get_exploration_bonus(self, state: State, action: Action) -> float:
        # The bonus is inversely proportional to the square root of the count
        return self.exploration_bonus / (1.0 + np.sqrt(self.state_action_counts[state][action]))


    def get_action(self, state: State) -> Action:
        """
        Compute the action to take in the current state, including exploration.
        """
        action = self.legal_actions[0]

        # BEGIN SOLUTION
        action = self.get_best_action(state)
        # END SOLUTION

        return action
