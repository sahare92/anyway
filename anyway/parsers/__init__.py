short_distance_resolutions = ["צומת עירוני", "צומת בינעירוני", "רחוב"]
long_distance_resolutions = ["עיר", "נפה", "מחוז", "כביש בינעירוני"]
resolution_dict = {
    "מחוז": ["region_hebrew"],
    "נפה": ["district_hebrew"],
    "עיר": ["yishuv_name"],
    "רחוב": ["yishuv_name", "street1_hebrew"],
    "צומת עירוני": ["yishuv_name", "street1_hebrew", "street2_hebrew"],
    "כביש בינעירוני": ["road1", "road_segment_name"],
    "צומת בינעירוני": ["road1", "road_segment_name", "road2", "non_urban_intersection_hebrew"],
    "אחר": [
        "region_hebrew",
        "district_hebrew",
        "yishuv_name",
        "street1_hebrew",
        "street2_hebrew",
        "non_urban_intersection_hebrew",
        "road1",
        "road2",
        "road_segment_name",
    ],
}
