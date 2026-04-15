from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
 
ext_modules = [
    Pybind11Extension(
        "simulation_engine",
        sources=[
            "core/src/KDTree.cpp",
            "core/src/RouteEngine.cpp",
            "core/bindings.cpp",
        ],
        include_dirs=["core/include"],
        cxx_std=17,
    ),
]
 
setup(
    name="simulation_engine",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)