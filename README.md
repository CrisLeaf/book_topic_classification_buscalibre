# Book Topic Classification

### Installation

Libraries Required:

- [Numpy](http://www.numpy.org/)
- [Pandas](http://pandas.pydata.org/)
- [Seaborn](http://matplotlib.org/)
- [Matplotlib](http://matplotlib.org/)
- [Scikit-Learn](http://scikit-learn.org/stable/)
- [XGBoost](https://xgboost.readthedocs.io/en/latest/)
- [LightGBM](https://lightgbm.readthedocs.io/en/latest/)
- [CatBoost](https://catboost.ai/)
- [Tensorflow](https://www.tensorflow.org)

Also, you will need to have a software installed to run [Jupyter Notebooks](http://jupyter.org/install.html).


### Dataset

The data was scrapped from a [Buscalibre website](https://www.buscalibre.cl/libros-envio-express-chile_t.html) using the `data_scrapping.py` script.

Feature Columns:
- `isbn`: categorical, the isbn (if available) or isbn13.
- `name`: string, the name of the book.
- `author`: string, the author of the book.
- `publisher`: string, the publisher of the book.
- `year`: numerical, year of publication.
- `language`: string, the language of the book.
- `pages`: numerical, pages of the book.
- `review`: string, the back cover of, almost every, book.
- `price`: numerical, the price of the book.
- `url`: the direct url of the book.

Target Column:
- `Topic`: categorical, label column with 13 different labels.


### Code

The code provided by the `data_analysis_part1.ipynb` and `data_analysis_part2.ipynb` notebook files, describes the Data Exploratory Analysis, being part 1 for all the features except the review column, and part 2 the analysis for the review column.

The notebook `numeric_ml_model.ipynb` shows different models trained using the features extracted from the EDA part.


### Results


Different scores were achieved, being the highest the one obtained by the CatBoost Classifier, with a 0.64 weighted f1 score.