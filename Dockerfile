FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main


#Install conda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output miniconda.sh
ENV CONDA_DIR /opt/conda
RUN bash miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

# configure conda
RUN conda config --add channels defaults &&\
    conda config --add channels bioconda &&\
    conda config --add channels conda-forge

# Install tb-profiler
RUN . /opt/conda/etc/profile.d/conda.sh &&\
    conda activate base &&\
    conda create -n profiler tb-profiler&&\
    conda activate profiler

COPY wf /root/wf

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN  sed -i 's/latch/wf/g' flytekit.config
RUN python3 -m pip install --upgrade latch
WORKDIR /root
ENV LATCH_AUTHENTICATION_ENDPOINT https://nucleus.latch.bio
