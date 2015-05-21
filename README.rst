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

    make setup-dev


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


The front end is written with the aid of ReactJS, you can find this part in the
``ui`` folder. Gulp is used to automatically build everything. To install the
node requirements:

.. code-block:: bash

    cd ui
    npm install

Then to run the watcher that initiates a rebuild on changes being save:

.. code-block:: bash

    cd ui
    npm start


Roadmap
-------

- Make the sorting after votes less sucky
- Add "skip this" action to allow consensus voting on skipping certain tracks
- Tidy up less files and make a little more consistent
