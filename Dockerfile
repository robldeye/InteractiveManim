FROM docker.io/manimcommunity/manim:v0.19.0

# Switch to root to install packages
USER root

RUN pip install --no-cache-dir \
    jupyterlab \
    jupyterlab_execute_time \
    jupyterlab_widgets \
    ipywidgets

# Makes pydub happy
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Switch back to the Manim user
ARG NB_USER=manimuser
USER ${NB_USER}

# Copy the repo content into the working directory
COPY --chown=manimuser:manimuser . /manim