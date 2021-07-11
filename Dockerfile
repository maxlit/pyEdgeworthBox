FROM jupyter/minimal-notebook
COPY requirements.txt requirements.txt
# Clone a repository (my website in this case)
RUN git clone https://gitlab.com/maxlit/powerindex.git
RUN cd powerindex
RUN pip3 install -r requirements.txt