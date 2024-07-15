To add submodule
```bash
git submodule add https://github.com/mage-ai/mlops.git
```
Go to the mlops directory, in my case this is `orchestration/mlops`
```bash
cd mlops
```
To start up Mage
```bash
./scripts/start.sh
```

Open [`http://localhost:6789`](http://localhost:6789) in your browser.

If you use VS Code, you can move the data from your data directory into mlops directory. If not, you can  launch the terminal on Mage and follow these commands
```bash
mkdir -p ~/.kaggle
mv ~/mental_health_mlops_project/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```
Then
```bash
kaggle datasets download -d ruchi798/stress-analysis-in-social-media 
unzip ../../data/stress-analysis-in-social-media.zip -d you_data_directory 
```

Note, in the requirements.txt file, add `nltk` as one of the packages to be installed

Create a project on Mage

Add some files to the utils folder (`mlops/utils/*`) cleaning and feature engineering [links]. You can do `Command + .` on MacOS, to launch the command center and then click text editor. Thereafter, right click on the text editor to create the files.

Create a data_peparation pipeline in that project and create data loaders, transformers and exporters using the files [list files] respectively. Create a Global Data Product(GDP) for the training set in data_preparation so you wouldn't need to load the data everytime.


Create an sklearn training pipeline and use the training set GDP to load the data.  Create a custom code block to load the model [link], a transformer for hyperparameter tuning[link], and a data exporter to run the on the entire data(training data in this case) on the models, and return those.

To get the dashboard, create the file analytics/data.py using this [code]. Create a new dashboard, select custom code, and add the code snippet

```python
from mlops.utils.analytics.data import data_load

# https://docs.mage.ai/visualizations/dashboards

@data_source
def data(*args, **kwargs):
    return data_load()
```
Select accuracy and group on model. You should be able to see the plot below. If the number of columns keeps running with no end, run the check [link], in the sklearn_pipeline to see what error is preventing the code from running.





