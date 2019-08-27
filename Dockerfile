FROM gitlab-registry.cern.ch/swan/docker-images/dev-jupyter

LABEL maintainer="Akash Ravi <akashkravi@gmail.com>"

USER root

RUN git clone https://github.com/techtocore/jupyter.git
RUN cd jupyter && \
rm -rf /opt/conda/lib/python3.7/site-packages/notebook/templates && \
cp -rl templates /opt/conda/lib/python3.7/site-packages/notebook/ && \
ls && \
cd SwanContents && pip install --no-deps . && \
jupyter nbextension install --py swancontents --system

RUN git clone https://github.com/Anaconda-Platform/nb_conda_kernels.git
RUN cd nb_conda_kernels && \
cat requirements.txt | xargs -n 1 pip install || true && \
pip install -e . && \
python -m nb_conda_kernels.install --enable && \
cd ..

RUN git clone https://github.com/techtocore/Jupyter-Package-Manager.git
RUN cd Jupyter-Package-Manager/extension && \
git checkout swan-integration && \
yarn install && \
yarn run webpack && \
python -m pip install -e . && \
jupyter nbextension install --py packagemanager --system --symlink && \
jupyter nbextension enable packagemanager --system --py && \
jupyter serverextension enable --py --system packagemanager

USER $NB_UID

EXPOSE 8888/tcp