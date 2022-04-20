## TypeSQL

## Haoran quick start

python 3.8.8, pytorch 1.9.0

python -u train.py --sd saved_model_kg > hzz5361_train.log 2> hzz5361_train.err &
python -u test.py --sd saved_model_kg > hzz5361_train.log 2> hzz5361_train.err 


## TODO


Merge



https://github.com/lyuqin/HydraNet-WikiSQL/blob/master/modeling/base_model.py#L59


to


https://github.com/NelsonDaniel/typesql/blob/py3.7/typesql/model/sqlnet.py#L384



#### Environment Setup

1. The code uses Python 3.7 and Pytorch 1.11.0 GPU.
3. Install dependencies: `conda env create -f environment.yml`

#### Download Data and Embeddings

1. Download the zip data file at the [Google Drive](https://drive.google.com/file/d/1CGIRCjwf2bgmWl3UyjY1yJpP4nU---Q0/view?usp=sharing), and put it in the root dir.
2. Download the pretrained [Glove](https://nlp.stanford.edu/data/wordvecs/glove.42B.300d.zip) and the [paraphrase embedding](https://drive.google.com/file/d/1iWTowxEG1-KZyq-fHP6cb6dNqMh4eHiN/view?usp=sharing) `para-nmt-50m/data/paragram_sl999_czeng.txt`. Put the unziped glove and para-nmt-50m folders in the root dir.

#### Train Models

1. To use knowledge graph types:
```
  mkdir saved_model_kg
  python train.py --sd saved_model_kg
```

2. To use DB content types:
```
   mkdir saved_model_con
   python train.py --sd saved_model_con --db_content 1
```

#### Test Models

1. Test Model with knowledge graph types:
```
python test.py --sd saved_model_kg
```
2. Test Model with knowledge graph types:
```
python test.py --sd saved_model_con --db_content 1
```

#### Get Data Types

1. Get a Google Knowledge Graph Search API Key by following the [link](https://developers.google.com/knowledge-graph/)
2. Search knowledge graph to get entities:
```
python get_kg_entities.py [Google freebase API Key] [input json file] [output json file]
```
3. Use detected knowledge graph entites and DB content to group questions and create type attributes in data files:
```
python data_process_test.py --tok [output json file generated at step 2] --table TABLE_FILE --out OUTPUT_FILE [--data_dir DATA_DIRECTORY] [--out_dir OUTPUT_DIRECTORY]

python data_process_train_dev.py --tok [output json file generated at step 2] --table TABLE_FILE --out OUTPUT_FILE [--data_dir DATA_DIRECTORY] [--out_dir OUTPUT_DIRECTORY]
```

#### Acknowledgement

The implementation is based on [SQLNet](https://github.com/xiaojunxu/SQLNet). Please cite it too if you use this code.
