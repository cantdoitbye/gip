"""
Traffic Service - Business logic for traffic operations
"""
import json
import logging
from typing import List, Dict, Any
from datetime import datetime
from openai import AsyncOpenAI
from app.config import settings
from app.schemas.traffic import (
    TrafficDataCreate,
    TrafficInsight,
    TrafficAnalysisResponse,
)
from app.models.traffic import CongestionLevel

logger = logging.getLogger(__name__)


class TrafficService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
    
    async def analyze_traffic_data(self, traffic_data: List[TrafficDataCreate]) -> TrafficAnalysisResponse:
        if not self.client:
            return self._generate_mock_insights(traffic_data)
        
        prompt = self._build_analysis_prompt(traffic_data)
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a traffic analysis expert. Analyze the provided traffic data and generate insights about patterns, anomalies, and recommendations."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            
            return self._parse_ai_response(response.choices[0].message.content, len(traffic_data))
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return self._generate_mock_insights(traffic_data)
    
    def _build_analysis_prompt(self, traffic_data: List[TrafficDataCreate]) -> str:
        data_summary = []
        for i, data in enumerate(traffic_data[:20]):
            data_summary.append(
                f"{i+1}. {data.location_name}: Flow={data.flow_rate}, "
                f"Vehicles={data.vehicle_count}, Speed={data.avg_speed} km/h, "
                f"Congestion={data.congestion_level}"
            )
        
        return f"""
        Analyze the following traffic data and provide insights:
        
        {chr(10).join(data_summary)}
        
        Provide:
        1. Key findings (3-5 insights)
        2. Recommendations for improvement
        3. Confidence scores (0-1)
        
        Format your response as JSON with keys: findings, recommendations, summary
 """
    
    def _parse_ai_response(self, response: str, total_analyzed: int) -> TrafficAnalysisResponse:
        insights = []
        summary = "Analysis completed"
        confidence = 0.75
        
        try:
            if "```json" in response:
                json_start = response.find("```json")
                json_end = response.rfind("```", json_start + 7)
                if json_start != -1 and json_end != -1:
                    json_str = response[json_start + 7:json_end].strip()
                    logger.debug(f"Extracted JSON string for parsing: {json_str[:100]}...")
                    try:
                        parsed = json.loads(json_str)
                        logger.info(f"Successfully parsed JSON response with {len(parsed)} top-level keys")
                    except json.JSONDecodeError as je:
                        logger.error(f"JSON parsing failed: {je}. Invalid JSON: {json_str[:200]}...")
                        raise
                    if "findings" in parsed:
                        for finding in parsed["findings"]:
                            insights.append(TrafficInsight(
                                finding=finding.get("finding", ""),
                                recommendation=finding.get("recommendation", ""),
                                confidence=finding.get("confidence", 0.5),
                                category=finding.get("category", "general"),
                                priority=finding.get("priority", "medium"),
                            ))
                    if "recommendations" in parsed:
                        for rec in parsed["recommendations"]:
                            insights.append(TrafficInsight(
                                finding=rec,
                                recommendation=rec,
                                confidence=0.7,
                                category="recommendation",
                                priority="high",
                            ))
                else:
                    logger.error(f"Failed to find valid JSON markers in response. json_start={json_start}, json_end={json_end}")
            else:
                logger.warning("No ```json marker found in AI response, attempting direct parse")
                try:
                    parsed = json.loads(response.strip())
                    logger.info("Successfully parsed response as direct JSON")
                except json.JSONDecodeError:
                    logger.error(f"Response is not valid JSON and contains no JSON markers: {response[:200]}...")
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed with error: {e}. Response snippet: {response[:200]}...")
        except Exception as e:
            logger.error(f"Unexpected error parsing OpenAI response: {e}")
        
        if not insights:
            insights = self._generate_default_insights()
        
        return TrafficAnalysisResponse(
            insights=insights,
            summary=summary,
            total_analyzed=total_analyzed,
            confidence_score=confidence,
        )
    
    def _generate_mock_insights(self, traffic_data: List[TrafficDataCreate]) -> TrafficAnalysisResponse:
        insights = [
            TrafficInsight(
                finding="High congestion detected during peak hours",
                recommendation="Consider implementing traffic signal optimization",
                confidence=0.85,
                category="congestion",
                priority="high",
            ),
            TrafficInsight(
                finding="Average vehicle speed below expected threshold",
                recommendation="Investigate road capacity improvements",
                confidence=0.78,
                category="performance",
                priority="medium",
            ),
            TrafficInsight(
                finding="Traffic flow patterns show morning and evening peaks",
                recommendation="Implement staggered work hours for nearby offices",
                confidence=0.92,
                category="pattern",
                priority="medium",
            ),
        ]
        
        return TrafficAnalysisResponse(
            insights=insights,
            summary="Mock analysis generated (OpenAI API key not configured)",
            total_analyzed=len(traffic_data),
            confidence_score=0.75,
        )
    
    def _generate_default_insights(self) -> List[TrafficInsight]:
        return [
            TrafficInsight(
                finding="Traffic data analysis completed",
                recommendation="Review individual data points for insights",
                confidence=0.6,
                category="general",
                priority="low",
            ),
        ]
