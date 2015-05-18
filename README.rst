Common-Player
=============

Quickstart
----------

Firstly you will need to run the crossbar.io router via docker:

.. code-block:: bash

    docker-composer up

Once that is up and running we can forget about it and install our requirements
with the following command.

.. code-block:: bash

    pip install -r requirements.txt


.. warning::
    There is currently a minor patch needed on the pyspotify library


Once all the requirements have been installed you need to supply the
application with your Spotify credentials. You can do this by exporting them as
environmental variables:

.. code-block:: bash

    export SPOTIFY_USER="my_user"
    export SPOTIFY_PASSWORD="my_password"

If you are running boot2docker instead of a proper operating system you will
also need to export the router dsn for crossbar:

.. code-block:: bash

    export ROUTER_DSN = "ws://<boot2docker ip>:8080/ws"


You can finally run the player component as follows:

.. code-block:: bash

    cd player
    ./run.py start_service

