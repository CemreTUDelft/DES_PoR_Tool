# [DES_PoR_Tool](https://github.com/CemreTUDelft/DES_PoR_Tool)

Developed in 2018 by Cemre Çubukçuoğlu - BK <C.Cubukcuoglu@tudelft.nl> 

This is a Discrete-Event Simulation (DES) tool developed as a parametric CAD program for validating program of requirements (PoR) for hospital space planning. The DES model simulates the procedures of processing of patients treated by doctors, calculating patient throughput and patient waiting times, based on the number of doctors, patient arrivals, and treatment times. In addition, the tool is capable of defining space requirements by taking hospital design standards into account. Using this tool, what-if scenarios and assumptions on the PoR pertaining to space planning can be tested and/or validated. The tool is ultimately meant for reducing patient waiting times and/or increasing patient throughput by checking the match of the layout of a hospital with respect to its procedural operations. This tool is envisaged to grow into a toolkit providing a methodological framework for bringing Operations Research into Architectural Space Planning. The tool is implemented in Python for [Grasshopper3D](https://www.grasshopper3d.com/), a plugin of McNeel's [Rhino3D](https://www.rhino3d.com/) CAD software using the [SimPy library](https://simpy.readthedocs.io/en/latest/).

Graphical Abstract: 
![alt text][logo]

[logo]: https://github.com/CemreTUDelft/DES_PoR_Tool/blob/master/DES_GraphicalAbstract.jpg "Logo Title Text 2"

The procedure run by the tool can be described as the following:
```
Begin
	Put the simulation settings
	Create DES model
		Create patient arrivals
		Create treatment process using GH inputs
		Run the simulation
	Get the outputs of DES

	Calculate space requirements for each unit
		Formulations using GH inputs and hospital design standards
	Get the outputs of PoR
End
```
