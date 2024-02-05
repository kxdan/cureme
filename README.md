# cureme
regular run:
C:\code\cureme>python manage.py runserver


docker:

python manage.py collectstatic
^ needed before a docker build

docker build -t curemetogether .

docker build --build-arg OPENAI_API_KEY=%OPENAI_API_KEY% -t curemetogether .


docker login curemecontainerregistry.azurecr.io -u curemecontainerregistry -p <redacted>

docker tag curemetogether:latest curemecontainerregistry.azurecr.io/curemetogether:latest

docker push curemecontainerregistry.azurecr.io/curemetogether:latest
