"""Healthcare provider service"""
from typing import List, Optional
import json
import os

from app.models import Provider, ProviderRequest
from app.config import settings


def load_mock_providers() -> List[Provider]:
    """Load mock healthcare providers"""
    providers_file = os.path.join(os.path.dirname(__file__), "..", "data", "mock_providers.json")
    
    try:
        with open(providers_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Provider(**provider) for provider in data]
    except FileNotFoundError:
        # Return default mock providers
        return [
            Provider(
                id="1",
                name="City General Hospital",
                type="hospital",
                address="123 Main Street, City, State 12345",
                phone="(555) 123-4567",
                distance=2.5,
                latitude=37.7749,
                longitude=-122.4194
            ),
            Provider(
                id="2",
                name="Community Health Clinic",
                type="clinic",
                address="456 Oak Avenue, City, State 12345",
                phone="(555) 234-5678",
                distance=3.1,
                latitude=37.7849,
                longitude=-122.4094
            ),
            Provider(
                id="3",
                name="Downtown Pharmacy",
                type="pharmacy",
                address="789 Elm Street, City, State 12345",
                phone="(555) 345-6789",
                distance=1.8,
                latitude=37.7649,
                longitude=-122.4294
            ),
            Provider(
                id="4",
                name="Urgent Care Center",
                type="clinic",
                address="321 Pine Road, City, State 12345",
                phone="(555) 456-7890",
                distance=4.2,
                latitude=37.7949,
                longitude=-122.4394
            )
        ]


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates in kilometers (Haversine formula)"""
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)
    
    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c


def get_providers(request: ProviderRequest) -> List[Provider]:
    """Get healthcare providers near the specified location"""
    providers = load_mock_providers()
    
    # Filter by provider type if specified
    if request.provider_type:
        providers = [p for p in providers if p.type == request.provider_type]
    
    # Calculate distances and filter by radius
    for provider in providers:
        if provider.latitude and provider.longitude:
            distance = calculate_distance(
                request.latitude,
                request.longitude,
                provider.latitude,
                provider.longitude
            )
            provider.distance = round(distance, 2)
    
    # Filter by radius and sort by distance
    filtered_providers = [
        p for p in providers
        if p.distance is not None and p.distance <= request.radius
    ]
    filtered_providers.sort(key=lambda x: x.distance or float('inf'))
    
    return filtered_providers


def search_providers_google_maps(request: ProviderRequest) -> List[Provider]:
    """Search providers using Google Maps API (requires API key)"""
    if not settings.maps_api_key:
        # Fallback to mock data
        return get_providers(request)
    
    # TODO: Implement Google Maps API integration
    # This would require the googlemaps library
    # For now, return mock data
    return get_providers(request)

