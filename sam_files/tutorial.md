# Preparing dataset for fine-tuning S.A.M. model

We’ll explain how to proceed with the creation of the dataset to fine-tune our S.A.M. model !

We have four main steps : 

1) Filtering the scrapped dataset to a dataframe (.csv)
2) Creation of JSON files (.json)
3) Downloading and renaming the audio files (.mp3)
4) Verifying audio files, JSON files and dataframe

## 0) Create your path variables
- in Google Colab:
  - secrets :
    - YOUR_PATH_TO_SAM={after/mounting/grive/to/S.A.M}
    - GITHUB_PROFILE_NAME={your-github-profile-name}
- in local (downloaded repository) :
  - create .env in /sam_files :
    - GITHUB_PROFILE_NAME={your-github-profile-name}

## 1) Filtering the scrapped dataset to a dataframe (.csv)

a) Open and run [Cleaning and filtering scrapped dataset.ipynb](changer)

## 2) Creation of JSON files (.json)

a) Open and run [Creating JSON files.ipynb](changer)

## 3) Downloading and renaming the audio files (.mp3)

a) Open and run [Downloading and renaming the audio files (.mp3).ipynb](changer)
