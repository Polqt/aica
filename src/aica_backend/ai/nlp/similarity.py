import numpy as np
from typing import List, Dict
import re
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class SimilarityCalculator:

    def __init__(self):
        self.stop_words = self._get_stop_words()
    
    def cosine_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        try:
            # Normalize vectors
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0

            similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Failed to calculate cosine similarity: {str(e)}")
            return 0.0
    
    def jaccard_similarity(self, text1: str, text2: str) -> float:

        try:
            # Tokenize and clean
            tokens1 = set(self._tokenize(text1.lower()))
            tokens2 = set(self._tokenize(text2.lower()))
            
            # Remove stop words
            tokens1 = tokens1 - self.stop_words
            tokens2 = tokens2 - self.stop_words
            
            if not tokens1 and not tokens2:
                return 1.0
            
            if not tokens1 or not tokens2:
                return 0.0
            
            # Calculate Jaccard similarity
            intersection = len(tokens1.intersection(tokens2))
            union = len(tokens1.union(tokens2))
            
            return intersection / union
            
        except Exception as e:
            logger.error(f"Failed to calculate Jaccard similarity: {str(e)}")
            return 0.0
    
    def skill_overlap_similarity(self, skills1: List[str], skills2: List[str]) -> float:
        """
        Calculate similarity based on skill overlap
        
        Args:
            skills1: First skill list
            skills2: Second skill list
            
        Returns:
            Skill overlap similarity score between 0 and 1
        """
        try:
            if not skills1 or not skills2:
                return 0.0
            
            # Normalize skill names
            skills1_norm = {skill.lower().strip() for skill in skills1}
            skills2_norm = {skill.lower().strip() for skill in skills2}
            
            # Calculate overlap
            intersection = len(skills1_norm.intersection(skills2_norm))
            union = len(skills1_norm.union(skills2_norm))
            
            if union == 0:
                return 0.0
            
            return intersection / union
            
        except Exception as e:
            logger.error(f"Failed to calculate skill overlap: {str(e)}")
            return 0.0
    
    def weighted_skill_similarity(self, skills1: List[str], skills2: List[str], 
                                skill_weights: Dict[str, float] = None) -> float:
        """
        Calculate weighted skill similarity
        
        Args:
            skills1: First skill list
            skills2: Second skill list
            skill_weights: Dictionary of skill weights
            
        Returns:
            Weighted skill similarity score
        """
        try:
            if not skills1 or not skills2:
                return 0.0
            
            # Normalize skills
            skills1_norm = {skill.lower().strip() for skill in skills1}
            skills2_norm = {skill.lower().strip() for skill in skills2}
            
            # Get common skills
            common_skills = skills1_norm.intersection(skills2_norm)
            
            if not common_skills:
                return 0.0
            
            # Calculate weighted score
            if skill_weights:
                total_weight = 0.0
                matched_weight = 0.0
                
                all_skills = skills1_norm.union(skills2_norm)
                for skill in all_skills:
                    weight = skill_weights.get(skill, 1.0)
                    total_weight += weight
                    if skill in common_skills:
                        matched_weight += weight
                
                return matched_weight / total_weight if total_weight > 0 else 0.0
            else:
                # Equal weights
                return len(common_skills) / len(skills1_norm.union(skills2_norm))
            
        except Exception as e:
            logger.error(f"Failed to calculate weighted skill similarity: {str(e)}")
            return 0.0
    
    def fuzzy_string_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate fuzzy string similarity using edit distance
        
        Args:
            str1: First string
            str2: Second string
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            if not str1 or not str2:
                return 0.0
            
            # Normalize strings
            str1 = str1.lower().strip()
            str2 = str2.lower().strip()
            
            if str1 == str2:
                return 1.0
            
            # Calculate Levenshtein distance
            distance = self._levenshtein_distance(str1, str2)
            max_len = max(len(str1), len(str2))
            
            if max_len == 0:
                return 1.0
            
            # Convert to similarity score
            similarity = 1.0 - (distance / max_len)
            return max(0.0, similarity)
            
        except Exception as e:
            logger.error(f"Failed to calculate fuzzy similarity: {str(e)}")
            return 0.0
    
    def semantic_text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic text similarity using TF-IDF
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Semantic similarity score between 0 and 1
        """
        try:
            # Tokenize texts
            tokens1 = self._tokenize(text1.lower())
            tokens2 = self._tokenize(text2.lower())
            
            # Remove stop words
            tokens1 = [t for t in tokens1 if t not in self.stop_words]
            tokens2 = [t for t in tokens2 if t not in self.stop_words]
            
            if not tokens1 or not tokens2:
                return 0.0
            
            # Create vocabulary
            vocab = set(tokens1 + tokens2)
            
            # Calculate TF-IDF vectors
            tfidf1 = self._calculate_tfidf(tokens1, vocab)
            tfidf2 = self._calculate_tfidf(tokens2, vocab)
            
            # Calculate cosine similarity
            return self.cosine_similarity(tfidf1, tfidf2)
            
        except Exception as e:
            logger.error(f"Failed to calculate semantic similarity: {str(e)}")
            return 0.0
    
    def calculate_composite_similarity(self, 
                                     text1: str, text2: str,
                                     skills1: List[str] = None,
                                     skills2: List[str] = None,
                                     embeddings1: np.ndarray = None,
                                     embeddings2: np.ndarray = None,
                                     weights: Dict[str, float] = None) -> Dict[str, float]:
        """
        Calculate composite similarity using multiple methods
        
        Args:
            text1: First text
            text2: Second text
            skills1: First skill list
            skills2: Second skill list
            embeddings1: First embedding vector
            embeddings2: Second embedding vector
            weights: Weights for different similarity methods
            
        Returns:
            Dictionary with individual and composite scores
        """
        results = {}
        
        # Default weights
        if weights is None:
            weights = {
                'text_similarity': 0.3,
                'skill_similarity': 0.4,
                'embedding_similarity': 0.3
            }
        

        if text1 and text2:
            results['jaccard_similarity'] = self.jaccard_similarity(text1, text2)
            results['semantic_similarity'] = self.semantic_text_similarity(text1, text2)
            results['text_similarity'] = (results['jaccard_similarity'] + results['semantic_similarity']) / 2
        else:
            results['text_similarity'] = 0.0
        
        # Skill similarity
        if skills1 and skills2:
            results['skill_similarity'] = self.skill_overlap_similarity(skills1, skills2)
        else:
            results['skill_similarity'] = 0.0
        
        # Embedding similarity
        if embeddings1 is not None and embeddings2 is not None:
            results['embedding_similarity'] = self.cosine_similarity(embeddings1, embeddings2)
        else:
            results['embedding_similarity'] = 0.0
        
        # Composite score
        composite_score = (
            results['text_similarity'] * weights.get('text_similarity', 0.3) +
            results['skill_similarity'] * weights.get('skill_similarity', 0.4) +
            results['embedding_similarity'] * weights.get('embedding_similarity', 0.3)
        )
        
        results['composite_score'] = composite_score
        
        return results
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Simple word tokenization
        tokens = re.findall(r'\b\w+\b', text)
        return [token for token in tokens if len(token) > 1]
    
    def _calculate_tfidf(self, tokens: List[str], vocab: set) -> np.ndarray:
        """Calculate TF-IDF vector for tokens"""
        # Term frequency
        tf_counter = Counter(tokens)
        tf_vector = np.array([tf_counter.get(term, 0) for term in vocab], dtype=float)
        
        # Normalize by document length
        if len(tokens) > 0:
            tf_vector = tf_vector / len(tokens)
        
        # Simple IDF (inverse document frequency)
        # In a real implementation, this would be calculated from a corpus
        idf_vector = np.ones(len(vocab))
        
        # TF-IDF
        tfidf_vector = tf_vector * idf_vector
        
        return tfidf_vector
    
    def _levenshtein_distance(self, str1: str, str2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(str1) < len(str2):
            return self._levenshtein_distance(str2, str1)
        
        if len(str2) == 0:
            return len(str1)
        
        previous_row = list(range(len(str2) + 1))
        for i, c1 in enumerate(str1):
            current_row = [i + 1]
            for j, c2 in enumerate(str2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _get_stop_words(self) -> set:
        """Get common English stop words"""
        return {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'would', 'you', 'your', 'have', 'had',
            'has', 'having', 'do', 'does', 'did', 'doing', 'should', 'could',
            'would', 'this', 'that', 'these', 'those', 'i', 'me', 'my', 'myself',
            'we', 'our', 'ours', 'ourselves', 'they', 'them', 'their', 'theirs',
            'themselves', 'what', 'which', 'who', 'whom', 'whose', 'why', 'how',
            'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
            'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'can', 'just', 'now', 'also'
        }


# Global similarity calculator instance
_similarity_calculator = None

def get_similarity_calculator() -> SimilarityCalculator:
    """Get global similarity calculator instance"""
    global _similarity_calculator
    if _similarity_calculator is None:
        _similarity_calculator = SimilarityCalculator()
    return _similarity_calculator
