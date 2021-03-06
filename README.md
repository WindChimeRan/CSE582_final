## TypeSQL

## thoughts

The problem I found:

https://arxiv.org/pdf/2008.04759.pdf the execuation-guided decoding is described in page 9. 
There are two parts of decoding: 1. Get top-k1 predicted aggregation-SELECT pairs, 2. Get top-k2 predicted conditions

However, according to their code in 
https://github.com/lyuqin/HydraNet-WikiSQL/blob/master/modeling/base_model.py#L59

They only argmax the top1 possible aggregation-SELECT. The 2nd part is fine. In other words, they only implement half of what they said. 

Should we implement the first part by ourselves? Maybe, maybe not. According to the experiments part of typesql, the most challenging prediction is the condition or where clauses. Then choosing the top1 select part may not be a sub-optimal idea. 

Another problem: The paper argues that their algorithm is a kind of beam search, while I don't think so. 

A general definition of beam search: https://en.wikipedia.org/wiki/Beam_search
general beam search in a nutshell: It's a greedy algorithm, and does not gurantee global optimal solution. 
NLP beam search in a nutshell: Instead of enumerating all possible prediction of sequence, beam search keeps a fix-size cache of topk local optimal solution until 1, 2, 3 ... n, and gradually expand it to the whole sequence. 

In fact, the algorithm in the paper enumerate all possible predictions of the conditions. Then I don't think it's a beam search.



## Haoran quick start

python 3.8.8, pytorch 1.9.0

    pip install records==0.5.2
    pip install SQLAlchemy==1.1.14


    python -u train.py --sd saved_model_kg > hzz5361_train.log 2> hzz5361_train.err &

    python -u test.py --sd saved_model_kg > hzz5361_train.log 2> hzz5361_train.err 

or run 

    bash run_test.sh

## Original model, epoch 10


{'agg': 3, 'sel': 2, 'conds': [[0, 2, 'a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a']]}
{'agg': 3, 'sel': 1, 'conds': []}



    Dev acc_qm: 0.6435866983372922;
      breakdown on (agg, sel, where): [0.89928741 0.92541568 0.75486936 0.96377672 0.89287411 0.98087886
    0.91733967]
    Dev execution acc: 0.7098574821852731
    Test acc_qm: 0.6385967122252315;
      breakdown on (agg, sel, where): [0.89884739 0.91572715 0.74894501 0.96290231 0.88454998 0.98066385
    0.92082887]
    Test execution acc: 0.7052339862694463

## typesql with execution-guided decoding

    Dev acc_qm: 0.994418052256532;
      breakdown on (agg, sel, where): [0.99916865 0.99809976 0.9956057  0.99916865 0.997981   0.99976247
    0.99869359]
    Dev execution acc: 0.7098574821852731
    Test acc_qm: 0.9942054544309379;
      breakdown on (agg, sel, where): [0.99829943 0.99924419 0.99609498 0.99911822 0.99817346 0.99974806
    0.99905524]
    Test execution acc: 0.7052339862694463

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
