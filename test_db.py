
import database as db
class TestStringContainer:
    def test_db_sqlr(self):
        base = db.Database()
        base.init('{"ip": "127.0.0.1",  "port": 5432,	"dbname" : "my_test","dbuser" : "postgres",	"dbpass" : "undecodable"}')

        base = db.Database()
        base.connect()

        all_users = base.query('select 1')
        #print (all_users)
        assert all_users == [(1,)]
