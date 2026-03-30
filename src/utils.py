import os

def detect_lead_language(lead):
    """
    Inteligencia de Lenguaje v2026:
    Detecta si el lead debe ser contactado en Inglés o Español.
    """
    website = lead.get('website', '').lower()
    location = lead.get('location', '').lower()
    name = lead.get('name', '').lower()
    
    # Marcadores de Español (ES/Latam)
    spanish_tlds = ['.es', '.mx', '.ar', '.cl', '.co', '.pe', '.uy', '.py', '.bo', '.ec', '.ve']
    spanish_locations = ['spain', 'madrid', 'barcelona', 'mexico', 'argentina', 'colombia', 'peru', 'chile']
    
    # Si el dominio termina en un TLD de habla hispana -> ES
    if any(website.endswith(tld) for tld in spanish_tlds):
        return 'ES'
    
    # Si la ubicación menciona un país/ciudad de habla hispana -> ES
    if any(loc in location for loc in spanish_locations):
        return 'ES'
    
    # Miami Hybrid: Si la ubicación es Miami pero el nombre tiene palabras en español -> ES/EN Mix (Default to EN for professionalism)
    if 'miami' in location:
        # Podríamos añadir detección de palabras clave en el nombre aquí
        return 'EN'
        
    # Default global para Dubai, London, NYC, etc.
    return 'EN'
