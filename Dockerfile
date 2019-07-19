FROM gitlab-registry.cern.ch/swan/docker-images/dev-jupyter
USER root
RUN git clone https://github.com/techtocore/jupyter.git
RUN cd jupyter
RUN mv -f templates /opt/conda/lib/python3.7/site-packages/notebook/
RUN cd swancontents && pip install --no-deps .
RUN jupyter nbextension install --py --system swancontents
RUN git clone https://github.com/techtocore/Jupyter-Package-Manager.git
RUN cd Jupyter-Package-Manager/extension
RUN python -m pip install -e .
RUN jupyter nbextension install --py packagemanagerextension --system --symlink
RUN jupyter nbextension enable packagemanagerextension --system --py
RUN jupyter serverextension enable --py --system packagemanagerextension
USER $NB_UID