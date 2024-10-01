#!/usr/bin/env python3
"""
## What is it?
The script exports all pages from the drawio schemes to images in the desired format(default - png).  
The original app can't export all pages at once (support only PDF, IDKW).
```
-a, --all-pages                    export all pages (for PDF format only)
```
So, drawio-exporter parses the XML and exports the images step-by-step.  
Now you can export all diagrams in the desired format(png, jpg, svg, vsdx, and xml).


## Usage
```
# drawio-exporter.py --help
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


# tree --charset=ascii
.
|-- mnsk
|   `-- scheme_mnsk.drawio
`-- sngk
    `-- scheme_sngk.drawio

2 directories, 2 files


# /opt/scripts/drawio-exporter.py -x mnsk/scheme_mnsk.drawio,sngk/scheme_sngk.drawio
2022-05-11 18:14:01,153 | INFO~: Exporting images from - [/opt/scripts/test/mnsk/scheme_mnsk.drawio]
2022-05-11 18:14:01,155 | INFO~: Directory [/opt/scripts/test/mnsk/images] created
2022-05-11 18:14:05,938 | INFO~: Image exported: l1_core, path - [/opt/scripts/test/mnsk/images/scheme_mnsk.drawio_l1_core.png]
2022-05-11 18:14:09,810 | INFO~: Image exported: l2_core, path - [/opt/scripts/test/mnsk/images/scheme_mnsk.drawio_l2_core.png]
2022-05-11 18:14:13,647 | INFO~: Image exported: ebgp, path - [/opt/scripts/test/mnsk/images/scheme_mnsk.drawio_ebgp.png]
2022-05-11 18:14:17,268 | INFO~: Image exported: mirroring, path - [/opt/scripts/test/mnsk/images/scheme_mnsk.drawio_mirroring.png]
2022-05-11 18:14:20,477 | INFO~: Image exported: revizor, path - [/opt/scripts/test/mnsk/images/scheme_mnsk.drawio_revizor.png]
2022-05-11 18:14:23,999 | INFO~: Image exported: l1_subdis, path - [/opt/scripts/test/mnsk/images/scheme_mnsk.drawio_l1_subdis.png]
2022-05-11 18:14:27,469 | INFO~: Image exported: oob, path - [/opt/scripts/test/mnsk/images/scheme_mnsk.drawio_oob.png]
2022-05-11 18:14:27,470 | INFO~: Exporting images from - [/opt/scripts/test/sngk/scheme_sngk.drawio]
2022-05-11 18:14:27,472 | INFO~: Directory [/opt/scripts/test/sngk/images] created
2022-05-11 18:14:31,136 | INFO~: Image exported: l1_core, path - [/opt/scripts/test/sngk/images/scheme_sngk.drawio_l1_core.png]
2022-05-11 18:14:34,824 | INFO~: Image exported: l2_core, path - [/opt/scripts/test/sngk/images/scheme_sngk.drawio_l2_core.png]


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

## Homepage
https://github.com/Savamoti/docker-drawio-exporter
"""

import xml.etree.ElementTree as ET
import sys
import os
import subprocess
import logging
import argparse


DRAWIO_APP = "xvfb-run -a /usr/bin/drawio {} --no-sandbox"


def absolute_paths(files):
    """Find absolute paths for files.

    Args:
        files (list): list of files with relative path

    Returns:
        list: files with absolute paths
    """
    abs_paths = []
    for file in files:
        abs_path = os.path.abspath(file)
        if not os.path.isfile(abs_path):
            logging.error(f"File [{abs_path}] doesn't exist")
            return False, []
        abs_paths.append(abs_path)
    return True, abs_paths


def parse_pages(file):
    """Parse drawio schemes to find pages.

    Args:
        file (str): filename of drawio scheme with absolute path

    Returns:
        list: list of dictionaries with page info
    """
    try:
        tree = ET.parse(file)
    except ET.ParseError:
        logging.error("Invalid format file, must be XML")
        return False, []
    pages = []
    for count, child in enumerate(tree.getroot()):
        pages.append(
            {
                "page_index": str(count),
                "page_name": child.attrib["name"].lower(),
            }
        )
    return True, pages


def export_image(file, args):
    """Export all images from drawio scheme.

    Args:
        file (str): path to drawio scheme
        args (argparse namespace): all arguments

    Returns:
        bool: is export was successfull?
    """
    status, pages = parse_pages(file)
    if not status:
        return False
    for page in pages:

        # Check if export image directory exist
        path_export_dir = os.path.join(os.path.dirname(file), "images")
        if not os.path.exists(path_export_dir):
            os.makedirs(path_export_dir)
            logging.info(f"Directory [{path_export_dir}] created")

        # Set export image name
        page_name = f"{os.path.basename(file)}_{page['page_name']}.{args.format}"
        path_exported_page_name = os.path.join(path_export_dir, page_name)

        if args.transparent:
            command = DRAWIO_APP.format(
                f"--export {file} "
                f"--format {args.format} "
                f"--scale {args.scale} "
                f"--quality {args.quality} "
                f"--border {args.border} "
                f"--output {path_exported_page_name} "
                f"--page-index {page['page_index']} "
                "--transparent "
            )
        else:
            command = DRAWIO_APP.format(
                f"--export {file} "
                f"--format {args.format} "
                f"--scale {args.scale} "
                f"--quality {args.quality} "
                f"--border {args.border} "
                f"--output {path_exported_page_name} "
                f"--page-index {page['page_index']} "
            )
        output = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
        # Is command succesfully executed?
        if output.returncode != 0:
            logging.error(f"Command is failed - [{command}], reason: {output.stderr}")
            return False
        logging.info(
            f"Image exported: {page['page_name']}, path - [{path_exported_page_name}]"
        )
    return True


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Drawio image exporter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-x",
        "--export",
        metavar="",
        required=True,
        help="drawio scheme(or list of schemes separated by commas without spaces)",
    )
    parser.add_argument(
        "-f",
        "--format",
        metavar="",
        default="png",
        help="output file type [png, jpg, svg, vsdx, xml]",
    )
    parser.add_argument(
        "-s",
        "--scale",
        metavar="",
        default="2",
        help="scales the diagram size [1=100%%, 2=200%%]",
    )
    parser.add_argument(
        "-t",
        "--transparent",
        action="store_true",
        default=False,
        help="set transparent background for PNG",
    )
    parser.add_argument(
        "-q",
        "--quality",
        metavar="",
        default="100",
        help="output image quality for JPEG",
    )
    parser.add_argument(
        "-b",
        "--border",
        metavar="",
        default="0",
        help="sets the border width around the diagram",
    )
    args = parser.parse_args()
    return args


def main():
    # Logging settings
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s~: %(message)s",
    )

    args = parse_arguments()
    status, files = absolute_paths(args.export.split(","))
    if not status:
        sys.exit(1)

    for file in files:
        logging.info(f"Exporting images from - [{file}]")
        if not export_image(file, args):
            sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
