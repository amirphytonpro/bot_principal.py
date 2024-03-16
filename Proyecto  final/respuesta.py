import wikipedia


def get_wikipedia_summary(query):
    try:
        wikipedia.set_lang("es")
        # Ajustar el número de oraciones
        summary = wikipedia.summary(query, sentences=3)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Hubo un error al procesar la solicitud: {e}"
    except wikipedia.exceptions.PageError as e:
        return f"No se encontraron resultados para esta consulta: {e}"
    except Exception as e:
        return f"Hubo un error al procesar la solicitud: {e}"
