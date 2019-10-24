FROM python:3

COPY ./requirements.txt /requirements.txt

COPY ./configs/tap_config_surveymonkey.json /configs/tap_config_surveymonkey.json
COPY ./configs/properties_surveymonkey.json /configs/properties_surveymonkey.json
COPY ./configs/config-stitch.json /configs/config-stitch.json

RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r requirements.txt

ENTRYPOINT ["bash"]
