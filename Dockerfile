FROM buildpack-deps:jessie
MAINTAINER Joseph Crotty <josephcrotty@gmail.com>

RUN apt-get update \
    && apt-get install -y cmake \
                          fonts-freefont-ttf \
                          gfortran \
                          libatlas-base-dev \
                          libopenjpeg5 \
                          libvtk5-dev \
                          python-dev \
                          python-pip \
                          python-tk \
                          python-vtk \
                          swig \
                          tcl-vtk \
    && rm -rf /var/lib/apt/lists/*

#ENV GDCM_VERSION 2.6.2

#RUN cd /tmp \
    #&& wget "https://downloads.sourceforge.net/project/gdcm/gdcm%202.x/GDCM%20${GDCM_VERSION}/gdcm-${GDCM_VERSION}.tar.bz2" \
    #&& tar xvf "gdcm-${GDCM_VERSION}.tar.bz2" \
    #&& rm "gdcm-${GDCM_VERSION}.tar.bz2" \
    #&& mkdir build_files \
    #&& cd build_files \
    #&& cmake -DGDCM_BUILD_SHARED_LIBS=ON \
             #-DGDCM_BUILD_APPLICATIONS=ON \
             #-DGDCM_WRAP_PYTHON=ON \
             #-DGDCM_INSTALL_PYTHONMODULE_DIR='/usr/local/lib/python2.7/dist-packages/' \
             #-DGDCM_USE_VTK=ON \
             #"../gdcm-${GDCM_VERSION}" \
    #&& make \
    #&& make install \
    #&& cd /tmp
    #&& rm -rf build_files "gdcm-${GDCM_VERSION}"

#ENV LD_LIBRARY_PATH "/usr/local/lib:$LD_LIBRARY_PATH"

# Optimixed for volume mounting on Mac YMMV
RUN groupadd -r imagen \
    && useradd -r -m -g imagen imagen \
    && usermod -u 1000 imagen \
    && usermod -G staff imagen

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY bin/ /usr/src/app/bin/
COPY images/ /usr/src/app/images/
RUN chown -R imagen:imagen /usr/src/app

COPY entrypoint.sh /
RUN chown imagen:imagen /entrypoint.sh

#USER imagen

CMD ["/entrypoint.sh"]
