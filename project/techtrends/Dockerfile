FROM python:3.8

# set working directory
WORKDIR /

# add all the files
ADD . . 

# install dependencies
RUN pip install -r requirements.txt 

# expose the port
EXPOSE 3111

# start the application
CMD ["python", "init_db.py"]
CMD ["python", "app.py"]