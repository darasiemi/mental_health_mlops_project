from mlops.utils.analytics.data import data_load

# https://docs.mage.ai/visualizations/dashboards

@data_source
def data(*args, **kwargs):
    return data_load()