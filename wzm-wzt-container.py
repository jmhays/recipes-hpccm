r"""
Wzm-Wzt simulations
Contents:
    Ubuntu 18.04 (default)
    CUDA version 10.1 (default)
    GNU compilers (upstream)
    OFED (upstream)
    OpenMPI version 2.1.5 (default)
    Gromacs 2019
    gmxapi master
    sample_restraint corr-struct
    wzm_wzt devel
"""

import os
import subprocess
from hpccm.templates.CMakeBuild import CMakeBuild
from hpccm.templates.git import git

Stage0 += comment(__doc__.strip(), reformat=False)
Stage0.name = 'devel'

cuda_version = USERARG.get('CUDA_VERSION', '10.1')
ubuntu_version = USERARG.get('UBUNTU_VERSION', '18.04')
openmpi_version = USERARG.get('OPENMPI_VERSION', '2.1.5')
gcc_version = USERARG.get("GCC_VERSION", '5.4')
gpu = USERARG.get("GMX_GPU", "ON")

if ubuntu_version == "16.04":
    python_version = '3.5'
elif ubuntu_version == '18.04':
    python_version = '3.6'
else:
    python_version = '3.5'

Stage0 += baseimage(image='nvidia/cuda:{}-devel-ubuntu{}'.format(
    cuda_version, ubuntu_version),
                    _as=Stage0.name)

Stage0 += python(devel=True)

compiler = gnu(fortran=False, extra_repository=True, version=gcc_version)
Stage0 += compiler

Stage0 += packages(ospackages=['ca-certificates', 'cmake',
                               'git'])  #, 'python3-pip', 'python-pip'])

Stage0 += ofed()

Stage0 += openmpi(configure_opts=['--enable-mpi-cxx'],
                  prefix="/opt/openmpi",
                  infiniband=True,
                  version=openmpi_version,
                  toolchain=compiler.toolchain)

Stage0 += pip(packages=[
    'setuptools', 'wheel', 'cmake', 'cython', 'numpy', 'mpi4py', 'networkx'
],
              pip="pip3")

Stage0 += environment(
    variables={
        'PYTHONPATH':
        '$PYTHONPATH:/usr/lib/python{}/site-packages:/usr/local/lib/python{}/dist-packages:/builds/gmxapi/build:/builds/sample_restraint/build/src/pythonmodule'
        .format(python_version, python_version),
        'PATH':
        '$PATH:/usr/local/gromacs/bin'
    })

################################################
# GROMACS
################################################
Stage0 += comment("GROMACS 2019")

cm = CMakeBuild()
build_cmds = [
    git().clone_step(repository='https://github.com/gromacs/gromacs',
                     branch='release-2019',
                     path='/builds/gromacs',
                     directory='src'),
    cm.configure_step(directory='/builds/gromacs/src',
                      build_directory='/builds/gromacs/build',
                      opts=[
                          '-DCMAKE_BUILD_TYPE=Release',
                          '-DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda',
                          '-DGMX_BUILD_OWN_FFTW=ON',
                          '-DGMX_GPU={}'.format(gpu), '-DGMX_MPI=OFF',
                          '-DGMX_OPENMP=ON', '-DGMXAPI=ON',
                          '-DMPIEXEC_PREFLAGS=--allow-run-as-root'
                      ]),
    cm.build_step(),
    cm.build_step(target='install'),
    cm.build_step(target='check')
]

Stage0 += shell(commands=build_cmds)

################################################
# gmxapi
################################################
Stage0 += comment("gmxapi master")
cm = CMakeBuild()
build_cmds = [
    git().clone_step(repository='https://github.com/kassonlab/gmxapi',
                     branch='master',
                     path='/builds/gmxapi',
                     directory='src'),
    cm.configure_step(
        directory='/builds/gmxapi/src',
        build_directory='/builds/gmxapi/build',
        opts=[
            "-DPYTHON_EXECUTABLE=`which python3`",
            "-DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.6m.so"
        ]),
    cm.build_step(),
    cm.build_step(target='install')
]

Stage0 += shell(commands=build_cmds)

################################################
# sample_restraint
################################################
Stage0 += comment("sample_restraint")
cm = CMakeBuild()
build_cmds = [
    git().clone_step(repository='https://github.com/jmhays/sample_restraint',
                     branch='corr-struct',
                     path='/builds/sample_restraint',
                     directory='src'),
    cm.configure_step(
        directory='/builds/sample_restraint/src',
        build_directory='/builds/sample_restraint/build',
        opts=[
            "-DPYTHON_EXECUTABLE=`which python3`",
            "-DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.6m.so"
        ]),
    cm.build_step(),
    cm.build_step(target='install')
]

Stage0 += shell(commands=build_cmds)

################################################
# wzm_wzt
################################################
Stage0 += comment("Wzm-Wzt devel")

build_cmds = [
    git().clone_step(repository='https://github.com/jmhays/wzm_wzt',
                     branch='devel',
                     path='/builds/'), "pip3 install /builds/wzm_wzt/"
]
Stage0 += shell(commands=build_cmds)

################################################
# post-processing
################################################

# Include examples if they exist in the build context
if os.path.isdir('recipes/gromacs/examples'):
    Stage0 += copy(src='recipes/gromacs/examples', dest='/workspace/examples')

Stage0 += label(metadata={'wzm_wzt': 'devel'})
Stage0 += comment("Make the TACC directories")
Stage0 += shell(commands=[
    "mkdir -p /scratch /work /home1 /gpfs /corral-repl /corral-tacc /data"
])

Stage0 += comment("Make the comet directories")
Stage0 += shell(commands=["mkdir -p /oasis /projects /scratch"])
Stage0 += workdir(directory='/scratch')
