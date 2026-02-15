def generate_startup_code(instance):
    industry_id = instance.industry_id
    location_id = instance.location_id
    
    return f"{industry_id}{location_id}{instance.id}"
