To add submodule
```bash
git submodule add https://github.com/mage-ai/mlops.git
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

Then create two files cleaning and feature engineering [links]

