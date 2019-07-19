r"""
Cuda 10.1 + Ubuntu 18.04 + OpenMPI 2.1.5
Contents:
    Ubuntu 18.04
    CUDA version 10.1
    GNU compilers (upstream)
    OFED (upstream)
    OpenMPI version 2.1.5
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment
# pylama: ignore=E0602
import os

Stage0 += comment(__doc__.strip(), reformat=False)
Stage0.name = 'devel'
Stage0 += baseimage(image='nvidia/cuda:10.1-devel-ubuntu18.04', _as=Stage0.name)

Stage0 += python(devel=True)

compiler = gnu(fortran=False)
Stage0 += compiler

Stage0 += packages(ospackages=['ca-certificates', 'cmake', 'fftw3', 'git', 'python3-pip', 'python-pip'])

Stage0 += ofed()

pip_packages = ['setuptools', 'wheel', 'cmake', 'cython', 'numpy', 'mpi4py', 'networkx']
pip_commands = ['pip3 install {}'.format(package) for package in pip_packages]

Stage0 += openmpi(configure_opts=['--enable-mpi-cxx'],
               prefix="/opt/openmpi", infiniband=True, version='2.1.5', toolchain=compiler.toolchain)

Stage0 += shell(commands=pip_commands)

Stage0 += label(metadata={'Base for gmxapi on Rivanna': '0.0.7'})

Stage0 += workdir(directory='/scratch')
