What is openSAP32
=================
openSAP32 is open source software for modeling and perform structural analysis.
This software is intended for students and civil engineers (especially
structural engineer) who wants to compute structure's response such as 
deformation and internal force.
Many softwares are created out there but they are good softwares that are too
expensive for me to perform some simple analysis. So this software is born to
satisfy my need and my thirstiness of knowledge in structural analysis.
Right now this software can only be used to perform structural analysis for
some simple structures. There will be GUI (Graphical User Interface), but
that's still a long journey to get there. The development will be focused
to solver engine and writing clean and tidy code.


Features
========
* Structural types:
	* Truss 2D
* Load type:
	* Axial load to node in x and y direction
* Restrain:
	* Fixed
	* Pin
	* Roller (restrained in x or y direction)
	* Add initial settlement 
* Material:
	* Concrete and steel material
* Section:
	* Area must be provided manually (there is not yet method to input dimension of section)
	* Second moment of inertia must be provided manually (there is not yet method to input dimension of section)
* Structure's response
	* Node displacement
	* End Element force
	* Axial Stress

Requirement
===========
* Numpy


Todo
====
* Store data using PyTables
* Simple drawing using openGL
* Analysis for Truss 3D
* Point load with specific angle

About Author
============
My name is Duken Marga Turnip, a bachelor with major civil engineering graduated
from Institut Teknologi Bandung, Indonesia.
I'm very interested at computational on structural engineering and try to study
more of it in my leisure time. You can visit my blog in http://duken.info/
(mostly in Indonesian).

License
=======
This software is using BSD 3-clause license. In other words, you
can use, distribute, even sell it without any restriction. But, you
must include the copyright notice, the license, and the following
disclaimer.
