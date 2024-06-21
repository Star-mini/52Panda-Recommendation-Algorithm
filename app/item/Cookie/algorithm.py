def process_cookie(cookie_id):
    # 쿠키 알고리즘 로직 구현
    return {'id': cookie_id, 'result': 'cookie processed'}


'''
# cookie_algorithm.py

import numpy as np
from scipy.spatial import distance
import logging
import json
from app.common.models import Item

def point_to_plane_distance(point, plane_point, plane_normal):
    return np.abs(np.dot(plane_normal, point - plane_point)) / np.linalg.norm(plane_normal)

def is_point_in_triangle(pt, v1, v2, v3):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0
    
    return ((b1 == b2) and (b2 == b3))

def get_embeddings_by_category(category_id):
    try:
        items = Item.query.filter_by(category_id=category_id).all()
        embeddings = []
        for item in items:
            for recommend in item.recommendations:
                if recommend.represent_embedding:
                    represent_embedding = recommend.represent_embedding
                    if isinstance(represent_embedding, str):
                        represent_embedding = json.loads(represent_embedding)
                    embeddings.append({
                        'id': item.item_id,
                        'embedding': represent_embedding
                    })
        return embeddings
    except Exception as e:
        logging.error(f"Error in get_embeddings_by_category: {e}")
        return []

def process_cookie(item_id):
    try:
        item = Item.query.filter_by(item_id=item_id).first()
        if item is None:
            raise ValueError(f"Item with ID {item_id} not found")

        recommendations = item.recommendations
        if not recommendations:
            raise ValueError(f"No recommendations found for item ID {item_id}")

        represent_embeddings = []
        for recommend in recommendations:
            if recommend.represent_embedding:
                represent_embedding = recommend.represent_embedding
                if isinstance(represent_embedding, str):
                    represent_embedding = json.loads(represent_embedding)
                represent_embeddings.append(represent_embedding)

        if len(represent_embeddings) < 4:
            raise ValueError("Not enough represent embeddings (need at least 4)")
        represent_embeddings = represent_embeddings[:4]

        embeddings = get_embeddings_by_category(item.category_id)

        distances = []
        for embedding in embeddings:
            other_item_id = embedding['id']
            other_embedding = embedding['embedding']

            min_distance = float('inf')
            for i in range(4):
                for j in range(i+1, 4):
                    for k in range(j+1, 4):
                        v1, v2, v3 = represent_embeddings[i], represent_embeddings[j], represent_embeddings[k]
                        plane_normal = np.cross(v2 - v1, v3 - v1)
                        
                        if is_point_in_triangle(other_embedding, v1, v2, v3):
                            distance_to_plane = point_to_plane_distance(other_embedding, v1, plane_normal)
                        else:
                            distance_to_plane = min(
                                np.linalg.norm(other_embedding - v1),
                                np.linalg.norm(other_embedding - v2),
                                np.linalg.norm(other_embedding - v3)
                            )
                        min_distance = min(min_distance, distance_to_plane)

            distances.append({'item_id': other_item_id, 'distance': min_distance, 'algorithm': 'cookie'})

        distances.sort(key=lambda x: x['distance'])
        top_recommendations = distances[:12]

        recommended_item_ids = [rec['item_id'] for rec in top_recommendations]
        logging.info(f"Top 12 cookie recommendations for item {item_id}: {recommended_item_ids}")

        return top_recommendations

    except Exception as e:
        logging.error(f"Error in process_cookie: {e}")
        return {'status': 'fail', 'message': str(e)}
'''