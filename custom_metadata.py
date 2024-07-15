def get_custom_metadata(info, audio):
    # On utilise la clé 'prompt' déjà présente dans les données JSON
    return {"prompt": info["prompt"]}