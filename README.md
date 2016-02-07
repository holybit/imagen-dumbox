# imagen-dumbox
Python [DICOM](http://dicom.nema.org/) file manipulator. For development
it is recommended to use [Docker](https://www.docker.com/). [Docker
Toolbox](https://www.docker.com/docker-toolbox) is the easiest way to
run docker locally and supports both Windows and Mac. Also, be sure to
install [Docker Compose](https://docs.docker.com/compose/).

St. Thomas Aquinas was viewed by youth peers as the "dumb ox."

# Development
Use Docker compose to build images.

```bash
$ docker-compose build
```

Run dumbox from the host CLI or exec into the container:
```bash
# host
$ docker run -it --rm --name imagen-dumbox -w /usr/src/app imagendumbox_python python dumbox.py -h
# exec
$ docker-compose up -d
$ docker exec -it imagendumbox_python bash
$ bin/dumbox.py -h
```

# Mac/Window VTK
VTK can be used but requires additional host configuration.

## Mac VTK
Install [socat](http://brewformulas.org/Socat) with [brew](http://brew.sh/) and [XQuartz](http://www.xquartz.org/).

```bash
# Open XQuartz from Desktop or CLI as below
# If a GUI app already bound to XQuartz and XQuartz was subsequently
# closed start socat first and then relaunch XQuartz
$ open -a XQuartz
# XQuartz -> Preferences -> Security -> Check Allow connections from
# network clients

# Ensure Bash is not setting DISPLAY in a profile
# After lanching XQuartz start a new terminal and check DISPLAY
$ echo $DISPLAY
/private/tmp/com.apple.launchd.9NpgnYjOME/org.macosforge.xquartz:0
$ socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\" &

# Ensure your docker-comopse.yml file has correct environment DISPLAY
# If running Docker Machine IP of 'ifconfig vboxnet1'
$ docker-compose up -d
```

# ToDo/Tech Debt
1.  Standard CLI Python arg parser package. Check/validate args.
2.  Autopep*8 my intial code effort
3.  Yikes, the Docker images is nearly 1GB. Shrink? Sigh, maybe not
    worth the effort.
4.  Should DICOM images be viewable from Docker container using pydicom
    methods?
5.  Learn how to deal with compressed vs uncompressed DICOM images.
    JPEG2000 is not supported out of box by pydicom, but GDCM does.
6.  Is there check if file is DICOM (e.g., .dcm file extension)?
7.  Not exactly a fan of storing images in a repo. GitHub LFS maybe?
