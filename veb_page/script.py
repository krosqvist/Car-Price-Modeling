import sys
import db

arg = sys.argv[1]
def get_cars():
    sql = """SELECT * FROM cars WHERE model = ?"""
    result = db.query(sql, [arg])
    if result:
        return [dict(row) for row in result]
    else:
        return "No cars found"
    

print(get_cars())
