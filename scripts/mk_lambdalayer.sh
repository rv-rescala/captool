rm -rf python
rm -rf py37-captool.zip
pyenv global 3.7.7
rm -rf python
mkdir -p python
pip install -r requirements.txt -t ./python
zip -r py37-captool.zip python/
aws s3 cp py37-captool.zip s3://libs-lambda/py37/