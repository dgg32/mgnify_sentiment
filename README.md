# mgnify_sentiment


  
# Introduction

This repo contains code for the my article in Medium (Borrow Text Analysis for Metagenome Sample Typing).

# Prerequisite

XGBoost

Sklearn

SHAP



# Usage
1. First dowload taxonomic profiles from MGnify with ebi_donwload_all_taxonomy.py:
```console
python ebi_download_all_taxonomy.py [habitat_string] [json_output_folder]
```

For example, to download the taxonomic profiles for soils:
```console
python ebi_download_all_taxonomy.py root:Environmental:Terrestrial:Soil /home/sih13/Downloads/sentiment/
```

2. Convert the json files into text files
```console
python convert_json_to_txt.py [json_output_folder] [test_output_folder]
```

3. ebi_sentiment_multi_value.ipynb contains my machine learning workflow for project.

## Authors

  

*  **Sixing Huang** - *Concept and Coding*

  

## License

  

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
