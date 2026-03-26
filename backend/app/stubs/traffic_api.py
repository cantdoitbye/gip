"""
Traffic API Stub Service - Mock data simulating government traffic APIs
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.models.traffic import CongestionLevel, IncidentType, IncidentSeverity


LOCATIONS = [
    {"name": "MG Road Junction", "lat": 17.3850, "lng": 78.4867},
    {"name": "Parade Grounds", "lat": 17.4065, "lng": 78.4699},
    {"name": "Begumpet Metro", "lat": 17.3988, "lng": 78.5551},
    {"name": "Hitech City", "lat": 17.4473, "lng": 78.3763},
    {"name": "Gachibowli Junction", "lat": 17.4299, "lng": 78.4532},
    {"name": "Kukatpally Junction", "lat": 17.4615, "lng": 78.3546},
    {"name": "Miyapur X Roads", "lat": 17.4967, "lng": 78.3916},
    {"name": "Secunderabad Industrial Area", "lat": 17.5234, "lng": 78.5367},
    {"name": "Shamshabad Airport Road", "lat": 17.3312, "lng": 78.3541},
    {"name": "Outer Ring Road", "lat": 17.4157, "lng": 78.4342},
]


class TrafficAPIStub:
    def __init__(self):
        self.last_update = datetime.now()
        self.cached_data: Dict[str, Any] = {}
    
    def generate_traffic_flow(self, location: Dict) -> Dict[str, Any]:
        base_flow = random.uniform(800, 2500)
        hour_factor = self._get_hour_factor()
        
        flow_rate = base_flow * hour_factor
        vehicle_count = int(flow_rate * random.uniform(2.5, 4.0))
        avg_speed = max(20, 80 - flow_rate * 0.03)
        
        congestion = self._calculate_congestion(flow_rate, vehicle_count, avg_speed)
        
        return {
            "location_name": location["name"],
            "latitude": location["lat"],
            "longitude": location["lng"],
            "flow_rate": round(flow_rate, 2),
            "vehicle_count": vehicle_count,
            "avg_speed": round(avg_speed, 1),
            "congestion_level": congestion,
            "timestamp": datetime.utcnow(),
        }
    
    def _get_hour_factor(self) -> float:
        hour = datetime.now().hour
        if 7 <= hour <= 10:
            return 1.5
        elif 11 <= hour <= 14:
            return 0.8
        elif 17 <= hour <= 20:
            return 1.3
        else:
            return 0.6
    
    def _calculate_congestion(self, flow_rate: float, vehicle_count: int, avg_speed: float) -> str:
        ratio = vehicle_count / max(avg_speed, 1)
        if ratio < 15:
            return CongestionLevel.low.value
        elif ratio < 25:
            return CongestionLevel.medium.value
        elif ratio < 40:
            return CongestionLevel.high.value
        else:
            return CongestionLevel.severe.value
    
    def get_all_traffic_data(self) -> List[Dict[str, Any]]:
        now = datetime.now()
        if (now - self.last_update).total_seconds() > 300:
            self._refresh_data()
        
        return list(self.cached_data.values())
    
    def _refresh_data(self) -> None:
        for location in LOCATIONS:
            self.cached_data[location["name"]] = self.generate_traffic_flow(location)
        self.last_update = datetime.now()
    
    def generate_incident(self, location: Dict) -> Dict[str, Any]:
        incident_types = [IncidentType.accident, IncidentType.construction, IncidentType.congestion, IncidentType.roadwork]
        severities = [IncidentSeverity.minor, IncidentSeverity.moderate, IncidentSeverity.severe]
        
        return {
            "location_name": location["name"],
            "latitude": location["lat"] + random.uniform(-0.002, 0.002),
            "longitude": location["lng"] + random.uniform(-0.002, 0.002),
            "incident_type": random.choice(incident_types).value,
            "severity": random.choice(severities).value,
            "description": self._generate_incident_description(random.choice(incident_types).value),
            "timestamp": datetime.utcnow(),
        }
    
    def _generate_incident_description(self, incident_type: str) -> str:
        descriptions = {
            IncidentType.accident.value: [
                "Minor collision reported",
                "Multi-vehicle accident on main road",
                "Vehicle breakdown blocking lane",
            ],
            IncidentType.construction.value: [
                "Road construction in progress",
                "Bridge maintenance work ongoing",
                "Utility work causing delays",
            ],
            IncidentType.congestion.value: [
                "Heavy traffic due to peak hour",
                "Congestion extending from junction",
                "Bottleneck at traffic signal",
            ],
            IncidentType.roadwork.value: [
                "Pothole repair work",
                "Road resurfacing project",
                "Lane marking in progress",
            ],
        }
        return random.choice(descriptions.get(incident_type, ["No description available"]))
    
    def get_incidents(self, limit: int = 10) -> List[Dict[str, Any]]:
        if random.random() < 0.3:
            return []
        
        num_incidents = random.randint(0, min(limit, 3))
        locations = random.sample(LOCATIONS, num_incidents)
        incidents = []
        for loc in locations:
            incidents.append(self.generate_incident(loc))
        
        return incidents
    
    def get_heatmap_data(self) -> List[Dict[str, Any]]:
        traffic_data = self.get_all_traffic_data()
        heatmap = []
        for data in traffic_data:
            intensity = 0.0
            congestion = data["congestion_level"]
            if congestion == CongestionLevel.low.value:
                intensity = 0.2
            elif congestion == CongestionLevel.medium.value:
                intensity = 0.5
            elif congestion == CongestionLevel.high.value:
                intensity = 0.8
            else:
                intensity = 1.0
            
            heatmap.append({
                "location_name": data["location_name"],
                "lat": data["latitude"],
                "lng": data["longitude"],
                "intensity": intensity,
            })
        
        return heatmap


traffic_api_stub = TrafficAPIStub()
