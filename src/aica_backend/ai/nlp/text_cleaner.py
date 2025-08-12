import re
import html
from typing import List
import logging
import unicodedata

logger = logging.getLogger(__name__)

class TextCleaner:
    
    def __init__(self):
        # Common patterns for cleaning
        self.html_pattern = re.compile(r'<[^>]+>')
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b')
        self.excessive_whitespace = re.compile(r'\s+')
        self.bullet_points = re.compile(r'^[\s]*[•\-\*\+]\s*', re.MULTILINE)
        self.numbers_only = re.compile(r'^\d+$')
    
    def clean_job_posting_text(self, text: str) -> str:
        if not text:
            return ""
        
        try:
            # Start with basic cleaning
            cleaned = self.basic_clean(text)
            
            # Remove common job posting artifacts
            cleaned = self._remove_job_posting_artifacts(cleaned)
            
            # Normalize whitespace
            cleaned = self.normalize_whitespace(cleaned)
            
            return cleaned.strip()
            
        except Exception as e:
            logger.error(f"Error cleaning job posting text: {str(e)}")
            return text
    
    def clean_profile_text(self, text: str) -> str:
        if not text:
            return ""
        
        try:
            # Start with basic cleaning
            cleaned = self.basic_clean(text)
            
            # Remove personal information patterns
            cleaned = self._remove_personal_info(cleaned)
            
            # Normalize whitespace
            cleaned = self.normalize_whitespace(cleaned)
            
            return cleaned.strip()
            
        except Exception as e:
            logger.error(f"Error cleaning profile text: {str(e)}")
            return text
    
    def basic_clean(self, text: str) -> str:
        if not text:
            return ""
        
        # Decode HTML entities
        cleaned = html.unescape(text)
        
        # Remove HTML tags
        cleaned = self.html_pattern.sub(' ', cleaned)
        
        # Normalize unicode characters
        cleaned = unicodedata.normalize('NFKD', cleaned)
        
        # Remove control characters
        cleaned = ''.join(char for char in cleaned if unicodedata.category(char)[0] != 'C')
        
        return cleaned
    
    def remove_urls_and_emails(self, text: str) -> str:
        if not text:
            return ""
        
        # Remove URLs
        text = self.url_pattern.sub('[URL]', text)
        
        # Remove emails
        text = self.email_pattern.sub('[EMAIL]', text)
        
        return text
    
    def normalize_whitespace(self, text: str) -> str:
        if not text:
            return ""
        
        # Replace multiple whitespace characters with single space
        text = self.excessive_whitespace.sub(' ', text)
        
        # Remove bullet points but keep the content
        text = self.bullet_points.sub('', text)
        
        return text.strip()
    
    def extract_sentences(self, text: str) -> List[str]:
        if not text:
            return []
        
        # Simple sentence splitting (can be enhanced with proper tokenizer)
        sentences = re.split(r'[.!?]+', text)
        
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Filter out very short sentences
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        if not text:
            return []
        
        # Convert to lowercase and split into words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Filter words
        keywords = []
        stop_words = self._get_stop_words()
        
        for word in words:
            if (len(word) >= min_length and 
                word not in stop_words and 
                not self.numbers_only.match(word)):
                keywords.append(word)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for keyword in keywords:
            if keyword not in seen:
                seen.add(keyword)
                unique_keywords.append(keyword)
        
        return unique_keywords
    
    def _remove_job_posting_artifacts(self, text: str) -> str:
        # Common phrases to remove or normalize
        artifacts = [
            r'\b(?:apply now|click here|visit our website)\b',
            r'\b(?:equal opportunity employer|eoe)\b',
            r'\b(?:drug free workplace|background check required)\b',
            r'\b(?:salary|compensation):\s*\$?[\d,\-\s]+(?:per|\/)?(?:year|month|hour)?\b',
            r'\b(?:job id|reference|req):\s*\w+\b',
            r'\b(?:posted|date posted):\s*[\d\/\-]+\b'
        ]
        
        for pattern in artifacts:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text
    
    def _remove_personal_info(self, text: str) -> str:
        # Remove phone numbers
        text = self.phone_pattern.sub('[PHONE]', text)
        
        # Remove email addresses
        text = self.email_pattern.sub('[EMAIL]', text)
        
        # Remove addresses (basic pattern)
        address_pattern = re.compile(r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)\b', re.IGNORECASE)
        text = address_pattern.sub('[ADDRESS]', text)
        
        return text
    
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
    
    def preprocess_for_embedding(self, text: str) -> str:
        if not text:
            return ""
        
        # Clean text
        cleaned = self.basic_clean(text)
        
        # Keep URLs and emails as placeholders rather than removing
        cleaned = self.url_pattern.sub('[URL]', cleaned)
        cleaned = self.email_pattern.sub('[EMAIL]', cleaned)
        
        # Normalize whitespace
        cleaned = self.normalize_whitespace(cleaned)
        
        # Limit length for embedding models
        if len(cleaned) > 5000:
            cleaned = cleaned[:5000] + "..."
        
        return cleaned.strip()
    
    def extract_technical_terms(self, text: str) -> List[str]:
        if not text:
            return []
        
        # Patterns for technical terms
        patterns = [
            r'\b[A-Z]{2,}\b',  # Acronyms (e.g., API, SQL, AWS)
            r'\b[A-Za-z]+\.[A-Za-z]+\b',  # Dotted names (e.g., React.js, Node.js)
            r'\b[A-Za-z]+-[A-Za-z]+\b',  # Hyphenated terms (e.g., test-driven)
            r'\b[A-Za-z]+\+\+?\b',  # Plus terms (e.g., C++, C+)
            r'\b[A-Za-z]*[0-9]+[A-Za-z]*\b'  # Terms with numbers (e.g., Python3, HTML5)
        ]
        
        technical_terms = set()
        for pattern in patterns:
            matches = re.findall(pattern, text)
            technical_terms.update(matches)
        
        return list(technical_terms)

_text_cleaner = None

def get_text_cleaner() -> TextCleaner:
    global _text_cleaner
    if _text_cleaner is None:
        _text_cleaner = TextCleaner()
    return _text_cleaner
