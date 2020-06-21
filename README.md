# CSGO_highlight

For this project, we would like to extraction CSGO highlights. 
The dataset is obtained from mediaeval19 gamestory workshop.

## Installation
Clone the source of this library:

```git clone https://gitlab.ewi.tudelft.nl/cs4065/2019-2020/group-07/csgo_highlight.git```

You may have to install ffmpeg before installing requirement.txt. In Anaconda environment, You can install it with:
 
 ```conda install -c menpo ffmpeg```

Install the dependencies:

```pip install -r ./requirements.txt``` 



## Usage

You can run ```main.py``` using the following commandline:

```python main.py -i input_file -o output_file -t threshold_quantile```

```input_file``` should be the location and mp4 name of the input match video. 

```output_file``` should be the output location/name of the extracted highlight.

```threshold_quantile``` is the threshold used for highlight. For example, if ```threshold_quantile``` is 0.85, the threshold for the arousal curve is ```quantile(arousal_curve, 0.85)```. The default value is set to 0.85. 

An example of this would be: 

```python main.py -i data_extracted/videos/training1.mp4 -o highlights/highlight1.mp4 -t 0.85```

## Folders and scripts
```analysis``` contains notebooks for all methods we have tried/tested. Notebooks are explained and plots are shown to support decisions.

```data_extracted```  contains extracted match videos, it can be downloaded [here](https://drive.google.com/drive/folders/1u1hSfAGRgzRiJD1nyTPb7IAYJKDKyyUI?usp=sharing) or you can generate those videos using ```preprocessing/extract_videos.py``` 

```data_raw``` contains original dataset, it can be downloaded [here](https://drive.google.com/drive/folders/1u1hSfAGRgzRiJD1nyTPb7IAYJKDKyyUI?usp=sharing).

```preprocessing``` Data_Analsysis.ipynb shows some initial exploration on the metadata and some simple statics on the dataset. extract_series.py extracts intended files to ```data_extracted``` folder. 

```src``` src folder contains all methods used for main.py 

```audioBascIO.py``` For some us, pyAudioAnalysis couldn't work due to broken imports in audioBasicIO.py . By adding this piece of code manually, we avoid the problem of broken imports.   

```main.py``` main execution of the program, it contains selected methods from analysis folder.

