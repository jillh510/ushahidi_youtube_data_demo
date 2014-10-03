video_story_arcs
================

Construct video playlists from general story arc descriptions. Like Mad Libs for playlists.

Usage:
Start by creating categories in the db, like "meals" or "party ideas". Categories have arc positions, which specify
the order in which videos should be selected, with keywords to select those videos. For instance, the arc position
keywords for the "meal" category might be "main dish", "side dish", etc. Finally, specify topics within the
categories, for instance "Italian". Hitting /api/1.0/create_playlists on the server will call the YouTube search
API with the cross-product of the arc-position and topic keywords, creating a playlist.

Notes:
- It's best to specify multiple keywords for each arc position and topic ("main dish", "entree", etc.). The
create_playlists function does simple scoring to choose the video that's found in the most searches.
- There's a tool at /tools to display some of the contents in the DB.

Future improvements:
- Using YouTube Freebase topics might improve the search results.
- Using a completely different data corpus would involve changing the functions in playlist.py to call the
different corpus rather than YouTube.
