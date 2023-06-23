Tic Tac Toe Game
================

This program allows you to play the popular game Tic Tac Toe. It doesn't have a GUI, but you can play it through a REST API. In the future, a frontend service may be added. The game is containerized with Docker, so to run it, execute the following command:

.. code-block:: bash

    docker-compose up --build

The service should start running, but if you want to run manually migrations run the following command:

.. code-block:: bash

    docker-compose exec tic_tac_toe bash run_migration.sh

After executing these commands, the service should be available at http://localhost:8000.

To play the game, follow these steps:

1. Create a session for player 1 and player 2:

.. code-block:: http

    POST http://127.0.0.1:8000/api/new_session/player1

.. code-block:: http

    POST http://127.0.0.1:8000/api/new_session/player2

Players start with zero credits on the first run. To increase their credits, use the following requests:

.. code-block:: http

    POST http://127.0.0.1:8000/api/add_credits/player1

.. code-block:: http

    POST http://127.0.0.1:8000/api/add_credits/player2

2. Now, let's start the game. Use the following commands:

.. code-block:: http

    POST http://127.0.0.1:8000/api/start_game/player1

    > {% client.global.set('id', response.body.id); %}


.. code-block:: http

    POST http://127.0.0.1:8000/api/start_game/player2


To ensure that both players are in the same game, the "start_game" command needs to be executed for each player. The response to this command will contain the game ID, which will be needed to make moves.

3. To check the current state of the board, use the following request:

.. code-block:: http

    GET http://127.0.0.1:8000/api/board/{{ id }}

4. It's time to make a move. Use the following sample REST calls:

.. code-block:: http

    POST http://127.0.0.1:8000/api/move/{{ id }}/player1
    Content-Type: application/json

    {
        "col": 0,
        "row": 0
    }

.. code-block:: http

    POST http://127.0.0.1:8000/api/move/{{ id }}/player2
    Content-Type: application/json

    {
        "col": 0,
        "row": 1
    }

5. Finally, to check the game statistics, use the following request:

.. code-block:: http

    GET http://127.0.0.1:8000/api/get_stats
    Content-Type: application/json


Currently, it shows all the data in the database, but a filter will be added in the future to allow filtering by date, for example.

PS. If you want you can test game with:

     example/example.rest 
