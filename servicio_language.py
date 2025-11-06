# === SERVICIO 1: LANGUAGE SERVICE ===
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Conexión al servicio
def conectar_language():
    """
    Conecta al servicio de Azure Text Analytics.
    
    Returns:
        TextAnalyticsClient: Cliente de Azure Text Analytics
    """
    key = os.getenv('TEXT_ANALYTICS_KEY')
    endpoint = os.getenv('TEXT_ANALYTICS_ENDPOINT')
    
    if not key or not endpoint:
        raise ValueError("TEXT_ANALYTICS_KEY o TEXT_ANALYTICS_ENDPOINT no están configuradas en las variables de entorno")
        
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Función para analizar texto
def analizar_sentimiento(texto):
    """
    Analiza el sentimiento de un texto utilizando Azure Text Analytics.
    
    Args:
        texto (str): Texto a analizar
        
    Returns:
        dict: Diccionario con los resultados del análisis de sentimiento
    """
    try:
        if not texto or not isinstance(texto, str) or not texto.strip():
            return {
                'sentimiento': 'neutral',
                'puntuaciones': {
                    'positivo': 0.0,
                    'neutral': 1.0,
                    'negativo': 0.0
                },
                'error': 'Texto de entrada no válido'
            }
            
        client = conectar_language()
        
        # Analizar sentimiento
        response = client.analyze_sentiment(
            documents=[texto],
            language="es"
        )
        
        # Procesar resultados
        if response and not response[0].is_error:
            doc = response[0]
            return {
                'sentimiento': doc.sentiment,
                'puntuaciones': {
                    'positivo': doc.confidence_scores.positive,
                    'neutral': doc.confidence_scores.neutral,
                    'negativo': doc.confidence_scores.negative
                }
            }
        else:
            return {
                'sentimiento': 'error',
                'error': f"Error al analizar el texto: {response[0].error if response and hasattr(response[0], 'error') else 'Respuesta inválida'}"
            }
            
    except Exception as e:
        return {
            'sentimiento': 'error',
            'error': f"Error inesperado: {str(e)}"
        }
