FROM nvcr.io/nvidia/pytorch:23.01-py3
WORKDIR /workdir
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r code/requirements.txt
COPY . /workdir/code
