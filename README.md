## TypeSQL

## Haoran quick start

python 3.8.8, pytorch 1.9.0

    pip install records==0.5.2
    pip install SQLAlchemy==1.1.14


    python -u train.py --sd saved_model_kg > hzz5361_train.log 2> hzz5361_train.err &

    python -u test.py --sd saved_model_kg > hzz5361_train.log 2> hzz5361_train.err 

or run 

    bash run_test.sh

## Original model, epoch 10

    Dev acc_qm: 0.6435866983372922;
      breakdown on (agg, sel, where): [0.89928741 0.92541568 0.75486936 0.96377672 0.89287411 0.98087886
    0.91733967]
    Dev execution acc: 0.7098574821852731
    Test acc_qm: 0.6385967122252315;
      breakdown on (agg, sel, where): [0.89884739 0.91572715 0.74894501 0.96290231 0.88454998 0.98066385
    0.92082887]
    Test execution acc: 0.7052339862694463

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
