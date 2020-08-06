# -*- coding: utf-8 -*-
import asyncio
import time

from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer
from tabulate import tabulate


class MaxDamagePlayer(Player):

    # The signature of choose_move is
    # choose_move(self, battle: Battle) -> str:
    # it takes a Battle object representing the game state as argument,
    # and returns a move order encoded as a string.
    # This move order must be formatted according to the showdown protocol.
    def choose_move(self, battle):
        # interesting properties of the battle input:
        # active_pokemon, available_moves, available_switches,
        # opponent_active_pokemon, opponent_team and team

        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available ones
            best_move = max(battle.available_moves, 
                    key=lambda move: move.base_power)
            return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)

async def main():
    start = time.time()

    # We create two players.
    random_player = RandomPlayer(
        battle_format="gen8randombattle",
    )
    max_damage_player = MaxDamagePlayer(
        battle_format="gen8randombattle",
    )

    # Now, let's evaluate our player
    await max_damage_player.battle_against(random_player, n_battles=100)

    print(
        "Max damage player won %d / 100 battles [this took %f seconds]"
        % (
            max_damage_player.n_won_battles, time.time() - start
        )
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
