"""
Smart Job Categorizer and Cost Estimator

Automatically categorizes jobs by tradesperson type and estimates costs
based on typical job characteristics when actual time tracking is not available.
"""

import pandas as pd
import re
from typing import Dict, Tuple, List
from config import DEFAULT_MARKET_RATES, DEFAULT_INHOUSE_RATES


class SmartJobCategorizer:
    """
    Intelligently categorizes jobs by analyzing titles and descriptions
    """
    
    # Keywords for identifying electrician jobs
    ELECTRICIAN_KEYWORDS = [
        'electric', 'light', 'bulb', 'socket', 'outlet', 'switch', 'wiring', 
        'wire', 'fuse', 'circuit', 'breaker', 'power', 'pat test', 'pattest',
        'voltage', 'electrical', 'lamp', 'spotlight', 'led'
    ]
    
    # Keywords for plumber jobs
    PLUMBER_KEYWORDS = [
        'plumb', 'pipe', 'drain', 'toilet', 'sink', 'tap', 'faucet', 'leak',
        'water', 'shower', 'bath', 'drainage', 'blocked', 'clog', 'overflow',
        'cistern', 'radiator', 'boiler', 'heating'
    ]
    
    # Keywords for HVAC/heating jobs
    HVAC_KEYWORDS = [
        'hvac', 'heating', 'cooling', 'air con', 'aircon', 'ac unit', 
        'ventilation', 'thermostat', 'boiler', 'radiator', 'temperature',
        'heat', 'cold', 'warm'
    ]
    
    # Keywords for carpenter jobs
    CARPENTER_KEYWORDS = [
        'door', 'cabinet', 'shelf', 'wood', 'timber', 'frame', 'hinge',
        'handle', 'drawer', 'cupboard', 'wardrobe', 'desk', 'table',
        'skirting', 'architrave', 'assembly', 'assemble', 'install'
    ]
    
    # Keywords for painter/decorator jobs
    PAINTER_KEYWORDS = [
        'paint', 'decor', 'wall', 'ceiling', 'emulsion', 'gloss', 'varnish',
        'stain', 'redecorate', 'touch up', 'repaint', 'decorative',
        'wallpaper', 'ceiling', 'magnolia'
    ]
    
    # Keywords for landscaper/groundwork jobs
    LANDSCAPER_KEYWORDS = [
        'garden', 'grass', 'lawn', 'hedge', 'tree', 'shrub', 'outdoor',
        'outside', 'ground', 'landscap', 'paving', 'path', 'drive',
        'fence', 'gate', 'soil', 'plant', 'weed'
    ]
    
    # Keywords for handyman/small jobs
    HANDYMAN_KEYWORDS = [
        'fix', 'repair', 'broken', 'loose', 'stuck', 'squeaky', 'adjust',
        'tighten', 'replace', 'small', 'minor', 'quick', 'simple',
        'hang', 'mount', 'move', 'shift'
    ]
    
    # Keywords for equipment/specialist jobs
    EQUIPMENT_KEYWORDS = [
        'hoist', 'lift', 'equipment', 'machine', 'appliance', 'device',
        'system', 'gear', 'mechanism', 'apparatus', 'wheelchair',
        'mobility', 'specialist'
    ]
    
    def __init__(self):
        """Initialize the categorizer"""
        pass
    
    def categorize_job(self, title: str, category: str = None, description: str = None) -> str:
        """
        Categorize a job based on title, existing category, and description
        
        Args:
            title: Job title
            category: Existing category from jobs list
            description: Job description/notes
            
        Returns:
            Task type (electrician, plumber, hvac_technician, carpenter, 
                      painter, landscaper, general_handyman, or other)
        """
        # Combine all text for analysis
        text = str(title or '').lower()
        if description and isinstance(description, str):
            text += ' ' + description.lower()
        
        # Use existing category if it maps directly
        if category and isinstance(category, str):
            category_lower = category.lower()
            if 'electric' in category_lower:
                return 'electrician'
            elif 'plumb' in category_lower:
                return 'plumber'
            elif 'decorat' in category_lower or 'paint' in category_lower:
                return 'painter'
            elif 'assembly' in category_lower or 'carpenter' in category_lower:
                return 'carpenter'
            elif 'ground' in category_lower or 'landscap' in category_lower:
                return 'landscaper'
            elif 'fire' in category_lower:
                return 'other'  # Fire safety often requires specialists
        
        # Analyze text for keywords (weighted scoring)
        scores = {
            'electrician': self._count_keywords(text, self.ELECTRICIAN_KEYWORDS),
            'plumber': self._count_keywords(text, self.PLUMBER_KEYWORDS),
            'hvac_technician': self._count_keywords(text, self.HVAC_KEYWORDS),
            'carpenter': self._count_keywords(text, self.CARPENTER_KEYWORDS),
            'painter': self._count_keywords(text, self.PAINTER_KEYWORDS),
            'landscaper': self._count_keywords(text, self.LANDSCAPER_KEYWORDS),
            'general_handyman': self._count_keywords(text, self.HANDYMAN_KEYWORDS),
            'other': self._count_keywords(text, self.EQUIPMENT_KEYWORDS)
        }
        
        # Get the category with highest score
        max_score = max(scores.values())
        
        # If score is very low, it's probably a handyman job or unknown
        if max_score < 2:
            # Check if it's a small/simple job
            if any(word in text for word in ['small', 'quick', 'simple', 'minor']):
                return 'general_handyman'
            return 'other'
        
        # Return the highest scoring category
        for task_type, score in scores.items():
            if score == max_score:
                return task_type
        
        return 'other'
    
    def _count_keywords(self, text: str, keywords: List[str]) -> int:
        """Count how many keywords appear in the text"""
        count = 0
        for keyword in keywords:
            if keyword in text:
                count += 1
        return count


class JobCostEstimator:
    """
    Estimates time and costs for jobs when actual data is not available
    """
    
    # Typical time estimates by task type (in hours)
    # These are conservative estimates for routine maintenance
    TYPICAL_HOURS = {
        'electrician': 1.5,      # Most electrical repairs are quick
        'plumber': 2.0,          # Plumbing often takes longer
        'hvac_technician': 2.5,  # HVAC work can be complex
        'carpenter': 3.0,        # Carpentry takes time
        'painter': 4.0,          # Painting is time-consuming
        'landscaper': 3.0,       # Outdoor work varies
        'general_handyman': 1.0, # Quick fixes
        'other': 2.0             # Unknown/equipment
    }
    
    # Typical materials cost by task type (in GBP)
    TYPICAL_MATERIALS = {
        'electrician': 45.00,
        'plumber': 75.00,
        'hvac_technician': 85.00,
        'carpenter': 60.00,
        'painter': 35.00,
        'landscaper': 40.00,
        'general_handyman': 15.00,
        'other': 50.00
    }
    
    # Contractor callout fees (additional to hourly rate)
    CALLOUT_FEES = {
        'electrician': 75.00,
        'plumber': 85.00,
        'hvac_technician': 95.00,
        'carpenter': 65.00,
        'painter': 0.00,      # Painters typically don't charge callout
        'landscaper': 50.00,
        'general_handyman': 50.00,
        'other': 75.00
    }
    
    def __init__(self, market_rates: Dict = None, inhouse_rates: Dict = None):
        """
        Initialize estimator with rate dictionaries
        
        Args:
            market_rates: Contractor hourly rates
            inhouse_rates: In-house hourly rates
        """
        self.market_rates = market_rates or DEFAULT_MARKET_RATES
        self.inhouse_rates = inhouse_rates or DEFAULT_INHOUSE_RATES
    
    def estimate_job_cost(self, task_type: str) -> Tuple[float, float, float, float]:
        """
        Estimate costs for a job
        
        Args:
            task_type: Type of tradesperson needed
            
        Returns:
            Tuple of (hours_spent, materials_cost, contractor_total, inhouse_total)
        """
        # Get estimates
        hours = self.TYPICAL_HOURS.get(task_type, 2.0)
        materials = self.TYPICAL_MATERIALS.get(task_type, 50.00)
        callout = self.CALLOUT_FEES.get(task_type, 75.00)
        
        # Get rates
        market_rate = self.market_rates.get(task_type, self.market_rates.get('other', 70.00))
        inhouse_rate = self.inhouse_rates.get(task_type, self.inhouse_rates.get('other', 38.00))
        
        # Calculate costs
        # Contractor: callout fee + (hours × rate) + materials
        contractor_total = callout + (hours * market_rate) + materials
        
        # In-house: (hours × rate) + materials (no callout fee)
        inhouse_total = (hours * inhouse_rate) + materials
        
        return hours, materials, contractor_total, inhouse_total
    
    def estimate_savings(self, task_type: str) -> float:
        """
        Calculate estimated savings for one job
        
        Args:
            task_type: Type of tradesperson needed
            
        Returns:
            Estimated savings in GBP
        """
        _, _, contractor_total, inhouse_total = self.estimate_job_cost(task_type)
        return contractor_total - inhouse_total
