instructions

1. pull the curiobaby_drop repo:

		- git clone https://github.com/langcog/curiobaby_drop


2. pull and install neuroailab/tdw_physics:
	
		- git clone https://github.com/neuroailab/tdw_physics

		- cd to directory where you just pulled to

		- actually install by doing:
				[your_python3] -m pip install -e .

		  or add to your pythonpath 

3. run the controller:
		- cd [/path/to/curiobaby_drop/models] 

		- PYTHONPATH=$PYTHONPATH:/path/to/neuroailab/tdw_physics/target_controllers python3.7 run_script.py

		- if it works, it should put a directory called "curiodrop_stimuli" in the current directory, with various subdirectories each containing written HDF5s 

		- often, on my machine, a failure mode is that it gets stuc around line 173 of tdw_physics/dataset.py,  e.g. 

		       resp = self.communicate(self.get_per_frame_commands(resp, frame))

		    ... it just hangs there permanently.  Whether it gets stuck seems random though. 