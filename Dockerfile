FROM docker.io/manimcommunity/manim:v0.19.0

USER root
RUN pip install notebook

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG NB_USER=manimuser
USER ${NB_USER}

COPY --chown=manimuser:manimuser . /manim