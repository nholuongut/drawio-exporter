# Drawio Exporter

![](https://i.imgur.com/waxVImv.png)
### [View all Roadmaps](https://github.com/nholuongut/all-roadmaps) &nbsp;&middot;&nbsp; [Best Practices](https://github.com/nholuongut/all-roadmaps/blob/main/public/best-practices/) &nbsp;&middot;&nbsp; [Questions](https://www.linkedin.com/in/nholuong/)

![GitHub language count](https://img.shields.io/github/languages/count/ashleymichaelwilliams/aws-sandbox) ![GitHub top language](https://img.shields.io/github/languages/top/ashleymichaelwilliams/aws-sandbox)<br>
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) ![AquaSec](https://img.shields.io/badge/aqua-%231904DA.svg?style=for-the-badge&logo=aqua&logoColor=#0018A8) !
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) ![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
<br>

## About
The script exports all pages from the drawio schemes to images in the desired format(default - png).  
The original app can't export all pages at once (support only PDF, IDKW).
```
-a, --all-pages                    export all pages (for PDF format only)
```
So, drawio-exporter parses the XML and exports the images step-by-step.  
Now you can export all diagrams in the desired format(png, jpg, svg, vsdx, and xml).

```bash
# docker run --rm -it -w /data -v $(pwd):/data savamoti/drawio-exporter --help
usage: drawio-exporter.py [-h] -x  [-f] [-s] [-t] [-q] [-b]

Drawio image exporter

optional arguments:
  -h, --help         show this help message and exit
  -x , --export      drawio scheme(or list of schemes separated by commas without spaces) (default: None)
  -f , --format      output file type [png, jpg, svg, vsdx, xml] (default: png)
  -s , --scale       scales the diagram size [1=100%, 2=200%] (default: 2)
  -t, --transparent  set transparent background for PNG (default: False)
  -q , --quality     output image quality for JPEG (default: 100)
  -b , --border      sets the border width around the diagram (default: 0)
```

## How-To
Examples

### Run it from your machine
```bash
# tree --charset=ascii
.
|-- mnsk
|   `-- scheme_mnsk.drawio
`-- sngk
    `-- scheme_sngk.drawio

2 directories, 2 files


# docker run --rm -it -w /data -v $(pwd):/data savamoti/drawio-exporter -x mnsk/scheme_mnsk.drawio,sngk/scheme_sngk.drawio
2022-05-11 18:27:14,556 | INFO~: Exporting images from - [/data/mnsk/scheme_mnsk.drawio]
2022-05-11 18:27:14,557 | INFO~: Directory [/data/mnsk/images] created
2022-05-11 18:27:19,396 | INFO~: Image exported: l1_core, path - [/data/mnsk/images/scheme_mnsk.drawio_l1_core.png]
2022-05-11 18:27:22,910 | INFO~: Image exported: l2_core, path - [/data/mnsk/images/scheme_mnsk.drawio_l2_core.png]
2022-05-11 18:27:26,858 | INFO~: Image exported: ebgp, path - [/data/mnsk/images/scheme_mnsk.drawio_ebgp.png]
2022-05-11 18:27:30,447 | INFO~: Image exported: mirroring, path - [/data/mnsk/images/scheme_mnsk.drawio_mirroring.png]
2022-05-11 18:27:33,562 | INFO~: Image exported: revizor, path - [/data/mnsk/images/scheme_mnsk.drawio_revizor.png]
2022-05-11 18:27:37,166 | INFO~: Image exported: l1_subdis, path - [/data/mnsk/images/scheme_mnsk.drawio_l1_subdis.png]
2022-05-11 18:27:40,532 | INFO~: Image exported: oob, path - [/data/mnsk/images/scheme_mnsk.drawio_oob.png]
2022-05-11 18:27:40,533 | INFO~: Exporting images from - [/data/sngk/scheme_sngk.drawio]
2022-05-11 18:27:40,534 | INFO~: Directory [/data/sngk/images] created
2022-05-11 18:27:44,013 | INFO~: Image exported: l1_core, path - [/data/sngk/images/scheme_sngk.drawio_l1_core.png]
2022-05-11 18:27:47,657 | INFO~: Image exported: l2_core, path - [/data/sngk/images/scheme_sngk.drawio_l2_core.png]


# tree --charset=ascii
.
|-- mnsk
|   |-- images
|   |   |-- scheme_mnsk.drawio_ebgp.png
|   |   |-- scheme_mnsk.drawio_l1_core.png
|   |   |-- scheme_mnsk.drawio_l1_subdis.png
|   |   |-- scheme_mnsk.drawio_l2_core.png
|   |   |-- scheme_mnsk.drawio_mirroring.png
|   |   |-- scheme_mnsk.drawio_oob.png
|   |   `-- scheme_mnsk.drawio_revizor.png
|   `-- scheme_mnsk.drawio
`-- sngk
    |-- images
    |   |-- scheme_sngk.drawio_l1_core.png
    |   `-- scheme_sngk.drawio_l2_core.png
    `-- scheme_sngk.drawio

4 directories, 11 files
```

### Use it as a base image for your pipeline
For example Gitlab CI.  
I store schemas in a repository, and when I change them, I'm too lazy to export images.  
When changes are made to the schemas, I want the images to be exported automatically.  
To the same repository.  

1. Prepare an image.
    Create Dockerfile:

    ```dockerfile
    # syntax=docker/dockerfile:1
    FROM savamoti/drawio-exporter:latest
    
    # Change this to your domain, if you use self-hosted gitlab
    ENV GITLAB_DOMAIN "gitlab.com"
    
    # Install soft and dependencies
    RUN apt-get update && apt-get install -y \
        unzip \
        ssh \
        git
    
    # Set keys to interact with the repository without login/password
    # You can create keys specifically for a project in its repository
    COPY .ssh /root/.ssh
    RUN chmod 600 /root/.ssh/* \
        && eval $(ssh-agent -s) \
        && ssh-add /root/.ssh/id_rsa \
        && ssh-keyscan -H ${GITLAB_DOMAIN} >> /root/.ssh/known_hosts
    
    # Fonts
    # Helvetica is a default font in drawio.
    WORKDIR /opt/fonts/
    RUN wget -O helvetica.zip https://boldfonts.com/download/helvetica-font/ \
        && unzip helvetica.zip \
        && rm -rf helvetica.zip \
        && mkdir -p /usr/share/fonts/truetype/helvetica/ \
        && mv * /usr/share/fonts/truetype/helvetica/ \
        && rm -rf /opt/fonts/
    
    # Change the ENTRYPOINT here or in the .gitlab-ci.yml file.
    # ENTRYPOINT [""]
    ```
    
    Build.
    
    ```bash
    docker build -t drawio-exporter .
    ```
    
2. Set **.gitlab-ci.yml** file.

    ```yaml
    image:
      name: drawio-exporter
      entrypoint: ['']
    
    variables:
      EXPORT_OPTIONS: "--format png --scale 2 --quality 100"
    
    default:
      tags:
        - drawio
        - automation
    
    stages:
      - export
    
    export-job:
      only:
        changes:
          - "**/*.drawio"
      stage: export
      before_script:
        - git config --global user.email "noc@example.com"
        - git config --global user.name "CI Pipeline"
        - export CI_PUSH_REPO=`echo $CI_REPOSITORY_URL | perl -pe 's#.*@(.+?(\:\d+)?)/#git@\1:#'`
        - git remote set-url origin $CI_PUSH_REPO
    
      script:
        - export CHANGED_FILES=`git diff --name-only HEAD^ HEAD | grep .drawio$`
        - echo -e "List of changed files:\n$CHANGED_FILES"
        - export CHANGED_FILES_LIST=`echo $CHANGED_FILES | tr ' ' ','`
        - echo "Exporting images from drawio schemes."
        - /opt/scripts/drawio-exporter.py --export $CHANGED_FILES_LIST $EXPORT_OPTIONS
        - echo "Commiting exported images."
        - git add *.png || true
        - git commit -m "Images exported from schemes - $CHANGED_FILES_LIST" || true
        - git push origin HEAD:$CI_COMMIT_REF_NAME || true
    ```

I'm are always open to your feedback.  Please contact as bellow information:
### [Contact ]
* [Name: nho Luong]
* [Skype](luongutnho_skype)
* [Github](https://github.com/nholuongut/)
* [Linkedin](https://www.linkedin.com/in/nholuong/)
* [Email Address](luongutnho@hotmail.com)

![](https://i.imgur.com/waxVImv.png)
![](bitfield.png)
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/nholuong)

# License
* Nho Luong (c). All Rights Reserved.
