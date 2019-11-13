# campi4

## docker run
```
docker run -d -v /dev:/dev --name name -p 5994:5994 campi4:tag     
```
doker image: https://hub.docker.com/r/agrasagar/campi4     
#### example : docker run -d -v /dev:/dev --name tryMe -p 5994:5994 campi4:v1

## app usage
check swagger doc.     

run webserver using command:     
```
python app.py (it will run webserver on localhost on port 5994)     
then go to http://0.0.0.0:5994/swagger/     
```
