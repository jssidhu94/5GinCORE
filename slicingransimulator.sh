docker pull rohankharade/gnbsim:develop
docker pull rohankharade/ueransim:latest
docker pull rdefosseoai/oai-gnb:develop
docker pull rdefosseoai/oai-nr-ue:develop

docker image tag rohankharade/gnbsim:develop gnbsim:latest
docker image tag rohankharade/ueransim:latest ueransim:latest
docker image tag rdefosseoai/oai-gnb:develop oai-gnb:develop
docker image tag rdefosseoai/oai-nr-ue:develop oai-nr-ue:develop
