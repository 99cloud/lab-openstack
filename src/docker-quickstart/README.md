- Build

        $ docker build --tag=friendlyhello .

        $ docker image ls
        REPOSITORY            TAG                 IMAGE ID
        friendlyhello         latest              326387cea398

- Run

        docker run -p 4000:80 friendlyhello
        
        $ curl http://localhost:4000
        <h3>Hello World!</h3><b>Hostname:</b> 8fc990912a14<br/><b>Visits:</b> <i>cannot connect to Redis, counter disabled</i>

- Run Daemon & Stop

        $ docker run -d -p 4000:80 friendlyhello

        $ docker container ls
        CONTAINER ID        IMAGE               COMMAND             CREATED
        1fa4ab2cf395        friendlyhello       "python app.py"     28 seconds ago

        $ docker container stop 1fa4ab2cf395

- Debugging
    - `docker run -it -p 80:80 --entrypoint /bin/bash friendlyhello`
    - `docker run -it friendlyhello python`
- Push & Pull
    
        docker login
        docker tag friendlyhello maodouzi/get-started:part2
        docker push maodouzi/get-started:part2
        // pull
        docker run -p 4000:80 maodouzi/get-started:part2
