import os
import json
import logging
from openai import OpenAI

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
try:
    openai = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {e}")
    openai = None

# Category definitions
CATEGORIES = {
    'all': 'All categories',
    'humor': 'Humorous and entertaining content',
    'tech': 'Technology-related content',
    'finance': 'Financial advice and education',
    'fitness': 'Health and fitness content',
    'education': 'Educational and informative content',
    'lifestyle': 'Lifestyle and daily vlog content'
}

def generate_content_ideas(topic, category='all'):
    """Generate content ideas for a given topic and category using OpenAI"""
    try:
        if not OPENAI_API_KEY or openai is None:
            logger.warning("Using mock data as OpenAI is not configured")
            return generate_mock_content_ideas(topic, category)
        
        # Prepare the prompt based on category
        if category != 'all':
            category_desc = CATEGORIES.get(category, 'various topics')
            prompt = f"""Generate 5 creative social media content ideas for "{topic}" specifically for {category_desc}.
            For each idea, include:
            1. A catchy title (max 60 chars)
            2. Brief description (1-2 sentences)
            3. Content type (e.g., video, reel, story, post)
            4. Estimated virality potential (low, medium, high)
            5. Target audience
            
            Return as a JSON array with fields: title, description, content_type, virality, target_audience, category.
            Set category to: {category}"""
        else:
            prompt = f"""Generate 5 creative social media content ideas across different categories for "{topic}".
            Include a mix of humor, tech, finance, fitness, and lifestyle ideas.
            For each idea, include:
            1. A catchy title (max 60 chars)
            2. Brief description (1-2 sentences)
            3. Content type (e.g., video, reel, story, post)
            4. Estimated virality potential (low, medium, high)
            5. Target audience
            6. Category (one of: humor, tech, finance, fitness, education, lifestyle)
            
            Return as a JSON array with fields: title, description, content_type, virality, target_audience, category."""

        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a social media trend expert and content strategist."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=1000
        )
        
        # Parse the response
        content = response.choices[0].message.content
        ideas = json.loads(content)
        
        # Handle different response formats
        if isinstance(ideas, dict) and 'ideas' in ideas:
            return ideas['ideas']
        elif isinstance(ideas, list):
            return ideas
        else:
            logger.error(f"Unexpected response format: {content}")
            return generate_mock_content_ideas(topic, category)
            
    except Exception as e:
        logger.error(f"Error generating content ideas: {e}")
        return generate_mock_content_ideas(topic, category)

def generate_mock_content_ideas(topic, category='all'):
    """Generate mock content ideas when API fails"""
    logger.info(f"Generating mock content ideas for {topic} in category {category}")
    
    # Base templates for different categories
    templates = {
        'humor': [
            {"title": f"When {topic} Goes Hilariously Wrong", 
             "description": f"A compilation of funny {topic} fails that everyone can relate to.", 
             "content_type": "video", "virality": "high", 
             "target_audience": "General audience with interest in comedy", 
             "category": "humor"},
            {"title": f"{topic} Expectations vs. Reality", 
             "description": f"Contrasting what people expect from {topic} with the often-amusing reality.", 
             "content_type": "reel", "virality": "high", 
             "target_audience": "Young adults and teens", 
             "category": "humor"}
        ],
        'tech': [
            {"title": f"5 {topic} Hacks You Never Knew Existed", 
             "description": f"Quick technical tips to master {topic} that most people don't know about.", 
             "content_type": "tutorial", "virality": "medium", 
             "target_audience": "Tech enthusiasts and early adopters", 
             "category": "tech"},
            {"title": f"The Future of {topic}: 2025 Predictions", 
             "description": f"Analysis of upcoming trends and technologies related to {topic}.", 
             "content_type": "post", "virality": "medium", 
             "target_audience": "Industry professionals and tech followers", 
             "category": "tech"}
        ],
        'finance': [
            {"title": f"How {topic} Can Save You $1000 This Month", 
             "description": f"Practical financial strategies using {topic} for immediate savings.", 
             "content_type": "video", "virality": "medium", 
             "target_audience": "Budget-conscious adults", 
             "category": "finance"},
            {"title": f"Investing in {topic}: Beginner's Guide", 
             "description": f"Step-by-step approach to understanding investment opportunities in {topic}.", 
             "content_type": "series", "virality": "low", 
             "target_audience": "New investors", 
             "category": "finance"}
        ],
        'fitness': [
            {"title": f"10-Minute {topic} Workout for Busy People", 
             "description": f"Quick and effective workout routine incorporating {topic} principles.", 
             "content_type": "reel", "virality": "high", 
             "target_audience": "Busy professionals interested in fitness", 
             "category": "fitness"},
            {"title": f"{topic} Transformation Challenge", 
             "description": f"30-day fitness journey using {topic} methods with visible results.", 
             "content_type": "series", "virality": "medium", 
             "target_audience": "Fitness enthusiasts looking for challenges", 
             "category": "fitness"}
        ],
        'education': [
            {"title": f"{topic} Explained in 60 Seconds", 
             "description": f"Quick, easy-to-understand explanation of {topic} for beginners.", 
             "content_type": "reel", "virality": "medium", 
             "target_audience": "Students and lifelong learners", 
             "category": "education"},
            {"title": f"What Schools Don't Teach About {topic}", 
             "description": f"Lesser-known but important facts about {topic} that aren't in textbooks.", 
             "content_type": "video", "virality": "medium", 
             "target_audience": "Curious minds and alternative education followers", 
             "category": "education"}
        ],
        'lifestyle': [
            {"title": f"Day in the Life: {topic} Edition", 
             "description": f"Follow-along vlog showing how {topic} integrates into daily routines.", 
             "content_type": "vlog", "virality": "medium", 
             "target_audience": "Lifestyle content followers", 
             "category": "lifestyle"},
            {"title": f"{topic} Room Makeover", 
             "description": f"Transforming a space with {topic}-inspired aesthetics and functionality.", 
             "content_type": "video", "virality": "medium", 
             "target_audience": "Home decor and design enthusiasts", 
             "category": "lifestyle"}
        ]
    }
    
    if category != 'all':
        # Return ideas from the specified category
        return templates.get(category, templates['humor'])
    else:
        # Return mix of ideas from all categories
        mixed_ideas = []
        for cat in templates:
            mixed_ideas.append(templates[cat][0])
            if len(mixed_ideas) >= 5:
                break
        return mixed_ideas
