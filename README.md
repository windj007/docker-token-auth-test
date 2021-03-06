# docker-token-auth-test
A minimal setup needed to test Docker Registry authentication via JWT (Bearer) token with Django and PyJWT-based authentication server

## Installation

    git clone https://github.com/windj007/docker-token-auth-test
    cd docker-token-auth-test
    wget -O docker-compose-1.5.2 https://github.com/docker/compose/releases/download/1.5.2/docker-compose-`uname -s`-`uname -m`
    wget -O docker-compose-1.7.1 https://github.com/docker/compose/releases/download/1.7.1/docker-compose-`uname -s`-`uname -m`
    chmod +x docker-compose-*
    sudo usermod -aG docker ${USER}
    exit # have to logout for usermod to be effective


## How to reproduce bug with token unmarshalling

    # First, install old docker 1.9.0 and run test
    sudo aptitude purge docker-engine
    sudo aptitude install docker-engine=1.9.0-0~jessie # or another variant for 1.9.0
    ./docker-compose-1.5.2 up &> docker-1.5.2.log &
    ./run_test.sh # must succeed
    ./docker-compose-1.5.2 stop
    docker images -aq | xargs docker rmi -f

    # Second, install new docker and run test again
    sudo aptitude purge docker-engine
    sudo aptitude install docker-engine=1.11.1-0~jessie # or another variant for 1.11.1
    ./docker-compose-1.7.1 up &> docker-1.7.1.log &
    ./run_test.sh # must fail with cannot unmarshal string to Go type int
    ./docker-compose-1.7.1 stop
    docker images -aq | xargs docker rmi -f

    # Check Docker daemon logs (client-side)
    tail -100 /var/log/daemon.log # should contain something like level=error msg="Upload failed, retrying: unable to decode token response: json: cannot unmarshal string into Go value of type int"
    
    # To get auth_server logs and the generated token, please run
    tail docker-1.7.1.log
