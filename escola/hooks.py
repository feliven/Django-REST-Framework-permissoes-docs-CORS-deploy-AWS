def custom_version_hook(result, generator, request, public):
    """
    Hook de pós-processamento do drf-spectacular para ajustar dinamicamente
    o campo 'version' no OpenAPI info de acordo com a versão ativa (v1 ou v2).
    """
    api_version = generator.api_version or (
        getattr(request, "version", None) if request else None
    )
    versions_map = {
        "v1": "1.0.0",
        "v2": "2.0.0",
    }
    if api_version in versions_map:
        result["info"]["version"] = versions_map[api_version]
    return result
