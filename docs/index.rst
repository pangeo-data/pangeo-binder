Pangeo
======

.. image:: _static/pangeo_simple_logo.svg
   :width: 390 px

.. raw:: html

   <br />

.. image:: _static/binder_logo.png
   :width: 145 px

About Pangeo's Binder
---------------------

Much like mybinder.org_, the `Pangeo's`_ BinderHub deployment (`binder.pangeo.io`_)
allows users to create and share custom computing environments. The main distinction
between the two BinderHubs is that Pangeo's BinderHub allows users to perform
scalable computations using `Dask Gateway`_.

For more information on the Pangeo project, check out the `online documentation`_.

Using Pangeo's Binder
---------------------

Preparing a repository for use with a BinderHub is quite simple. The best place
to start is the `BinderHub documentation`_. The sections below outline some
common configurations used on Pangeo's BinderHub deployment. Specifically,
we'll provide examples of the ``.dask/config.yaml`` configuration file and the
``binder/start`` script.

Using the Pangeo-Binder Cookiecutter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have put together a cookiecutter repo to help setup binder repositories that
can take advantage of Pangeo. This automates the setup of some of the
configuration (described in detail below). The usage for this tool is described
below.

::

  pip install -U cookiecutter
  cookiecutter https://github.com/pangeo-data/cookiecutter-pangeo-binder.git

After running the cookiecutter command, simply follow the command line instructions
to compete setting up your repository. Add some Jupyter Notebooks, configure your
environment and push the whole thing to GitHub.

Configuring Dask
~~~~~~~~~~~~~~~~

The Pangeo Binder is configured to include a Dask Gateway server, which allows
users to create Dask Clusters for distributed computation. To create the clusters,
we recommend depending on the ``pangeo-notebook`` metapackage. This metapackage
brings in `several dependencies`_ including dask-gateway and dask-labextension.

.. code-block:: yaml

   # binder/environment.yml
   channels:
     - conda-forge
   dependencies:
     - pangeo-notebook
     # Additional packages for your analysis...

The version of dask-gateway pre-configured on the Binder must
match the dask-gateway in the ``environment.yml``. That's currently
``dask-gateway==0.7.1``.

With Dask Gateway installed, your notebooks can create clusters:

.. code-block:: python

   from dask_gateway import Gateway
   from dask.distributed import Client

   gateway = Gateway()
   cluster = gateway.new_cluster()

   client = Client(cluster)

You can use :meth:`dask_gateway.GatewayCluster.scale` to scale the number
of workers manually, or set the cluster to adaptive mode with
:meth:`dask_gateway.GatewayCluster.adapt` to scale up and down based on
computational load.

start script
~~~~~~~~~~~~

The start script (e.g. ``binder/start``) provides a mechanism to update the
user environment at run time. The start script should look roughly like the
example below. A few key points about using the start script:

- The start script must end with the ``exec "$@"`` line.
- The start script should not do any major work (i.e. don't download a large
  dataset using this script)

::

  #!/bin/bash

  # Replace DASK_DASHBOARD_URL with the proxy location
  sed -i -e "s|DASK_DASHBOARD_URL|/user/${JUPYTERHUB_USER}/proxy/8787|g" binder/jupyterlab-workspace.json
  # Get the right workspace ID
  sed -i -e "s|WORKSPACE_ID|/user/${JUPYTERHUB_USER}/lab|g" binder/jupyterlab-workspace.json

  # Import the workspace into JupyterLab
  jupyter lab workspaces import binder/jupyterlab-workspace.json \
    --NotebookApp.base_url=user/${JUPYTERHUB_USER}

  exec "$@"

Examples using Pangeo's Binder
------------------------------

- `Pangeo Example Notebooks`_

.. _Pangeo: http://www.pangeo.io
.. _Pangeo's: http://www.pangeo.io
.. _online documentation: http://www.pangeo.io

.. _mybinder.org: https://mybinder.org
.. _binder.pangeo.io: http://binder.pangeo.io
.. _issues page: https://github.com/pangeo-data/pangeo/issues
.. _binderhub Documentation: https://binderhub.readthedocs.io/en/latest/
.. _Dask-kubernetes: https://dask-kubernetes.readthedocs.io/en/latest/
.. _Kubernetes: https://kubernetes.io/
.. _Pangeo Example Notebooks: https://github.com/pangeo-data/pangeo-example-notebooks
.. _Dask Gateway: https://gateway.dask.org/
.. _several dependencies: https://github.com/conda-forge/pangeo-notebook-feedstock/blob/master/recipe/meta.yaml
