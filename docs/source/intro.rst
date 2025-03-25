************
Introduction
************

``CST-Python-API`` is an object-oriented Python package which aims to provide a
programmatic interface to control `CST Microwave Studio`_ with the goal of
automating the generation of 3D models, execution of simulations and
post-treatment of the results.

This tool is developed at the `IETR`_ laboratory (France), as part of the
`HERMES`_ platform. Its source code is hosted `here
<https://gitlab.insa-rennes.fr/hermes/cst-python-api>`_.

The current version of ``CST-Python-API`` is 0.1.1 (*Hanter dro*).

.. _CST Microwave Studio: https://www.cst.com
.. _IETR: https://www.ietr.fr/en
.. _HERMES: https://www.ietr.fr/en/platform-hermes

Why *Hanter dro*?
=================

This tool has been developed at `INSA Rennes`_, an engineering school in France
which is part of the IETR laboratory. As indicated by its name, INSA Rennes is
based in the city of Rennes, the capital city of the `Region of Brittany
<https://en.wikipedia.org/wiki/Brittany>`_.

Brittany is a region with a very rich culture, which draws from its Celtic
heritage. One of the manifestations of this culture are the traditional dances
from Brittany, which are commonly danced by people of all age at the *fest noz*
and *fest deiz* (Breton names for, respectively, "night party" and "day party").
An example of a *fest noz* can be found in `this video
<https://www.youtube.com/watch?v=gI78xl35CPs>`_.

With the goal of contributing to the dissemination of the folklore from Brittany
worldwide, we have decided to give to each version of ``CST-Python-API`` the name
of a traditional Breton dance. For this initial release, we have chosen the
dance called *hanter dro*. *Hanter* can be translated to English as "half", and
*dro* as "turn". This is the very first dance that we are taught when we begin
to learn Breton dance, and for this reason we decided that it would an
appropriate choice for the first release of ``CST-Python-API``. `Here
<https://www.youtube.com/watch?v=uKigVwaGvOg>`_ you can find a tutorial for
learning this dance!

.. _INSA Rennes: https://www.insa-rennes.fr/graduate-school-of-engineering.html

Limitations
===========

CST Microwave Studio is a complex tool with many features. Although the
long-term goal of ``CST-Python-API`` is to provide a complete interface for all
of them, the tool us currently in an early stage of development. For this
reason, only the most common features are supported at this moment.

Our goal is to keep developing the tool, adding new features periodically. If
there is a particular feature that you would like to see implemented, do not
hesitate to open an issue at the `GitLab page of the project
<https://gitlab.insa-rennes.fr/hermes/cst-python-api/-/issues>`_.

``CST-Python-API`` is only available for Windows systems. Although we believe
that this should not be a problem since the vast majority of CST users make use
of Windows machines, in the future we would like to make the tool usable in
GNU-Linux operating systems too.