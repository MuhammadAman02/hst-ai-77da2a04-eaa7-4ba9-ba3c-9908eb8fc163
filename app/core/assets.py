"""
Professional Visual Asset Management System for Seiko Watch Store
Handles luxury watch imagery with contextual categories and fallbacks
"""

import requests
from typing import Dict, List, Optional
from urllib.parse import quote
import hashlib
import os
from pathlib import Path

class SeikoAssetManager:
    """Advanced professional visual asset management for luxury watch e-commerce"""
    
    SEIKO_WATCH_CATEGORIES = {
        "hero": [
            "seiko+watch+luxury", "luxury+timepiece", "premium+watch", 
            "seiko+automatic", "watch+collection", "luxury+wristwatch"
        ],
        "products": [
            "seiko+watch+face", "watch+detail", "timepiece+close", 
            "luxury+watch+band", "seiko+movement", "watch+craftsmanship"
        ],
        "lifestyle": [
            "businessman+watch", "luxury+lifestyle", "professional+timepiece",
            "watch+wrist", "elegant+watch", "premium+accessories"
        ],
        "collections": [
            "seiko+prospex", "seiko+presage", "seiko+astron",
            "watch+collection+display", "luxury+watch+showcase", "timepiece+gallery"
        ],
        "craftsmanship": [
            "watch+mechanism", "seiko+movement", "watchmaking+craft",
            "precision+engineering", "japanese+craftsmanship", "horological+art"
        ],
        "trust": [
            "luxury+service", "watch+warranty", "premium+support",
            "professional+consultation", "authorized+dealer", "watch+expertise"
        ]
    }
    
    FALLBACK_CATEGORIES = {
        "hero": ["luxury", "premium", "elegant", "sophisticated"],
        "products": ["product", "detail", "quality", "craftsmanship"],
        "lifestyle": ["lifestyle", "professional", "business", "elegant"],
        "collections": ["collection", "gallery", "showcase", "display"],
        "craftsmanship": ["precision", "engineering", "craft", "art"],
        "trust": ["service", "quality", "professional", "trust"]
    }
    
    def __init__(self):
        self.cache_dir = Path("app/static/images/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.base_unsplash_url = "https://source.unsplash.com"
        self.base_picsum_url = "https://picsum.photos"
        
    def get_seiko_assets(self, section_count: int = 8) -> Dict[str, List[Dict]]:
        """Fetch contextually relevant professional Seiko watch images"""
        assets = {}
        
        for section, keywords in self.SEIKO_WATCH_CATEGORIES.items():
            section_images = []
            for i in range(min(section_count, len(keywords))):
                keyword = keywords[i % len(keywords)]
                fallback_keyword = self.FALLBACK_CATEGORIES[section][i % len(self.FALLBACK_CATEGORIES[section])]
                
                # Create unique seed for consistent images
                seed = int(hashlib.md5(f"seiko_{section}_{i}".encode()).hexdigest()[:8], 16) % 10000
                
                # Multiple image sources for reliability
                primary_url = f"{self.base_unsplash_url}/1200x800/?{quote(keyword)}&sig={seed}"
                secondary_url = f"{self.base_unsplash_url}/1200x800/?{quote(fallback_keyword)}&sig={seed}"
                fallback_url = f"{self.base_picsum_url}/1200/800?random={seed}"
                
                section_images.append({
                    "primary": primary_url,
                    "secondary": secondary_url,
                    "fallback": fallback_url,
                    "alt": f"Professional Seiko {keyword.replace('+', ' ')} imagery",
                    "title": f"Seiko {section.title()} - {keyword.replace('+', ' ').title()}"
                })
            
            assets[section] = section_images
        
        return assets
    
    def get_product_image(self, product_name: str, image_type: str = "main") -> Dict[str, str]:
        """Get specific product image with multiple fallbacks"""
        # Clean product name for search
        clean_name = product_name.lower().replace(" ", "+")
        
        # Create seed based on product name for consistency
        seed = int(hashlib.md5(f"{clean_name}_{image_type}".encode()).hexdigest()[:8], 16) % 10000
        
        if image_type == "main":
            search_terms = [f"seiko+{clean_name}", f"{clean_name}+watch", "luxury+watch"]
        elif image_type == "detail":
            search_terms = [f"{clean_name}+detail", "watch+mechanism", "watch+face"]
        elif image_type == "lifestyle":
            search_terms = [f"{clean_name}+lifestyle", "watch+wrist", "luxury+lifestyle"]
        else:
            search_terms = ["seiko+watch", "luxury+timepiece"]
        
        return {
            "primary": f"{self.base_unsplash_url}/800x800/?{quote(search_terms[0])}&sig={seed}",
            "secondary": f"{self.base_unsplash_url}/800x800/?{quote(search_terms[1])}&sig={seed}",
            "fallback": f"{self.base_picsum_url}/800/800?random={seed}",
            "alt": f"{product_name} - Professional watch photography",
            "title": product_name
        }
    
    def get_hero_banner(self, collection: str = "luxury") -> Dict[str, str]:
        """Get hero banner image for specific Seiko collection"""
        seed = int(hashlib.md5(f"hero_{collection}".encode()).hexdigest()[:8], 16) % 10000
        
        search_terms = {
            "luxury": "seiko+luxury+watch+collection",
            "sport": "seiko+prospex+sport+watch",
            "dress": "seiko+presage+dress+watch",
            "solar": "seiko+astron+solar+watch"
        }
        
        search_term = search_terms.get(collection, "seiko+watch+luxury")
        
        return {
            "primary": f"{self.base_unsplash_url}/1920x600/?{quote(search_term)}&sig={seed}",
            "secondary": f"{self.base_unsplash_url}/1920x600/?luxury+timepiece&sig={seed}",
            "fallback": f"{self.base_picsum_url}/1920/600?random={seed}",
            "alt": f"Seiko {collection.title()} Collection - Premium timepieces",
            "title": f"Seiko {collection.title()} Collection"
        }
    
    def generate_image_css(self) -> str:
        """Generate CSS for professional Seiko watch store image handling"""
        return """
        /* Seiko Watch Store Professional Image System */
        :root {
            --seiko-gold: #D4AF37;
            --seiko-dark: #1a1a1a;
            --seiko-silver: #C0C0C0;
            --shadow-luxury: 0 8px 32px rgba(0,0,0,0.3);
            --shadow-product: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .hero-banner {
            width: 100%;
            height: 500px;
            object-fit: cover;
            border-radius: 12px;
            box-shadow: var(--shadow-luxury);
            position: relative;
        }
        
        .hero-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(0,0,0,0.4) 0%, rgba(212,175,55,0.2) 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
        }
        
        .product-image {
            width: 100%;
            height: 300px;
            object-fit: cover;
            border-radius: 8px;
            transition: all 0.4s ease;
            box-shadow: var(--shadow-product);
        }
        
        .product-image:hover {
            transform: scale(1.05);
            box-shadow: var(--shadow-luxury);
        }
        
        .product-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
            margin: 32px 0;
        }
        
        .product-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: var(--shadow-product);
            transition: all 0.3s ease;
            border: 1px solid #f0f0f0;
        }
        
        .product-card:hover {
            transform: translateY(-8px);
            box-shadow: var(--shadow-luxury);
            border-color: var(--seiko-gold);
        }
        
        .product-detail-image {
            width: 100%;
            height: 400px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 16px;
        }
        
        .image-zoom {
            cursor: zoom-in;
            transition: transform 0.3s ease;
        }
        
        .image-zoom:hover {
            transform: scale(1.02);
        }
        
        .lifestyle-gallery {
            display: flex;
            gap: 16px;
            overflow-x: auto;
            padding: 16px 0;
            scroll-behavior: smooth;
        }
        
        .lifestyle-image {
            min-width: 200px;
            height: 150px;
            object-fit: cover;
            border-radius: 8px;
            box-shadow: var(--shadow-product);
        }
        
        .collection-showcase {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 24px 0;
        }
        
        .collection-card {
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: var(--shadow-product);
            transition: transform 0.3s ease;
        }
        
        .collection-card:hover {
            transform: scale(1.03);
        }
        
        .collection-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        
        .collection-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0,0,0,0.8));
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .trust-badge {
            display: inline-block;
            padding: 8px 16px;
            background: linear-gradient(135deg, var(--seiko-gold), #B8860B);
            color: white;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin: 4px;
            box-shadow: var(--shadow-product);
        }
        
        .loading-placeholder {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        @media (max-width: 768px) {
            .hero-banner {
                height: 300px;
            }
            
            .product-gallery {
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 16px;
            }
            
            .product-image {
                height: 250px;
            }
            
            .collection-showcase {
                grid-template-columns: 1fr;
            }
        }
        
        /* Image error handling */
        .image-error {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #6c757d;
            font-size: 14px;
            text-align: center;
        }
        
        .image-error::before {
            content: "🕰️";
            font-size: 24px;
            margin-bottom: 8px;
            display: block;
        }
        """
    
    def validate_image_url(self, url: str) -> bool:
        """Validate if image URL is accessible"""
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except:
            return False