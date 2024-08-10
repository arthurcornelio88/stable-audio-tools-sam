# Preparing dataset for fine-tuning S.A.M. model

We’ll explain how to proceed with the creation of the dataset to fine-tune our S.A.M. model !

We have four main steps : 

1) Filtering the scrapped dataset to a dataframe (.csv)
2) Creation of JSON files (.json)
3) Downloading and renaming the audio files (.mp3)
4) Verifying audio files, JSON files and dataframe

## 1) Filtering the scrapped dataset to a dataframe (.csv)

a) Open and run [Cleaning and filtering scrapped dataset.ipynb](changer) in Google Colab (GDrive) or locally (Github Repo)

## 2) Creation of JSON files (.json)

a) Open and run [Creating JSON files.ipynb](changer) in Google Colab (GDrive) or locally (Github Repo)
- Attention to :
  - Local paths
  - Create your .env file in /sam_files, with GITHUB_PROFILE_NAME={your-github-profile-name}
