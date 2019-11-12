# campi4

## docker run
docker run -d -v /dev:/dev --name name -p 5994:5994 campi4:tag     
doker image: https://hub.docker.com/r/agrasagar/campi4     
#### example : docker run -d -v /dev:/dev --name tryMe -p 5994:5994 campi4:v1

## app usage
make GET requests to http://ip_of_pi:5994/snap/:device_number
parameters

imageName (optional): name of image. Should end with ext jpg. (default:image(device_number).jpg)
colorSpace (optional): RGB, HSV, YUV (default:RGB)
