def run_etl():
    from extract import get_token, get_auth_header, search_artist_id, get_artist_details
    from extract import get_album_details, get_album_tracks, get_artist_top_tracks

    import pandas as pd
    import psycopg2
    from dotenv import load_dotenv
    load_dotenv() 
    import os
    import datetime
    from datetime import datetime

    host = os.getenv("db_host")
    user = os.getenv("db_user")
    password = os.getenv("db_password")
    database = os.getenv("db_name")
    port = os.getenv("db_port")

    #connect to database
    def connect_to_database(): 
        cnx = psycopg2.connect(
        dbname = database,
        user = user,
        password = password,
        host = host,
        port = port)
        cursor = cnx.cursor()
        return cnx, cursor
    cnx, cursor = connect_to_database()

    if cnx is None or cursor is None:
        print("Failed to connect to the database.")
    else:
        print("Connection successful!")

    #call spotify funtions defined in extract_spotify
    artist_name = "Tems"                           #artist name
    token = get_token()                            #get token
    headers = get_auth_header(token)               #get header
    artist_id = search_artist_id(artist_name)      #get artist id
    artist_details = get_artist_details(artist_id)
    album_details = get_album_details(artist_id)   #get albums
    track_details = [] #create a list to combine all track details
    for album in album_details:
        album_id = album['id']
        tracks = get_album_tracks(album_id)['items']
        for track in tracks:
            track['album_id'] = album_id
            track_details.append(track)
    top_tracks = get_artist_top_tracks(artist_id)  #get top tracks 

    #transform and load data into database
    #albums
    insert_into_album = """insert into albums(id, album_name, album_type, 
                             available_markets, release_date, total_tracks)
                             values(%s, %s, %s, %s, %s, %s) 
                             on conflict (id) do nothing"""
    for album in album_details:
        cursor.execute(insert_into_album,
                   (album['id'],
                    album['name'],
                    album['album_type'],
                    int(len(album['available_markets'])),
                    datetime.strptime(album['release_date'], "%Y-%m-%d"),
                    album['total_tracks']))

    cnx.commit()

    #artist
    insert_into_artist = """insert into artist(id, name, followers, popularity, genre)
                        values(%s, %s, %s, %s, %s)
                        on conflict (id) do nothing"""
    cursor.execute(insert_into_artist, 
               (artist_details['id'],
                artist_details['name'],
                artist_details['followers']['total'],
                artist_details['popularity'],
                artist_details['genres']))
    cnx.commit()

    #tracks
    insert_into_tracks = """insert into tracks(id, track_name, track_number, duration, explicit, album_id)
                        values(%s, %s, %s, %s, %s, %s)
                        on conflict (id) do nothing"""
    for track in track_details:
        cursor.execute(insert_into_tracks,
                   (track['id'],
                    track['name'],
                    track['track_number'],
                    round(track['duration_ms']/60000,2),
                    track['explicit'],
                    track['album_id']))
    cnx.commit()

    #top_tracks
    insert_into_top_tracks = """insert into top_tracks(track_id, name, popularity)
                        values(%s, %s, %s)"""
    check_count_of_records = """select count(*) from top_tracks"""
    delete_old_top_tracks = """delete from top_tracks"""

    cursor.execute(check_count_of_records)
    record_count = cursor.fetchone()[0]
    if record_count > 0:
        cursor.execute(delete_old_top_tracks)
    cnx.commit()

    for track in top_tracks:
        cursor.execute(insert_into_top_tracks,
                   (track['id'],
                   track['name'],
                   track['popularity']))
    cnx.commit()
    