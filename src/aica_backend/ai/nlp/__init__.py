"""
NLP Module

This module provides natural language processing capabilities for the AICA backend.
"""

from .skill_extractor import SkillExtractor, get_skill_extractor
from .text_cleaner import TextCleaner, get_text_cleaner
from .similarity import SimilarityCalculator, get_similarity_calculator

__all__ = [
    'SkillExtractor',
    'get_skill_extractor',
    'TextCleaner',
    'get_text_cleaner',
    'SimilarityCalculator',
    'get_similarity_calculator'
]
