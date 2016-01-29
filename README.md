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

To run dumbox from the container:
```bash
$ docker run -it --rm --name imagen-dumbox -w /usr/src/app imagendumbox_python python dumbox.py images/vhf.159.dcm -v
(0008, 0008) Image Type                          CS: ['ORIGINAL', 'PRIMARY', 'AXIAL']
(0008, 0012) Instance Creation Date              DA: '20050726'
(0008, 0013) Instance Creation Time              TM: '103913'
...
```

# ToDo/Tech Debt
1.  Standard CLI Python arg parser package. Check/validate args.
2.  Autopep*8 my intial code effort
3.  Yikes, the Docker images is nearly 1GB. Shrink? Sigh, maybe not
    worth the effort.
4.  Should DICOM images be viewable from Docker container using pydicom
    methods?
5.  Learn how to deal with compressed vs uncompressed DICOM images.
6.  Is there check if file is DICOM (e.g., .dcm file extension)?
7.  Not exactly a fan of storing images in a repo. GitHub LFS maybe?
