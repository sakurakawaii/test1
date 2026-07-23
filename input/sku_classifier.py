"""
sku_classifier.py

Determines the downstream handling route for an inventory record
based on its category. Perishable and hazardous categories are routed
to expedited/special handling; anything unrecognized falls through to
the default 'unknown' route, which skips expedited handling entirely.
"""

CATEGORY_ROUTES = {
    'PERISHABLE': 'expedited',
    'HAZARDOUS': 'special_handling',
    'ELECTRONICS': 'standard',
    'APPAREL': 'standard',
    'GENERAL': 'standard',
}


def get_route(record):
    """
    Looks up the handling route for record['category'] in
    CATEGORY_ROUTES. Falls through to 'unknown' for anything not in
    the map.
    """
    category = record.get('category')
    return CATEGORY_ROUTES.get(category, 'unknown')
