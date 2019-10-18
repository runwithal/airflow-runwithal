FROM python:3

COPY ./requirements.txt /requirements.txt

RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r requirements.txt

ENTRYPOINT ["bash"]
