FROM python:3.8

# set working directory
WORKDIR /

# add all the files
ADD . . 

# install dependencies
RUN pip install -r requirements.txt 
RUN python init_db.py

# expose the port
EXPOSE 3111

# start the application
CMD ["python", "app.py"]