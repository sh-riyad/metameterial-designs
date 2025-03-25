************
Installation
************

Since this package has not been published on `PyPi`_ yet, installation requires
to manually download the code and install the module via the ``setup.py``
script. The code can be found in
https://gitlab.insa-rennes.fr/hermes/cst-python-api, and it can be downloaded
either by running a ``git clone`` on a terminal:

.. code-block:: console

    > git clone https://gitlab.insa-rennes.fr/hermes/cst-python-api

Or directly using GitLab's web interface (if this option is chosen, please
unzip the downloaded file before continuing with the instructions below). Once
that the code has been downloaded, we can proceed with the installation:

.. code-block:: console

    > cd cst-python-api
    > pip install .

To verify that the module was successfully installed, we can use the following
command:

.. code-block:: console

    > pip show cst-python-api

If the installation has been successful, information about the module will be
displayed in the terminal.

.. _PyPi: https://pypi.org/