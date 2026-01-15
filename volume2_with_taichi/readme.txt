Run the main file to start the program. The main.py file controls which scene is rendered — simply uncomment the render function you want

If you encounter errors related to Cython, install it using pip install cython. After installation, build the Cython extensions by running python setup.py build_ext --inplace in the project directory, then run the program again.

You can change whether the program runs on CPU or GPU by editing the architecture setting inside the render() function in camera.py. For example, switching between ti.init(arch=ti.cuda) and ti.init(arch=ti.cpu) allows you to choose the backend
