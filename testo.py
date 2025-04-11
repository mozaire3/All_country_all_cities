import requests

def get_countries():
    # Récupérer une liste de pays depuis Overpass (Filtrer les zones géographiques)
    query = """
    [out:json];
    area[admin_level=2];
    out body;
    """
    url = "http://overpass-api.de/api/interpreter"
    
    try:
        response = requests.post(url, data={'data': query})
        
        if response.status_code == 200:
            data = response.json()  # Récupérer la réponse en JSON
            countries = data['elements']
            country_list = [{"country": country['tags'].get('name', 'N/A'), "country_code": country['id']} for country in countries]
            return country_list
        else:
            print(f"Error: Unable to fetch countries. Status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return []

def get_osm_cities(country_code):
    # URL de la requête Overpass API pour récupérer les villes d'un pays spécifique
    query = f"""
    [out:json];
    area(id:{country_code});
    (
      node["place"="city"](area);
    );
    out body;
    """
    url = "http://overpass-api.de/api/interpreter"
    
    try:
        response = requests.post(url, data={'data': query})
        
        if response.status_code == 200:
            data = response.json()  # Récupérer la réponse en JSON
            cities = data['elements']
            city_list = [{"city": city['tags'].get('name', 'N/A'), "lat": city['lat'], "lng": city['lon']} for city in cities]
            return city_list
        else:
            print(f"Error: Unable to fetch data. Status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return []

# Fonction principale pour tester
def main():
    # Étape 1: Obtenir la liste des pays
    countries = get_countries()
    
    print("Liste des pays :")
    for idx, country in enumerate(countries):
        print(f"{idx + 1}. {country['country']}")
    
    # Demander à l'utilisateur de choisir un pays
    choice = int(input("Choisissez un pays (numéro): ")) - 1
    
    if 0 <= choice < len(countries):
        selected_country = countries[choice]
        print(f"Vous avez sélectionné: {selected_country['country']}")
        
        # Étape 2: Obtenir les villes pour le pays sélectionné
        cities = get_osm_cities(selected_country['country_code'])
        
        if cities:
            print(f"Villes dans {selected_country['country']}:")
            for city in cities:
                print(f"{city['city']} (Latitude: {city['lat']}, Longitude: {city['lng']})")
        else:
            print("Aucune ville trouvée pour ce pays.")
    else:
        print("Choix invalide.")

# Lancer la fonction principale
if __name__ == "__main__":
    main()
