FROM gitlab-registry.cern.ch/swan/docker-images/dev-jupyter
USER root
RUN git clone https://github.com/techtocore/jupyter.git
RUN cd jupyter && \
rm -rf /opt/conda/lib/python3.7/site-packages/notebook/templates && \
cp -rl templates /opt/conda/lib/python3.7/site-packages/notebook/ && \
ls && \
cd SwanContents && pip install --no-deps . && \
jupyter nbextension install --py --system swancontents
RUN git clone https://github.com/techtocore/Jupyter-Package-Manager.git
RUN cd Jupyter-Package-Manager/extension && \
git checkout swan-integration && \
python -m pip install -e . && \
jupyter nbextension install --py packagemanagerextension --system --symlink && \
jupyter nbextension enable packagemanagerextension --system --py && \
jupyter serverextension enable --py --system packagemanagerextension
USER $NB_UID