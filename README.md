# Legos

Our data is from the [Amsterdam Library of Object Images (ALOI)](https://aloi.science.uva.nl/)

To choose an object go to:  
`ALOI Collection` > `Object Images` > `[img]` and click on any image 


# Setting up the venv

```bash
$ python3 -m venv /path/to/venv
$ . /path/to/venv/bin/activate
$ pip install -r requirements.txt
```

# Part 1 - Mosaics

```bash
$ apt install python3-pip
$ pip install opencv-python
$ python3 threshold.py
$ pip install pillow
$ pip install matplotlib
$ python3 mosaic.py
```

This will produce 3 files:
```
mosaicCup.jpg
mosaicDucc.jpg
mosaicshoo.jpg
```

# Part 2 - Voxels

Open [lego_voxels.ipynb in Google Colab](https://colab.research.google.com/github/Kevin-Lyy/CVFinalProject/blob/master/lego_voxels.ipynb) ([Github file here](/lego_voxels.ipynb))  

## To Run 

More detailed instructions are available in the file itself

1. Run the pip installs  (the cell below **Installs**)
2. **Restart the runtime** so the installs work correctly - you *will* get errors otherwise
3. **Run all cells** 
4. Navigate to the **Run** cell 
5. Modify **`lego_image`** and **`lego_image_deg`** (the cell below **Run**) as instructed, then run all cells below to see results
