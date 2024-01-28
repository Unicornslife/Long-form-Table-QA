model_current = None
api_key = None
organization = None

def set_global_config(model, key, org):
    global model_current, api_key, organization
    model_current = model
    api_key = key
    organization = org
