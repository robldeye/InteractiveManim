FROM docker.io/manimcommunity/manim:v0.19.0

USER root
RUN pip install --no-cache-dir \
    notebook \
    jupyter_contrib_nbextensions \
    jupyter-nbextensions-configurator \
    voila && \
    jupyter contrib nbextension install --sys-prefix --overwrite && \
    jupyter nbextensions_configurator enable --sys-prefix && \
    jupyter nbextension enable execute_time/main --sys-prefix && \
    jupyter nbextension enable hide_input_all/main --sys-prefix

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG NB_USER=manimuser
USER ${NB_USER}

COPY --chown=manimuser:manimuser . /manim