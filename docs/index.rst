Pangeo
======

.. image:: _static/pangeo_simple_logo.svg
   :width: 500 px

.. raw:: html

   <br />

.. image:: _static/binder_logo.png
   :width: 400 px

About Pangeo's Binder
---------------------

Much like mybinder.org_, the `Pangeo's`_ BinderHub deployment (`binder.pangeo.io`_)
allows users to create and share custom computing environments. The main distinction
between the two BinderHubs is that Pangeo's BinderHub allows users to perform
scalable computations using the dask-kubernetes package.

For more information on the Pangeo project, check out the `online documentation`_.

Using Pangeo's Binder
---------------------

Preparing a repository for use with a BinderHub is quite simple. The best place
to start is the `BinderHub documentation`_. The sections below outline some
common configurations used on Pangeo's BinderHub deployment. Specifically,
we'll provide examples of the ``.dask/config.yaml`` configuration file and the
``binder/start`` script.

Configuring dask-kubernetes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Dask-kubernetes`_ is a library designed to deploy dask-distributed using
Kubernetes_. When using dask-kubernetes on binder, you need to specify some
basic configuration options. An example of a file named `.dask/config.yaml`.

Note the configuration value for ``image`` is set to ``WORKER_IMAGE``. This is
a template value that will be overwritten in the `start script`_ below.

.. .dask/config.yaml

::

  # .dask/config.yaml
  logging:
    bokeh: critical

  diagnostics-link: "../proxy/{port}/status"
    tick-maximum-delay: 5s

  kubernetes:
   worker-template:
     metadata:
     spec:
       restartPolicy: Never
       containers:
       - args:
           - dask-worker
           - --nthreads
           - '2'
           - --no-bokeh
           - --memory-limit
           - 7GB
           - --death-timeout
           - '60'
         image: WORKER_IMAGE
         name: dask-worker
         resources:
           limits:
             cpu: "1.75"
             memory: 7G
           requests:
             cpu: "1.75"
             memory: 7G

start script
~~~~~~~~~~~~

The start script (e.g. ``binder/start``) provides a mechanism to update the
binder environment at run time. The start script should look roughly like the
example below. A few key points about using the start script:

- The ``WORKER_IMAGE`` variable is updated using the ``sed`` command. This is an
  important step when using dask-kubernetes.
- The start script must end with the ``exec "$@"`` line.
- The start script should not do any major work (i.e. don't download a large
  dataset using this script)

::

   #!/usr/bin/env bash

   export DASK_DISTRIBUTED__DIAGNOSTICS_LINK={JUPYTERHUB_SERVICE_PREFIX}proxy/{port}/status
   export DASK_KUBERNETES__WORKER_TEMPLATE_PATH=${PWD}/.dask/config.yaml
   export DASK_KUBERNETES__WORKER_NAME=dask-{JUPYTERHUB_USER}-{uuid}


   # set worker image url in worker template
   if [[ -z "${JUPYTER_IMAGE_SPEC}" ]]; then
       echo "JUPYTER_IMAGE_SPEC is not set"
   else
     sed -i -e "s|WORKER_IMAGE|${JUPYTER_IMAGE_SPEC}|g" ${DASK_KUBERNETES__WORKER_TEMPLATE_PATH}
   fi

   exec "$@"

.. _Pangeo: http://www.pangeo.io
.. _Pangeo's: http://www.pangeo.io
.. _online documentation: http://www.pangeo.io

.. _mybinder.org: https://mybinder.org
.. _binder.pangeo.io: http://binder.pangeo.io
.. _issues page: https://github.com/pangeo-data/pangeo/issues
.. _binderhub Documentation: https://binderhub.readthedocs.io/en/latest/
.. _Dask-kubernetes: https://dask-kubernetes.readthedocs.io/en/latest/
.. _Kubernetes: https://kubernetes.io/
