What is open-frame32
=================
open-frame32 is an open source software for modeling and perform structural analysis.
This software can be used to compute structure's response such as
deformation and internal force.

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


Todo
====
* Store data using PyTables
* Simple drawing using openGL
* Analysis for Truss 3D
* Point load with specific angle

License
=======
This software is using BSD 3-clause license. In other words, you
can use, distribute, even sell it without any restriction. But, you
must include the copyright notice, the license, and the following
disclaimer.
