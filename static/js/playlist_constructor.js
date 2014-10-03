// JavaScript code to construct a playlist and put it in a YouTube embedded player iframe

function addTitle() {
    $( "h1" ).text( "Videos from Citizen Reporters" );
}

function getPlaylistVideos(callback) {
    playlist_data = do_api_call('get_playlists', {'foo': 2}, function(playlist_data) {
        if (callback) {
            callback(playlist_data['all_playlists']);
        }
    }, function(error_string) {
        console.log(error_string);
    });
}
