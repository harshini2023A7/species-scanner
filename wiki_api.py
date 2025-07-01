import requests

def get_species_info(species_name):
    base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
    response = requests.get(base_url + species_name.replace(" ", "_"))
    
    if response.status_code == 200:
        data = response.json()
        summary = data.get("extract", "").lower()

        # Detect plant or animal
        if any(word in summary for word in ["plant", "tree", "flower", "leaf", "herb", "fruit", "vegetable"]):
            kingdom = "Plantae"
        else:
            kingdom = "Animalia"

        classification = {
            "Kingdom": kingdom,
            "Species": species_name
        }

        return {
            "summary": data.get("extract"),
            "classification": classification
        }

    return None


def get_species_images(species_name):
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&titles={species_name}&pithumbsize=500"
    response = requests.get(search_url)

    if response.status_code == 200:
        pages = response.json().get("query", {}).get("pages", {})
        image_urls = []
        for page in pages.values():
            if "thumbnail" in page:
                image_urls.append(page["thumbnail"]["source"])
        return image_urls

    return []
