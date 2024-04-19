.. FileGateway documentation master file, created by
   sphinx-quickstart on Wed Apr 17 21:14:15 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FileGateway's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Filegateway is a Flask application for serving and uploading files from and to several targets, build upon PyFilesystem.
Interacting with Filegateway is done through simple RESTful APIs.

.. autofunction:: filegateway.app.write_document

.. autofunction:: filegateway.app.read_document

.. autofunction:: filegateway.app.list_contents

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
