FROM amazon/aws-glue-libs:glue_libs_4.0.0_image_01

USER root
RUN groupadd --g 1024 groupcontainer
RUN usermod -a -G groupcontainer glue_user

USER glue_user
WORKDIR /home/glue_user/workspace
COPY ../poetry.lock ../pyproject.toml ${WORKDIR}

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.6.1

ENV PACKAGE="${WORKDIR}/helpers"
ENV PYTHONPATH="${PYTHONPATH}:$PACKAGE"
ENV PATH="/home/glue_user/.local/bin:$PATH"


RUN python3 -m pip install --upgrade pip --user
COPY ../src/glue ${WORKDIR}

# Give write permission incase of any permission issues
USER root
RUN chown -R glue_user:groupcontainer /home/glue_user/workspace
USER glue_user