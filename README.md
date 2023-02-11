# Molecule Clicker
Manual position labelling program. Train a monkey to click on interesting features to get the coordinates of the clicks.

## Installation
To get started, follow these steps. Unless otherwise noted, all paths are relative to project's root directory. If you have Make installed, simply

1. Clone this repo.
1. Run `make install`.

If you don't have Make installed, you can follow these steps instead.

1. Clone this repo.
1. Create a virtual environment.
```bash
python3 -m venv venv
```
1. Install project and requirements.
```bash
pip install -r requirements.txt
pip install -e .
```

# Examples
```bash
python get_image_coords.py test.jpg 100 192
```

arg[1]: 'test.jpg': the image to open

arg[2]: 100: the size of the image, in this case 100 nm x 100 nm

arg[3]: 192: the pixel resolution of the image, in this case 192 x 192

This command opens up 'test.jpg' so you can click on points in the canvas. After you are done clicking, press esc and the positions will be written to a file positions.txt.