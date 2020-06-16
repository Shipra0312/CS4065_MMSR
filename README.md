# CSGO_highlight

For this project, we would like to extraction CSGO highlights. 
The dataset is obtained from mediaeval19 gamestory workshop.

##Installation
TODO:Mention requirements.txt and pyAudioAnalysis

## Folders and scripts
```methods``` contains notebooks for all methods we have tried. For these implementations, notebooks are explained and plots are shown to support decisions.

```data_extracted```  contains extracted match videos, it can be downloaded here or you can generate it using ```preprocessing/extract_videos.py``` 

```data_raw``` contains original dataset, it can be downloaded here: 

```preprocessing``` Data_Analsysis.ipynb shows some initial exploration on the metadata and some simple stastics on the dataset. extract_series.py extracts intended files to ```data_extracted``` folder. 

```main.py``` main execution of the program, it contains some selected methods from analysis folder.

## Usage
TODO: Mentioned how main.py should be used.