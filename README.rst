YakiRPM
=======

YakiRPM is a python library that uses the Perl module 'rpmgrill'to analyze
RPM packages.

Installing
----------

You can install it with:

.. code:: bash

    python setup.py install

Note that you will also need rpmgrill https://git.fedorahosted.org/cgit/rpmgrill.git
installed for it to work.

Usage
-----

Here is how you can use it:

.. code:: python

  import yakirpm
  yaki = yakirpm.YakiRPM()
  # This will test the kernel packages in mock's result dir,
  # results are in JSON.
  result = yaki.analyze_local('/var/lib/mock/fedora-19-x86_64/results', 'kernel*')

Note that a src RPM must be one of the RPMs that is analyzed. If there is a 'build.log'
file in the directory, that will also be analyzed.
