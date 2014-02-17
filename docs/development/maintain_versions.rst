Maintain adhocracy dependencies
===============================


Python dependencies
~~~~~~~~~~~~~~~~~~~

setup.py
--------

Direct dependencies are manually tracked in setup.py. This should only include
minimal versions if we know that we depend on a certain feature which was
included in that version.  And this should only include maximal versions if we
know that the library breaks our code in a certain version.


versions.cfg
------------

A known-good set of all direct and indirect dependency versions is maintained
in versions.cfg.  This makes sure that deployments always receive versions of
dependencies which have been tested as good, and avoids breakage through new
versions in PyPI.


To pin versions of new dependencies:

* make sure your working copy is clean and buildout has successfully
  been run.

* empty versions.cfg:

    echo -n > versions.cfg

* let buildout suggest versions.cfg contents:

    ./bin/buildout -N > versions.cfg 2>&1

* crop versions.cfg to contain only the lines starting from and
  including '[versions]'

* compare to previous version:

    git diff versions.cfg

* edit versions.cfg to suit your taste

* run buildout again; if successful, commit


To update all eggs to the latest release:

* delete all versions in versions.cfg, apart from those manually pinned in
  setup.py.

* rerun buildout in newest mode and catch the picked versions ::

    bin/buildout -n > output

* copy the versions from the last line of the output file to versions.cfg


To update only minor releases:

* run checkversion script and catch the picked versions ::

    bin/checkversions -l 2 > output

* read output and manually update the versions in versions.cfg


python/buildout.cfg
-------------------

You may want to modify the version of Pillow here if needed.
