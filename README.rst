To run the docker container, execute the following command:

.. code-block:: bash

    docker compose up --build


To perform migrations, run the following command within the tic_tac_toe container:

.. code-block:: bash

   docker compose exec tic_tac_toe bash run_migration.sh

For local execution, set the following environment variables:

.. code-block:: bash

   export FLASK_APP=tic_tac_toe.application
   export FLASK_ENV=development
   flask run

You can also use PyCharm to run the application, but make sure to set up the environment variables from docker/requirements.txt.

To create a game and play it, refer to the provided example in the designated folder.
