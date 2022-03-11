docker pull rohankharade/gnbsim:develop
docker pull rohankharade/ueransim:latest
#docker pull rdefosseoai/oai-gnb:develop
#docker pull rdefosseoai/oai-nr-ue:develop
docker pull rdefosseoai/oai-amf:v1.3.0
docker pull rdefosseoai/oai-nrf:v1.3.0
docker pull rdefosseoai/oai-spgwu-tiny:v1.1.5
docker pull rdefosseoai/oai-smf:v1.3.0
docker pull rdefosseoai/oai-udr:v1.3.0
docker pull rdefosseoai/oai-udm:v1.3.0
docker pull rdefosseoai/oai-ausf:v1.3.0
docker pull rdefosseoai/oai-upf-vpp:v1.3.0
docker pull rdefosseoai/oai-nssf:v1.3.0
docker pull mysql:5.7
docker pull redfoot/webserver:ubuntu

docker image tag rdefosseoai/oai-amf:v1.3.0 oai-amf:latest
docker image tag rdefosseoai/oai-nrf:v1.3.0 oai-nrf:latest
docker image tag rdefosseoai/oai-smf:v1.3.0 oai-smf:latest
docker image tag rdefosseoai/oai-spgwu-tiny:v1.1.5 oai-spgwu-tiny:latest
docker image tag rdefosseoai/oai-udr:v1.3.0 oai-udr:latest
docker image tag rdefosseoai/oai-udm:v1.3.0 oai-udm:latest
docker image tag rdefosseoai/oai-ausf:v1.3.0 oai-ausf:latest
docker image tag rdefosseoai/oai-upf-vpp:v1.3.0 oai-upf-vpp:latest
docker image tag rdefosseoai/oai-nssf:v1.3.0 oai-nssf:latest
docker image tag redfoot/ubuntu:webserver ubuntu:webserver


docker image tag rohankharade/gnbsim:develop gnbsim:latest
docker image tag rohankharade/ueransim:latest ueransim:latest
#docker image tag rdefosseoai/oai-gnb:develop oai-gnb:develop
#docker image tag rdefosseoai/oai-nr-ue:develop oai-nr-ue:develop
