# Convert processing code to a function
def process_results(video_data):
    nested_values = ['channelThumbnail', 'thumbnail', 'richThumbnail']
    skip_values = ['description', 'richThumbnail', 'type']
    
    # Initialize a dictionary to store flattened data
    flattened_data = {}
    
    # Loop through each video
    for idx, value in enumerate(video_data):
        flattened_data[idx] = {}
        # Loop through each property in each video
        for prop_idx, prop_value in value.items():
            # Check if it's a list (nested value)
            if isinstance(prop_value, list):
                # Loop through each nested property
                for nested_idx, nested_value in prop_value[0].items():
                    if prop_idx not in skip_values:
                        flattened_data[idx][prop_idx + '_' + nested_idx] = nested_value
            # If it's not a list and not in the skip list, add it directly
            elif prop_idx not in skip_values:
                flattened_data[idx][prop_idx] = prop_value
        
    return flattened_data


    