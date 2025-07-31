FROM docker.io/manimcommunity/manim:v0.19.0

# Switch to root to install packages
USER root

RUN pip install --no-cache-dir \
    jupyterlab \
    voila \
    jupyterlab_execute_time \
    jupyterlab_widgets \
    ipywidgets

# Copy Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Switch back to the Manim user
ARG NB_USER=manimuser
USER ${NB_USER}

# Copy the repo content into the working directory
COPY --chown=manimuser:manimuser . /manim