from flask_app.config.mysqlconnection import connectToMySQL

class FileTest:
    db = 'file_upload_schema'

    def __init__( self, data ):
        self.id = data['id']
        self.filename = data['filename']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save( cls, data ):
        query = """
        INSERT INTO files (filename, updated_at, created_at) VALUES (%(filename)s, NOW(), NOW());
        """

        return connectToMySQL( cls.db ).query_db( query, data )


    @classmethod
    def get_one_by_id( cls, data ):
        query = """
        SELECT * FROM files WHERE id = %(id)s;
        """

        results = connectToMySQL( cls.db ).query_db( query, data )

        return FileTest(results[0])
