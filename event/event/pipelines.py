from itemadapter import ItemAdapter
from psycopg_pool import ConnectionPool

insert_artist = '''
with ins as (
    insert into artist (name)
    values (%(name)s)
    on conflict do nothing
    returning id
)
    select id from ins
union all
    select id from artist
    where name = %(name)s
limit 1
'''


insert_venue = '''
with ins as (
    insert into venue (name)
    values (%(name)s)
    on conflict do nothing
    returning id
)
    select id from ins
union all
    select id from venue
    where name = %(name)s
limit 1
'''

insert_event = '''
with ins as (
    insert into event
        (title, datetime, description)
    values
        (%(title)s, %(datetime)s, %(description)s)
    on conflict do nothing
    returning id
)
    select id from ins
union all
    select id from event
    where title = %(title)s
    and datetime = %(datetime)s
limit 1
'''

insert_artists_of_event = '''
insert into artists_of_event
    (artist_id, event_id)
values
    (%(artist_id)s, %(event_id)s)
on conflict do nothing
'''

insert_venue_of_event = '''
insert into venue_of_event
    (venue_id, event_id)
values
    (%(venue_id)s, %(event_id)s)
on conflict do nothing
'''


class PGPipeline:
    def open_spider(self, spider):
        conninfo = {
            'host': spider.settings.get("PG_HOST"),
            'dbname': spider.settings.get("PG_DBNAME"),
            'user': spider.settings.get("PG_USER"),
            'password': spider.settings.get("PG_PASSWORD"),
            'port': spider.settings.get("PG_PORT"),
        }
        conninfo = ' '.join([
            f'{key}={value}' for key, value in conninfo.items()])
        self.pool = ConnectionPool(conninfo, max_size=20)
        self.pool.wait()

    def close_spider(self, _):
        self.pool.close()

    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        with self.pool.connection() as conn:
            # save event
            (event_id,) = conn.execute(insert_event, {
                'title': adapter.get('title'),
                'datetime': adapter.get('datetime'),
                'description': adapter.get('description')
            }).fetchone()

            # save artists
            artists = adapter.get('artists')
            for artist in artists:
                (artist_id,) = conn.execute(insert_artist, {
                    'name': artist
                }).fetchone()

                # save artist of event
                conn.execute(insert_artists_of_event, {
                    'artist_id': artist_id,
                    'event_id': event_id
                })

            # save venue
            (venue_id,) = conn.execute(insert_venue, {
                'name': adapter.get('location')
            }).fetchone()

            # save venue of event
            conn.execute(insert_venue_of_event, {
                'venue_id': venue_id,
                'event_id': event_id
            })

        return item
