from app import (
    harvest,
    shift_finder,
    headerflow,
    # docforge,
    # vector_engine, 
    # Retrive,
    # forge
)



Topics = {
    'Space & Astronomy' : [
        'Solar System',
        'Sun',
        'Moon',
        'Mars',
        'Black Hole',
        'Galaxy',
        'Space Exploration'
        ],

    'Science': [
        'Physics',
        'Chemistry',
        'Biology',
        'Genetics',
        'Quantum Mechanics',
        'Evolution',
        'Neuroscience'
    ],

    'Geography':[
        'India',
        'United States',
        'Japan',
        'Himalayas',
        'Amazon Rainforest',
        'Pacific Ocean',
        'Sahara',
    ],

    'Computer Science':[
        'Python',
        'Java',
        'Database',
        'Operating System',
        'Computer Network',
        'Internet',
        'Cybersecurity'
    ]


}


if __name__ == '__main__':

    # Passing one by one topic to extract articles related to topic
    for main_head in Topics:
        for chapters in Topics[main_head]:
            store_text = harvest.extract_text(chapters, main_head)

    # Applying a technique for retrived chunks (semantic)
    semantic_chunking = shift_finder.call_slicer()

    # Adding Headers for each chunks and storing in cache files 
    headers = headerflow.call_shifter()


    

    

    


