"""
Process M.tb whole genome sequencing data to predict lineage and drug-resistance
"""

import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile, LatchDir
import os


@small_task
def Tbprofiler_task(fastq_file1: LatchFile, fastq_file2: LatchFile, out_dir: LatchDir) -> LatchDir:

    # A reference to our output.

    local_dir = "/root/tbprofiler/"
    local_prefix = os.path.join(local_dir, "pfiles")

    # Defining the command 

    _tbprofiler_cmd = [
        "tb-profiler",
        "profile",
        "-1",
        fastq_file1.local_path,
        "-2",
        fastq_file2.local_path,
        "-p",
        str(local_prefix),
        "--txt"

    ]

    subprocess.run(_tbprofiler_cmd, check=True)

    return LatchFile(str(local_dir), out_dir.remote_path)


@workflow
def profiler(fastq_file1: LatchFile, fastq_file2: LatchFile, out_dir: LatchDir) -> LatchDir:
    """Process M.tb whole genome sequencing data to predict lineage and drug-resistance


    __metadata__:
        display_name: Process M.tb whole genome sequencing data to predict lineage and drug-resistance

        author:
            name: GeOdette

            email: steveodettegeorge@gmail.com

            github:
        repository: https://github.com/GeOdette/tbprofiler.git

        license:
            id: MIT

    Args:

        fastq_file1:
          Paired-end read 1 file to be analyzed

          __metadata__:
            display_name: FASTQ File 1

        fastq_file2:
          Paired-end read 2 file to be analyzed.

          __metadata__:
            display_name: FASTQ File 2

        out_dir:
          Output Directory. *Tip, create a directory at the latch console

          __metadata__:
            display_name: Output Directory
    """
    return Tbprofiler_task(fastq_file1=fastq_file1, fastq_file2=fastq_file2, out_dir=out_dir)
